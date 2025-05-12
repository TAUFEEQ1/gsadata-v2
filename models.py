from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from utils import generate_signed_url,validate_signed_url
from werkzeug.exceptions import NotFound

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    # Additional fields can be added here

    def __repr__(self):
        return f"<User {self.username}>"


class Entity(db.Model):
    __tablename__ = 'entities'

    id = db.Column(db.Integer, primary_key=True)
    
    # Entity details
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100), nullable=True)
    sector = db.Column(db.String(100), nullable=True)
    
    # Contact person details
    contact_name = db.Column(db.String(255), nullable=True)
    contact_position = db.Column(db.String(100), nullable=True)
    contact_phone = db.Column(db.String(50), nullable=True)
    contact_email = db.Column(db.String(100), nullable=True)

    signed_service_link = db.Column(db.String(255), nullable=True)

    # Relationship to services is already defined in the Service model

    def __repr__(self):
        return f"<Entity {self.name}>"

    @classmethod
    def validate_signed_url(cls, signed_url):
        """
        Validates the signed URL and retrieves the associated entity ID.
        If the URL is invalid or expired, it raises a NotFound exception.
        """
        entity_name:str = validate_signed_url(signed_url)
        # Check if the entity exists in the database
        entity:Entity = cls.query.filter(Entity.name.ilike(entity_name.replace("_"," "))).first()

        if not entity:
            raise NotFound("Entity not found.")
        return entity

    def save(self, secret_key):
        """Save the entity to the database."""
        # Generate a signed URL for adding a service
        if not self.signed_service_link:
            self.signed_service_link = generate_signed_url(self.name.lower().replace(" ", "_"), secret_key)
        # Save the entity to the database
        db.session.add(self)
        db.session.commit()
    

class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    entity_id = db.Column(db.Integer, db.ForeignKey('entities.id'), nullable=False)

    service_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    interaction_category = db.Column(db.String(100), nullable=True)
    g2g_beneficiary_count = db.Column(db.Integer, nullable=True)
    geographic_reach = db.Column(db.String(100), nullable=True)
    process_flow = db.Column(db.Text, nullable=True)

    has_kpi = db.Column(db.Boolean, default=False)
    kpi_details = db.Column(db.Text, nullable=True)

    standard_duration = db.Column(db.String(100), nullable=True)
    actual_duration = db.Column(db.String(100), nullable=True)

    users_total = db.Column(db.Integer, nullable=True)
    users_female = db.Column(db.Integer, nullable=True)
    users_male = db.Column(db.Integer, nullable=True)

    customer_satisfaction_measured = db.Column(db.Boolean, default=False)
    customer_satisfaction_rating = db.Column(db.String(100), nullable=True)

    support_available = db.Column(db.Boolean, default=False)
    support_available_via = db.Column(db.String(100), nullable=True)  # e.g., Phone, Email, Chat

    access_mode = db.Column(db.String(50), nullable=True)  # e.g., Digital only, Physical only, Both

    access_website = db.Column(db.Boolean, default=False)
    access_mobile_app = db.Column(db.Boolean, default=False)
    access_ussd = db.Column(db.Boolean, default=False)
    access_physical_office = db.Column(db.Boolean, default=False)

    requires_internet = db.Column(db.Boolean, default=False)
    self_service_available = db.Column(db.Boolean, default=False)

    supported_by_it_system = db.Column(db.Boolean, default=False)
    system_name = db.Column(db.String(255), nullable=True)
    system_launch_date = db.Column(db.String(20), nullable=True)  # dd/mm/yyyy
    system_version = db.Column(db.String(50), nullable=True)
    system_last_update = db.Column(db.String(20), nullable=True)
    system_target_uptime = db.Column(db.String(50), nullable=True)
    system_actual_uptime = db.Column(db.String(50), nullable=True)
    hosting_location = db.Column(db.String(255), nullable=True)  # e.g., Cloud, On-premise, Hybrid
    funding_details = db.Column(db.String(255), nullable=True)  # e.g., Government, Private, Donor-funded

    complies_with_standards = db.Column(db.Boolean, default=False)
    standards_details = db.Column(db.Text, nullable=True)

    system_integrated = db.Column(db.Boolean, default=False)
    integrated_systems = db.Column(db.Text, nullable=True)

    planned_automation = db.Column(db.Boolean, default=False)

    comments = db.Column(db.Text, nullable=True)

    # Relationship back to entity
    entity = db.relationship('Entity', backref=db.backref('services', lazy=True))

    def __repr__(self):
        return f"<Service {self.service_name} for Entity ID {self.entity_id}>"

