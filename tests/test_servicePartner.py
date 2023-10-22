import unittest
import uuid
from sqlalchemy.exc import IntegrityError
from src.app import app
from sqlalchemy import text
from src.models.models import  Plans, Services, PlansServices, ServicesSchema, db
import json

class PartnerTestCase(unittest.TestCase):
    def setUp(self):
        '''Creating Testing Data'''
        print('Creating Testing Data')
        try:
            plan = Plans(id=uuid.uuid4(), price=0, description="", short_name="TestName")
            db.session.add(plan)
            db.session.commit()

            service = Services(id=uuid.uuid4(), type="virtual", description="TestService")
            service.plans.append(plan)
            db.session.add(service)
            db.session.commit()

        except Exception as e:
            print(str(e))
            db.session.rollback()
            #return 'Se produjo un error al efectuar los cambios',409
        
    def tearDown(self):
        '''Deleting Testing Data'''
        print('Deleting Testing Data')
        try:
            
            services = Services.query.filter(Services.description.like('Test%')).all()

            for service in services:
                PlansServices.query.filter(PlansServices.id_service.__eq__(service.id)).delete()
            
            Services.query.filter(Services.description.like('Test%')).delete()
            Plans.query.filter(Plans.short_name.like('Test%')).delete()    
            
            db.session.commit()
        except Exception as e:
            print(str(e))
            db.session.rollback()
        finally: 
            db.session.close()
    
    def test_get_ping(self):
        print("\n- Get ping\n")
        client = app.test_client(self)
        res = client.get('/ping')
        self.assertEqual(res.status_code, 200)

    def test_get_service(self):
        print("\n- Get Services\n")
        client = app.test_client(self)
        res = client.get('/partner/service', headers={"uuid":"00000000-0000-0000-0000-000000000000" })
        self.assertEqual(res.status_code, 200)
    
    def test_post_service(self):
        print("\n- Post Creating Service \n")
        client = app.test_client(self)
        plan = Plans.query.filter(Plans.short_name.like('Test%')).first()
        #print("plan-")
        #print(plan)
        body = {"id":uuid.uuid4(), "type": "virtual", "description":"TestMedico", "plans":plan.id}
        res = client.post('/partner/service', json=body, headers={"uuid":"00000000-0000-0000-0000-000000000000" }, content_type='application/json')
        self.assertEqual(res.status_code, 201)
        
    def test_get_and_delete_service(self):
        print("\n- Get and Delete Service \n")
        client = app.test_client(self)
        service = Services.query.filter(Services.description.like('Test%')).first()
        #print("plan-")
        #print(plan)
        res = client.get('/partner/service/' + str(service.id), headers={"uuid":"00000000-0000-0000-0000-000000000000" })
        self.assertEqual(res.status_code, 200)
        res = client.delete('/partner/service/' + str(service.id), headers={"uuid":"00000000-0000-0000-0000-000000000000" })
        self.assertEqual(res.status_code, 204)
        
    def test_get_not_found(self):
        print("\n- Get Service and NotFound \n")
        client = app.test_client(self)
        res = client.get('/partner/service/00000000-0000-0000-0000-000000000000', headers={"uuid":"00000000-0000-0000-0000-000000000000" })
        self.assertEqual(res.status_code, 404)

if __name__ == "__main__":
    unittest.main()