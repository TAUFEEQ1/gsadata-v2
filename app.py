from flask import Flask
from models import db, User, Entity, Service
from utils import generate_signed_url
from forms import ServiceForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from flask import render_template, redirect, url_for, request, flash, Response
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.actions import action

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import NotFound
import click
import os
import csv
import io
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///services.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db.init_app(app)

with app.app_context():
    db.create_all()


@app.cli.command('create_admin')
@click.argument('username')
@click.argument('email')
@click.argument('password')
def create_admin(username, email, password):
    """Creates an admin user with the provided username and password."""
    admin = User.query.filter_by(username=username).first()
    if admin:
        print(f"User {username} already exists.")
    else:
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        admin = User(username=username, email=email, password=hashed_password)
        db.session.add(admin)
        db.session.commit()
        print(f"Admin user {username} created successfully.")

# Initialize login manager
login_manager = LoginManager(app)

login_manager.login_view = 'login'  # Redirect to login page if not logged in

# Login Manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Admin Views
class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    

class ServiceModelView(ModelView):
    # Configure list view
    list_template = 'admin/model/list.html'
    can_export = True
    export_max_rows = 1000
    
    @action('export_selected_csv', 'Export Selected to CSV', 'Export selected services to CSV?')
    def action_export_selected_csv(self, ids):
        """Export selected services with entity data as CSV"""
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write CSV header
        headers = [
            'Entity ID', 'Entity Name', 'Entity Category', 'Entity Sector',
            'Contact Name', 'Contact Position', 'Contact Phone', 'Contact Email',
            'Service ID', 'Service Name', 'Service Description', 'Interaction Category',
            'G2G Beneficiary Count', 'Geographic Reach', 'Process Flow',
            'Has KPI', 'KPI Details', 'Standard Duration', 'Actual Duration',
            'Users Total', 'Users Female', 'Users Male',
            'Customer Satisfaction Measured', 'Customer Satisfaction Rating',
            'Support Available', 'Support Available Via', 'Access Mode', 'Offices Count',
            'Access Website', 'Access Mobile App', 'Access USSD', 'Access Physical Office',
            'Requires Internet', 'Self Service Available', 'Supported by IT System',
            'System Vendor', 'System Ownership', 'System Type',
            'System Name', 'System Launch Date', 'System Version', 'System Last Update',
            'System Target Uptime', 'System Actual Uptime', 'Hosting Location', 'Funding Details',
            'Complies with Standards', 'Standards Details', 'System Integrated',
            'Integrated Systems', 'Planned Automation', 'Comments'
        ]
        writer.writerow(headers)
        
        # Query selected services with their related entities
        services = db.session.query(Service, Entity).join(Entity, Service.entity_id == Entity.id).filter(Service.id.in_(ids)).all()
        
        # Write data rows
        for service, entity in services:
            row = [
                entity.id, entity.name, entity.category, entity.sector,
                entity.contact_name, entity.contact_position, entity.contact_phone, entity.contact_email,
                service.id, service.service_name, service.description, service.interaction_category,
                service.g2g_beneficiary_count, service.geographic_reach, service.process_flow,
                'Yes' if service.has_kpi else 'No', service.kpi_details,
                service.standard_duration, service.actual_duration,
                service.users_total, service.users_female, service.users_male,
                'Yes' if service.customer_satisfaction_measured else 'No', service.customer_satisfaction_rating,
                'Yes' if service.support_available else 'No', service.support_available_via,
                service.access_mode, service.offices_count,
                'Yes' if service.access_website else 'No',
                'Yes' if service.access_mobile_app else 'No',
                'Yes' if service.access_ussd else 'No',
                'Yes' if service.access_physical_office else 'No',
                'Yes' if service.requires_internet else 'No',
                'Yes' if service.self_service_available else 'No',
                'Yes' if service.supported_by_it_system else 'No',
                service.system_vendor, service.system_ownership, service.system_type,
                service.system_name, service.system_launch_date, service.system_version,
                service.system_last_update, service.system_target_uptime, service.system_actual_uptime,
                service.hosting_location, service.funding_details,
                'Yes' if service.complies_with_standards else 'No', service.standards_details,
                'Yes' if service.system_integrated else 'No', service.integrated_systems,
                'Yes' if service.planned_automation else 'No', service.comments
            ]
            writer.writerow(row)
        
        # Create the response
        output.seek(0)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"gsa_services_selected_{timestamp}.csv"
        
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename={filename}'}
        )

    def is_accessible(self):
        """Only allow access for admins."""
        return current_user.is_authenticated


