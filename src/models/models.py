from dataclasses import dataclass

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
import uuid
from marshmallow_sqlalchemy import fields

db = SQLAlchemy()


@dataclass
class Plans(db.Model):
    __tablename__ = "sports_plans"
    id = db.Column(UUID(), primary_key=True, autoincrement=False)
    price = db.Column(db.DECIMAL(asdecimal=False))
    description = db.Column(db.String(1024))
    short_name = db.Column(db.String(512))
    services = db.relationship('Services', secondary="sports_plan_services", back_populates='plans')


class Services(db.Model):
    __tablename__ = "sports_services"
    id = db.Column(UUID(), primary_key=True, autoincrement=False)
    type = db.Column(db.String(100))
    description = db.Column(db.String(512))
    plans = db.relationship('Plans', secondary="sports_plan_services", back_populates='services')

class PlansServices(db.Model):
    __tablename__ = "sports_plan_services"
    id_plan = db.Column(UUID(), db.ForeignKey("sports_plans.id"), primary_key=True)
    id_service = db.Column(UUID(), db.ForeignKey("sports_services.id"), primary_key=True)

class PlansSchema(SQLAlchemyAutoSchema):
    class Meta:
         include_fk = True
         model = Plans
         load_instance = True
         exclude = ('services',)

class PlansSchemaWithServices(SQLAlchemyAutoSchema):
    class Meta:
         include_fk = True
         model = Plans
         load_instance = True
         include_relationships = True
    services = fields.Nested('ServicesSchema', many=True)

class ServicesSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Services
         load_instance = True
         exclude = ('plans',)
         
class ServicesSchemaWithPlans(SQLAlchemyAutoSchema):
    class Meta:
         model = Services
         load_instance = True
         include_relationships = True
    plans = fields.Nested('PlansSchema', many=True)


@dataclass
class Notifications(db.Model):
    __tablename__ = "notification"
    id = db.Column(UUID(), primary_key=True, autoincrement=False)
    is_read = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(1024))
    creation_timestamp = db.Column(db.DateTime(timezone=False))
    sportman = db.Column(UUID(), db.ForeignKey("sport_man._uuid"))
    event = db.Column(UUID(), db.ForeignKey("events.id"))
    
class Events(db.Model):
    __tablename__ = "events"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(256))
    description = db.Column(db.String(1024))
    place = db.Column(db.String(256))
    start_timestamp = db.Column(db.DateTime(timezone=False))
    end_timestamp = db.Column(db.DateTime(timezone=False))

class SportMan(db.Model):
    __tablename__ = "sport_man"
    _uuid = db.Column(UUID(), primary_key=True, autoincrement=False)
    name = db.Column(db.String(128))
    lastName = db.Column(db.String(128))
    docType = db.Column(db.String(128))
    docNumber = db.Column(db.Integer) 
    gender = db.Column(db.String(128))
    birthCountry = db.Column(db.String(128))
    birthCity = db.Column(db.String(128))
    email = db.Column(db.String(128))
    age = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    height = db.Column(db.Integer)
    country = db.Column(db.String(128))
    city = db.Column(db.String(128))
    antiquity = db.Column(db.Integer)
    plan = db.Column(UUID())

class Trainer(db.Model):
    id = db.Column(UUID(), primary_key=True, autoincrement=False)
    name = db.Column(db.String(512))

class TrainerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Trainer
        include_relationships = True
        load_instance = True
        
class SportManSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = SportMan
         include_relationships = True
         load_instance = True

class EventSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Events
         include_relationships = True
         load_instance = True         

class NotificationsSchema(SQLAlchemyAutoSchema):
    class Meta:
         include_fk = True
         model = Notifications    
         load_instance = True
         include_relationships = True
         sportman = fields.Nested(SportManSchema, only=("_uuid", "name", "lastName"))
         event = fields.Nested(EventSchema, only=("id", "name", "description"), many=True)
