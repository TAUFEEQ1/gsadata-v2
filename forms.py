from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, BooleanField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Optional


class ServiceForm(FlaskForm):
    service_name = StringField('Service Name', validators=[DataRequired()],
                               description="This refers to the official name of the government service delivered by the entity")
    description = TextAreaField("Service Description (a brief explanation of what a particular service is, who it is for, and what it entails)", validators=[
                                Optional()], description="This refers to a brief explanation of what a particular service is, who it is for, and what it entails")
    interaction_category = SelectMultipleField("Which category best describes the nature of interaction for this service? (Select one or more options)",
                                               choices=[
                                                   ('G2G', 'Government to Government (G2G)'),
                                                   ('G2B', 'Government to Business (G2B)'),
                                                   ('G2C', 'Government to Citizen (G2C)'),
                                               ],
                                               validators=[DataRequired()],
                                               description="This aims to identify the target user of the service. This will be dissagregated according to; Government to Government (G2G), Government to Business (G2B) and Government to Citizen (G2C). Select all options that apply"
                                               )
    g2g_beneficiary_count = IntegerField(
        'If G2G, how many entities benefit from the service? (All entities benefiting including the host entity)', validators=[Optional()])
    geographic_reach = SelectField('At what level is this service primarily delivered? (Targeted Geographic_Reach)?- Select one',
                                   choices=[
                                       ('National', 'National'),
                                       ('Regional', 'Regional'),
                                       ('Local', 'Local'),
                                       ('Global', 'Global'),
                                   ],
                                   validators=[Optional()])
    process_flow = TextAreaField(
        'What are the key steps a user must follow to access and complete this service (process flow of the service)? Please include all stages, from the initial request to fulfillment', validators=[DataRequired()],
        description="This refers to the step-by-step sequence of activities/actions involved in delivering a service; from the point a user requests the service to the point it is completed or fulfilled.Provide a summary of the steps involved in accessing the specific service")
    has_kpi = BooleanField(
        'Does service have Key Performance Indicators (KPI)? (Yes, No)', default=False,description="This seeks to inquire whether the service has key performance indicators (KPI) for tracking performance of the service. If Yes, list all the KPIs available.")
    kpi_details = TextAreaField(
        'If Yes, list the KPIs', validators=[Optional()])
    standard_duration = StringField(
        'What is the standard average duration required to deliver the service from the time it is requested to its completion? (Recode average time in; seconds, minutes, hours, days, weeks, months)- ', validators=[Optional()])
    actual_duration = StringField(
        'What is the actual average duration taken to deliver the service from the time it is requested to its completion? (Recode average time in; seconds, minutes, hours, days, weeks, months)- ', validators=[Optional()],description="Refers to the duration between when a user requests a service and when the service is fully delivered or completed. This could be in seconds, minutes, hours, days, weeks or months. Here, indicate the servce standard turnaround time and actual turn around time")
    users_total = IntegerField(
        'What is the average or cumulative number of users of the service (Total)', validators=[Optional()])
    users_female = IntegerField(
        'What is the average or cumulative number of female users of the service?', validators=[Optional()])
    users_male = IntegerField(
        'What is the average or cumulative number of male users of the service?', validators=[Optional()])
    customer_satisfaction_measured = BooleanField(
        'Has customer satisfaction been measured for the service before? (Yes, No)', default=False)
    customer_satisfaction_rating = StringField(
        'If Yes, What is the average customer satisfaction rating/level for the service, based on the most recent survey? (include unit)', validators=[Optional()])

    support_available = BooleanField(
        'Are there exisiting support channels  available for users to access help related to the specific government service? (Yes, No)', default=False)
    support_help_desk = BooleanField(
        'Is there a help desk available for users to access help related to the specific government service? (Yes, No)', default=False)
    support_call_center = BooleanField(
        'Is there a call center available for users to access help related to the specific government service? (Yes, No)', default=False)
    support_online_chat = BooleanField(
        'Is there an online chat/bots available for users to access help related to the specific government service? (Yes, No)', default=False)
    support_email = BooleanField(
        'Is there an email available for users to access help related to the specific government service? (Yes, No)', default=False)

    support_social_media = BooleanField(
        'Is there a social media available for users to access help related to the specific government service? (Yes, No)', default=False)

    access_mode = SelectField('How is this service accessed by users? (select any of the options; Digital Only, Physical only or both online and physical)',
                              choices=[
                                  ('Digital Only', 'Digital Only'),
                                  ('Physical Only', 'Physical Only'),
                                  ('Both', 'Both')
                              ],
                              validators=[DataRequired()],
                              )
    access_website = BooleanField(
        'Is the service available on a website? (Yes, No)', default=False)
    access_mobile_app = BooleanField(
        'Is the service available on a mobile app? (Yes, No)', default=False)
    access_ussd = BooleanField(
        'Is the service available on USSD? (Yes, No)', default=False)
    access_physical_office = BooleanField(
        'Is the service available at a physical office? (Yes, No)', default=False)
    requires_internet = BooleanField(
        'Does the service require internet access? (Yes, No)', default=False)
    self_service_available = BooleanField(
        'Can a user access and complete the service on their own, without needing to physically visit an office or interact with a government official directly? (Yes, No)', default=False)
    supported_by_it_system = BooleanField(
        'Is the service supported by an IT system? (Yes, No)', default=False)

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

    complies_with_standards = BooleanField(
        'Does the IT system comply with any standards? (Yes, No)', default=False)
    standards_details = TextAreaField(
        'If Yes, please provide details of the standards', validators=[Optional()])

    system_integrated = BooleanField(
        'Is the IT system integrated with other systems? (Yes, No)', default=False)
    integrated_systems = TextAreaField(
        'If Yes, please provide details of the integrated systems', validators=[Optional()])

    planned_automation = BooleanField(
        'If the service is not supported by an IT system, is there a plan to automate it?', default=False)

    comments = TextAreaField('Additional Comments', validators=[Optional()])

    def validate(self):
        if not super(ServiceForm, self).validate():
            return False

        # Conditional validation for 'kpi_details' if 'has_kpi' is True
        if self.has_kpi.data and not self.kpi_details.data:
            self.kpi_details.errors.append('This field is required when "Has KPI" is selected.')
            return False

        # Conditional validation for 'system_name' if 'supported_by_it_system' is True
        if self.supported_by_it_system.data and not self.system_name.data:
            self.system_name.errors.append('This field is required when "Supported by IT System" is selected.')
            return False

        # Conditional validation for 'integrated_systems' if 'system_integrated' is True
        if self.system_integrated.data and not self.integrated_systems.data:
            self.integrated_systems.errors.append('This field is required when "System Integrated" is selected.')
            return False
        
        # Conditional validation for 'g2g_beneficiary_count' if 'G2G' is selected in 'interaction_category'
        if 'G2G' in self.interaction_category.data and not self.g2g_beneficiary_count.data:
            self.g2g_beneficiary_count.errors.append('This field is required when "G2G" is selected in Interaction Category.')
            return False
        
        # Conditional validation for 'customer_satisfaction_rating' if 'customer_satisfaction_measured' is True
        if self.customer_satisfaction_measured.data and not self.customer_satisfaction_rating.data:
            self.customer_satisfaction_rating.errors.append('This field is required when "Customer Satisfaction Measured" is selected.')
            return False

        # Conditional validation for 'standards_details' if 'complies_with_standards' is True
        if self.complies_with_standards.data and not self.standards_details.data:
            self.standards_details.errors.append('This field is required when "Complies with Standards" is selected.')
            return False


        # Conditional validation for 'integrated_systems' if 'system_integrated' is True
        if self.system_integrated.data and not self.integrated_systems.data:
            self.integrated_systems.errors.append('This field is required when "System Integrated" is selected.')
            return False

        return True