class EntityModelView(ModelView):
    form_columns = ['name', 'category', 'sector', 'contact_name', 'contact_position', 'contact_phone', 'contact_email']


    def on_model_change(self, form, model:Entity, is_created):
        """Override to generate signed link when creating a new entity."""
        if is_created:
            # Pass the app's secret key when generating the signed URL
            if not model.signed_service_link:
                sanitize_name= model.name.lower().replace(" ", "_")
                model.signed_service_link = url_for('add_service', signed_url=generate_signed_url(sanitize_name))
        # Call the parent class's method to ensure the model is saved
        return super(EntityModelView, self).on_model_change(form, model, is_created)

    @action('regenerate_link', 'Regenerate Link', 'Are you sure you want to regenerate the link for selected entities?')
    def action_regenerate_link(self, ids):
        count = 0
        for entity in Entity.query.filter(Entity.id.in_(ids)).all():
            sanitize_name = entity.name.lower().replace(" ", "_")
            entity.signed_service_link = url_for('add_service', signed_url=generate_signed_url(sanitize_name))
            count += 1
        db.session.commit()
        flash(f"Regenerated link for {count} entities.", "success")

    def is_accessible(self):
        """Only allow access for admins."""
        return current_user.is_authenticated

# Initialize Flask-Admin
admin = Admin(app, name='GSA Data Collection Tool - Admin', template_mode='bootstrap3')
admin.add_view(AdminModelView(User, db.session))
admin.add_view(EntityModelView(Entity, db.session))
admin.add_view(ServiceModelView(Service, db.session))

# Login Manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))  # Redirect to Flask-Admin dashboard
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('admin.index'))  # Redirect to Flask-Admin dashboard
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/services/<signed_url>', methods=['GET', 'POST'])
def add_service(signed_url):

    try:
        # Validate the signed URL and retrieve the entity ID
        entity:Entity = Entity.validate_signed_url(signed_url)
    except NotFound:
        flash("Invalid or expired signed URL.", "danger")
    
        return redirect(url_for('expired'))  # Redirect to expired page
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        return redirect(url_for('expired'))
    
    # list of all services for the entity
    services = Service.query.filter_by(entity_id=entity.id).all()
    
    if request.method == 'POST':

        form = ServiceForm()

        if form.validate_on_submit():
            
            service = Service(
                entity_id=entity.id,
                service_name=form.service_name.data,
                description=form.description.data,
                interaction_category=','.join(form.interaction_category.data),
                g2g_beneficiary_count=form.g2g_beneficiary_count.data,
                geographic_reach=form.geographic_reach.data,
                process_flow=form.process_flow.data,
                has_kpi=(form.has_kpi.data == 'Yes'),
                kpi_details=form.kpi_details.data,
                standard_duration=form.standard_duration.data,
                actual_duration=form.actual_duration.data,
                users_total=form.users_total.data,
                users_female=form.users_female.data,
                users_male=form.users_male.data,
                customer_satisfaction_measured=(form.customer_satisfaction_measured.data == 'Yes'),
                customer_satisfaction_rating=form.customer_satisfaction_rating.data,
                support_available=(form.support_available.data == 'Yes'),
                support_available_via=','.join(form.support_available_via.data) if form.support_available_via.data else None,
                access_mode=form.access_mode.data,
                access_website=(form.access_website.data == 'Yes'),
                access_mobile_app=(form.access_mobile_app.data == 'Yes'),
                access_ussd=(form.access_ussd.data == 'Yes'),
                access_physical_office=(form.access_physical_office.data == 'Yes'),
                requires_internet=(form.requires_internet.data == 'Yes'),
                self_service_available=(form.self_service_available.data == 'Yes'),
                supported_by_it_system=(form.supported_by_it_system.data == 'Yes'),
                system_name=form.system_name.data,
                system_launch_date=form.system_launch_date.data,
                system_version=form.system_version.data,
                system_last_update=form.system_last_update.data,
                system_target_uptime=form.system_target_uptime.data,
                system_actual_uptime=form.system_actual_uptime.data,
                complies_with_standards=(form.complies_with_standards.data == 'Yes'),
                standards_details=form.standards_details.data,
                system_integrated=(form.system_integrated.data == 'Yes'),
                integrated_systems=form.integrated_systems.data,
                planned_automation=(form.planned_automation.data == 'Yes'),
                comments=form.comments.data
            )

            db.session.add(service)
            db.session.commit()
            flash("Service added successfully!", "success")  # Move flash message here
            return redirect(url_for('add_service', signed_url=signed_url))
        else:
            return render_template('services.html', entity=entity, services=services, signed_url=signed_url, form=form)

    form = ServiceForm()

    return render_template('services.html', entity=entity, services=services, signed_url=signed_url, form=form)


