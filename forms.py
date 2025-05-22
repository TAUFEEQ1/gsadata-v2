from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, SelectMultipleField, RadioField
from wtforms.validators import DataRequired, Optional, InputRequired, NumberRange


class ServiceForm(FlaskForm):
    service_name = StringField('Service Name', validators=[DataRequired()],
                               description="This refers to the official name of the government service delivered by the entity")
    description = TextAreaField("Service Description (a brief explanation of what a particular service is, who it is for, and what it entails)", validators=[
                                DataRequired()], description="This refers to a brief explanation of what a particular service is, who it is for, and what it entails")
    interaction_category = SelectMultipleField("Which category best describes the nature of interaction for this service? (Select one or more options)",
                                               choices=[
                                                   ('G2G', 'Government to Government (G2G)'),
                                                   ('G2B', 'Government to Business (G2B)'),
                                                   ('G2C', 'Government to Citizen (G2C)'),
                                               ],
                                               coerce=str,
                                               validators=[InputRequired()],
                                               description="This aims to identify the target user of the service. This will be dissagregated according to; Government to Government (G2G), Government to Business (G2B) and Government to Citizen (G2C). Select all options that apply"
                                               )
    g2g_beneficiary_count = IntegerField(
        'If G2G, how many entities benefit from the service? (All entities benefiting including the host entity)', validators=[Optional(), NumberRange(min=0, message="Please enter a positive number")])
    geographic_reach = SelectField('At what level is this service primarily delivered? (Targeted Geographic_Reach)?- Select one',
                                   choices=[
                                       ('Central Government', 'Central Government'),
                                       ('Local Government','Local Government'),
                                       ('Regional (East Africa)', 'Regional (East Africa)'),
                                       ('Global (Worldwide)','Global (Worldwide)'),
                                       ('Local (Internal to the entity only)','Local (Internal to the entity only)'),
                                       ('Sub County','Sub County'),
                                       ('Parish', 'Parish'),
                                   ],
                                   validators=[Optional()])
    process_flow = TextAreaField(
        'What are the key steps a user must follow to access and complete this service (process flow of the service)? Please include all stages, from the initial request to fulfillment', validators=[DataRequired()],
        description="This refers to the step-by-step sequence of activities/actions involved in delivering a service; from the point a user requests the service to the point it is completed or fulfilled.Provide a summary of the steps involved in accessing the specific service")
    has_kpi = RadioField(
        'Does service have Key Performance Indicators (KPI)? (Yes, No)',
        choices=[('Yes', 'Yes'), ('No', 'No')],
        default='No',
        description="This seeks to inquire whether the service has key performance indicators (KPI) for tracking performance of the service. If Yes, list all the KPIs available."
    )
    kpi_details = TextAreaField(
        'If Yes, list the KPIs', validators=[Optional()])
    standard_duration = StringField(
        'What is the standard average duration required to deliver the service from the time it is requested to its completion? (Recode average time in; seconds, minutes, hours, days, weeks, months)- ', validators=[Optional()])
    actual_duration = StringField(
        'What is the actual average duration taken to deliver the service from the time it is requested to its completion? (Recode average time in; seconds, minutes, hours, days, weeks, months)- ', validators=[Optional()], description="Refers to the duration between when a user requests a service and when the service is fully delivered or completed. This could be in seconds, minutes, hours, days, weeks or months. Here, indicate the servce standard turnaround time and actual turn around time")
    users_total = IntegerField(
        'What is the average or cumulative number of users of the service (Total)', validators=[Optional(), NumberRange(min=0, message="Please enter a positive number")])

    users_female = IntegerField(
        'What is the average or cumulative number of female users of the service?', validators=[Optional(), NumberRange(min=0, message="Please enter a positive number")])
    users_male = IntegerField(
        'What is the average or cumulative number of male users of the service?', validators=[Optional(), NumberRange(min=0, message="Please enter a positive number")])
    customer_satisfaction_measured = RadioField(
        'Has customer satisfaction been measured for the service before? (Yes, No)',
        choices=[('Yes', 'Yes'), ('No', 'No')],
        default='No'
    )
    customer_satisfaction_rating = StringField(
        'If Yes, What is the average customer satisfaction rating/level for the service, based on the most recent survey? (include unit)', validators=[Optional()])

    support_available = RadioField(
        'Are there existing support channels available for users to access help related to the specific government service?',
        choices=[('Yes', 'Yes'), ('No', 'No')],
        default='No',
        description="This refers to the channels through which users can access help or support related to the specific government service. Select all options that apply"
    )
    support_available_via = SelectMultipleField(
        'If Yes, how is support provided? (select all that apply)',
        choices=[
            ('Call Center', 'Call Center'),
            ('Help Desk', 'Help Desk'),
            ('Online Chat', 'Online Chat'),
            ('Email', 'Email'),
            ('Social Media', 'Social Media')
        ],
        coerce=str,
        validators=[Optional()],
        description="This refers to the channels through which users can access help or support related to the specific government service. Select all options that apply"
    )

    access_mode = SelectField('How is this service accessed by users? (select any of the options; Digital Only, Physical Only or Both)',
                              choices=[
                                  ('Digital Only', 'Digital Only'),
                                  ('Physical Only', 'Physical Only'),
                                  ('Both', 'Both')
                              ],
                              validators=[DataRequired()],
                              render_kw={"class": "radio-group"}
                              )
    offices_count = IntegerField(
        'How many offices or locations (including HQ) does the entity have to support the users?',
        validators=[Optional(), NumberRange(min=0, message="Please enter a positive number")]
    )

    access_website = RadioField(
        'Is the service available on a website? (Yes, No)',
        choices=[('Yes', 'Yes'), ('No', 'No')],
        default='No'
    )
    access_mobile_app = RadioField(
        'Is the service available on a mobile app? (Yes, No)',
        choices=[('Yes', 'Yes'), ('No', 'No')],
        default='No'
    )
    access_ussd = RadioField(
        'Is the service available on USSD? (Yes, No)',
        choices=[('Yes', 'Yes'), ('No', 'No')],
        default='No'
    )
    access_physical_office = RadioField(
        'Is the service available at a physical office? (Yes, No)',
        choices=[('Yes', 'Yes'), ('No', 'No')],
        default='No'
    )
    requires_internet = RadioField(
        'Does the service require internet access? (Yes, No)',
        choices=[('Yes', 'Yes'), ('No', 'No')],
        default='No'
    )
    self_service_available = RadioField(
        'Can a user access and complete the service on their own, without needing to physically visit an office or interact with a government official directly? (Yes, No)',
        choices=[('Yes', 'Yes'), ('No', 'No')],
        default='No'
    )
    supported_by_it_system = RadioField(
        'Is the service supported by an IT system? (Yes, No)',
        choices=[('Yes', 'Yes'), ('No', 'No')],
        default='No'
    )

    hosting_location = SelectField(
        'Where is the IT system hosted? (select one)',
        choices=[
            ('Cloud', 'Cloud'),
            ('On-premise', 'On-premise'),
            ('Hybrid', 'Hybrid')
        ],
        validators=[Optional()]
    )
    
    funding_details = StringField(
        'What is the funding source for the IT system? (e.g., Government, Private, Donor-funded)', validators=[Optional()])
    
    system_vendor = StringField(
        'Who is the vendor who supplied the system?', validators=[Optional()],
        description="Name of the vendor who supplied the system"
    )

    system_ownership = SelectField(
        'Who owns the rights to the system?',
        choices=[
            ('Vendor', 'Vendor'),
            ('Govt', 'Government'),
            ('Both', 'Both')
        ],
        validators=[Optional()],
        description="Who owns the rights to the system? (Vendor, Govt, Both)"
    )
    system_type = SelectField(
        'Is the system bespoke or off-the-shelf?',
        choices=[
            ('Bespoke', 'Bespoke'),
            ('Off-the-shelf', 'Off-the-shelf')
        ],
        validators=[Optional()],
        description="Is the system bespoke or off-the-shelf?"
    )

    system_name = StringField(
        'What is the name of the IT system that supports this service?', validators=[Optional()])
    system_launch_date = StringField(
        'When was the IT system launched? (dd/mm/yyyy)', validators=[Optional()])

    system_version = StringField(
        'What is the current version of the IT system?', validators=[Optional()])
    system_last_update = StringField(
        'When was the IT system last updated? (dd/mm/yyyy)', validators=[Optional()])
    system_target_uptime = StringField(
        'What is the target uptime for the IT system? (e.g., 99.9%)', validators=[Optional()])
    system_actual_uptime = StringField(
        'What is the actual uptime for the IT system? (e.g., 99.9%)', validators=[Optional()])

    complies_with_standards = RadioField(
        'Does the IT system comply with any standards (ITIL, ISO 20000, ISO 27000)? (Yes, No)',
        choices=[('Yes', 'Yes'), ('No', 'No')],
        default='No'
    )
    standards_details = TextAreaField(
        'If Yes, please provide details of the standards', validators=[Optional()])

    system_integrated = RadioField(
        'Is the IT system integrated with other systems? (Yes, No)',
        choices=[('Yes', 'Yes'), ('No', 'No')],
        default='No'
    )
    integrated_systems = TextAreaField(
        'If Yes, please provide details of the integrated systems', validators=[Optional()])

    planned_automation = RadioField(
        'If the service is not supported by an IT system, is there a plan to automate it?',
        choices=[('Yes', 'Yes'), ('No', 'No')],
        default='No'
    )

    comments = TextAreaField('Additional Comments', validators=[Optional()])

    def validate(self, extra_validators=None):
        if not super(ServiceForm, self).validate(extra_validators=extra_validators):
            return False

        # Conditional validation for 'offices_count' if 'access_mode' is 'Physical Only'
        if self.access_mode.data == 'Physical Only':
            if not self.offices_count.data or self.offices_count.data <= 0:
                self.offices_count.errors.append('Offices count must be greater than 0 when access mode is Physical Only.')
                return False

        # Conditional validation for 'kpi_details' if 'has_kpi' is True
        if self.has_kpi.data == 'Yes' and not self.kpi_details.data:
            self.kpi_details.errors.append('This field is required when "Has KPI" is selected.')
            return False

        # Conditional validation for 'system_name' if 'supported_by_it_system' is True
        if self.supported_by_it_system.data == 'Yes' and not self.system_name.data:
            self.system_name.errors.append('This field is required when "Supported by IT System" is selected.')
            return False

        # Conditional validation for 'integrated_systems' if 'system_integrated' is True
        if self.system_integrated.data == 'Yes' and not self.integrated_systems.data:
            self.integrated_systems.errors.append('This field is required when "System Integrated" is selected.')
            return False

        # Conditional validation for 'g2g_beneficiary_count' if 'G2G' is selected in 'interaction_category'
        if 'G2G' in self.interaction_category.data and not self.g2g_beneficiary_count.data:
            self.g2g_beneficiary_count.errors.append('This field is required when "G2G" is selected in Interaction Category.')
            return False

        # Conditional validation for 'customer_satisfaction_rating' if 'customer_satisfaction_measured' is True
        if self.customer_satisfaction_measured.data == 'Yes' and not self.customer_satisfaction_rating.data:
            self.customer_satisfaction_rating.errors.append('This field is required when "Customer Satisfaction Measured" is selected.')
            return False

        # Conditional validation for 'standards_details' if 'complies_with_standards' is True
        if self.complies_with_standards.data == 'Yes' and not self.standards_details.data:
            self.standards_details.errors.append('This field is required when "Complies with Standards" is selected.')
            return False

        # Conditional validation if 'supported_by_it_system' is True
        if self.supported_by_it_system.data == 'Yes':
            if not self.system_name.data:
                self.system_name.errors.append('This field is required when "Supported by IT System" is selected.')
                return False

            if not self.hosting_location.data:
                self.hosting_location.errors.append('This field is required when "Supported by IT System" is selected.')
                return False
            if not self.funding_details.data:
                self.funding_details.errors.append('This field is required when "Supported by IT System" is selected.')
                return False

        # Conditional validation for 'support_available_via' if 'support_available' is True
        if self.support_available.data == 'Yes' and not self.support_available_via.data:
            self.support_available_via.errors.append('This field is required when "Support Available" is selected.')
            return False

        return True