from flask import Flask
from models import db, User, Entity, Service
from utils import generate_signed_url
from forms import ServiceForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from flask import render_template, redirect, url_for, request, flash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import NotFound
import click
import os
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
    

class EntityModelView(ModelView):
    form_columns = ['name', 'category', 'sector', 'contact_name', 'contact_position', 'contact_phone', 'contact_email']


    def on_model_change(self, form, model:Entity, is_created):
        """Override to generate signed link when creating a new entity."""
        if is_created:
            # Pass the app's secret key when generating the signed URL
            if not model.signed_service_link:
                sanitize_name= model.name.lower().replace(" ", "_")
                model.signed_service_link = url_for('add_service', signed_url=generate_signed_url(sanitize_name), _external=True)
        # Call the parent class's method to ensure the model is saved
        return super(EntityModelView, self).on_model_change(form, model, is_created)

    def is_accessible(self):
        """Only allow access for admins."""
        return current_user.is_authenticated

# Initialize Flask-Admin
admin = Admin(app, name='GSA Data Collection Tool - Admin', template_mode='bootstrap3')
admin.add_view(AdminModelView(User, db.session))
admin.add_view(EntityModelView(Entity, db.session))
admin.add_view(AdminModelView(Service, db.session))

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
    
        return redirect(url_for('login'))  # Redirect to login page or any other page
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        return redirect(url_for('login'))
    
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
                has_kpi=form.has_kpi.data,
                kpi_details=form.kpi_details.data,
                standard_duration=form.standard_duration.data,
                actual_duration=form.actual_duration.data,
                users_total=form.users_total.data,
                users_female=form.users_female.data,
                users_male=form.users_male.data,
                customer_satisfaction_measured=form.customer_satisfaction_measured.data,
                customer_satisfaction_rating=form.customer_satisfaction_rating.data,
                support_available=form.support_available.data,
                support_call_center=form.support_call_center.data,
                support_help_desk=form.support_help_desk.data,
                support_online_chat=form.support_online_chat.data,
                support_email=form.support_email.data,
                support_social_media=form.support_social_media.data,
                access_mode=form.access_mode.data,
                access_website=form.access_website.data,
                access_mobile_app=form.access_mobile_app.data,
                access_ussd=form.access_ussd.data,
                access_physical_office=form.access_physical_office.data,
                requires_internet=form.requires_internet.data,
                self_service_available=form.self_service_available.data,
                supported_by_it_system=form.supported_by_it_system.data,
                system_name=form.system_name.data,
                system_launch_date=form.system_launch_date.data,
                system_version=form.system_version.data,
                system_last_update=form.system_last_update.data,
                system_target_uptime=form.system_target_uptime.data,
                system_actual_uptime=form.system_actual_uptime.data,
                complies_with_standards=form.complies_with_standards.data,
                standards_details=form.standards_details.data,
                system_integrated=form.system_integrated.data,
                integrated_systems=form.integrated_systems.data,
                planned_automation=form.planned_automation.data,
                comments=form.comments.data
            )

            db.session.add(service)
            db.session.commit()
            flash("Service added successfully!", "success")  # Move flash message here
            return redirect(url_for('add_service', signed_url=signed_url))
        else:
            flash("Please correct the errors in the form.", "danger")
            return render_template('services.html', entity=entity, services=services, signed_url=signed_url, form=form)

    form  = ServiceForm()


    return render_template('services.html', entity=entity, services=services,signed_url=signed_url, form=form)



@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4949, debug=True)