@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/expired')
def expired():
    return render_template('expired_link.html')

@app.route('/admin/export_csv')
@login_required
def export_csv():
    """Export all services with entity data as CSV"""
    if not current_user.is_authenticated:
        flash("You must be logged in to access this feature.", "danger")
        return redirect(url_for('login'))
    
    # Create a string buffer to write CSV data
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write CSV header
    headers = [
        'Entity ID', 'Entity Name', 'Entity Category', 'Entity Sector',
        'Contact Name', 'Contact Position', 'Contact Phone', 'Contact Email',
        'Service ID', 'Service Name', 'Service Description', 'Interaction Category',
        'G2G Beneficiary Count', 'Geographic Reach', 'Process Flow',
        'Has KPI', 'KPI Details', 'Standard Duration', 'Actual Duration',
        'Users Total', 'Users Female', 'Users Male',
        'Customer Satisfaction Measured', 'Customer Satisfaction Rating',
        'Support Available', 'Support Available Via', 'Access Mode', 'Offices Count',
        'Access Website', 'Access Mobile App', 'Access USSD', 'Access Physical Office',
        'Requires Internet', 'Self Service Available', 'Supported by IT System',
        'System Vendor', 'System Ownership', 'System Type',
        'System Name', 'System Launch Date', 'System Version', 'System Last Update',
        'System Target Uptime', 'System Actual Uptime', 'Hosting Location', 'Funding Details',
        'Complies with Standards', 'Standards Details', 'System Integrated',
        'Integrated Systems', 'Planned Automation', 'Comments'
    ]
    writer.writerow(headers)
    
    # Query services with their related entities
    services = db.session.query(Service, Entity).join(Entity, Service.entity_id == Entity.id).all()
    
    # Write data rows
    for service, entity in services:
        row = [
            entity.id, entity.name, entity.category, entity.sector,
            entity.contact_name, entity.contact_position, entity.contact_phone, entity.contact_email,
            service.id, service.service_name, service.description, service.interaction_category,
            service.g2g_beneficiary_count, service.geographic_reach, service.process_flow,
            'Yes' if service.has_kpi else 'No', service.kpi_details,
            service.standard_duration, service.actual_duration,
            service.users_total, service.users_female, service.users_male,
            'Yes' if service.customer_satisfaction_measured else 'No', service.customer_satisfaction_rating,
            'Yes' if service.support_available else 'No', service.support_available_via,
            service.access_mode, service.offices_count,
            'Yes' if service.access_website else 'No',
            'Yes' if service.access_mobile_app else 'No',
            'Yes' if service.access_ussd else 'No',
            'Yes' if service.access_physical_office else 'No',
            'Yes' if service.requires_internet else 'No',
            'Yes' if service.self_service_available else 'No',
            'Yes' if service.supported_by_it_system else 'No',
            service.system_vendor, service.system_ownership, service.system_type,
            service.system_name, service.system_launch_date, service.system_version,
            service.system_last_update, service.system_target_uptime, service.system_actual_uptime,
            service.hosting_location, service.funding_details,
            'Yes' if service.complies_with_standards else 'No', service.standards_details,
            'Yes' if service.system_integrated else 'No', service.integrated_systems,
            'Yes' if service.planned_automation else 'No', service.comments
        ]
        writer.writerow(row)
    
    # Create the response
    output.seek(0)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"gsa_services_export_{timestamp}.csv"
    
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename={filename}'}
    )

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4949, debug=True)