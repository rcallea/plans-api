from flask import request
from flask_restful import Resource
from requests import HTTPError
from sqlalchemy import desc, asc
from sqlalchemy.exc import IntegrityError

from src.models.models import PlansSchemaWithServices, ServicesSchemaWithPlans, db, Plans, PlansSchema, Services, ServicesSchema, Notifications, NotificationsSchema

import uuid

plans_schema = PlansSchema()
plansWithServices_schema = PlansSchemaWithServices()
services_schema = ServicesSchema()
servicesWithPlans_schema = ServicesSchemaWithPlans()
notifications_schema = NotificationsSchema()

class ViewPlans(Resource):
    def get(self):
        try:
            return [plansWithServices_schema.dump(p) for p in Plans.query.order_by(asc(Plans.price)).all()]

        except HTTPError as err:
            #print(err.response.status_code)
            print(err.response.text)
            return {'message': 'error getting plans'}, 500


class ViewServices(Resource):
    def get(self):
        #print('get method Service API')
        #print(Services.query.all())
        return [servicesWithPlans_schema.dump(ca) for ca in Services.query.all()]
            
    def post(self):
        try:
            plans=request.json["plans"]
            print('Service to create:')
            print(plans)
            planto = Plans.query.get_or_404(uuid.UUID(str(plans)))
            #planto = Plans.query.filter(Plans.id == uuid.UUID(str(plans))).first()
            print('plan.query')
            print(planto)
            print(plans_schema.dump(planto))

            new_service = Services(id = uuid.uuid4(),
                                   type=request.json["type"], 
                                    description=request.json["description"])
            new_service.plans.append(planto)

            db.session.add(new_service)
            db.session.commit()
            #print('new service')
            #print(new_service)
        except IntegrityError as e:
            db.session.rollback()
            return 'El servicio ya existe',409
        return 'Objeto Creado',201

class ViewService(Resource):
    def get(self, uuid_service):
        try:
            getservice = Services.query.get(uuid_service)
            #print("buscar por uuid")
            #print(getservice)
            if getservice:
                return services_schema.dump(getservice)
            return {'mensage': 'servicio no encontrado'}, 404
        except IntegrityError:
            return {'mensage': 'error obteniendo el servicio'},500
    
    def delete(self, uuid_service):
        service = Services.query.get_or_404(uuid_service)
        db.session.delete(service)
        db.session.commit()
        return '',204
    

class ViewNotifications(Resource):
    def get(self, id_sportman):
        try:
            print('get')
            print(id_sportman)
            notif = Notifications.query.filter(Notifications.sportman==id_sportman)
            print('notificacion')
            print(notif)
            return [notifications_schema.dump(ca) for ca in notif]
        except HTTPError as err:
            print(err.response.status_code)
            print(err.response.text)
            return {'message': 'error getting notifications'}, 500

class ViewNotification(Resource):    
    def put(self, id_notification):
        notification = Notifications.query.get(id_notification)
        if notification == None :
            return {'mensage': 'deportista no encontrado'}, 404
        
        notification.is_read = request.json["is_read"]
        db.session.commit()
        return 'updated',204


#def is_valid_uuid(value):
#    try:
#        uuid.UUID(str(value))
#        return True
#    except ValueError:
#        return False