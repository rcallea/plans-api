import unittest
import uuid
from sqlalchemy.exc import IntegrityError
from src.app import app
from sqlalchemy import text
from src.models.models import  Plans, PlansSchema, db
import json
plan_schema = PlansSchema()

class CalendarTestCase(unittest.TestCase):

    def setUp(self):
        '''Creating Testing Data'''
        print('Creating Testing Data')
        service = Plans(id=uuid.uuid4(), price=0, description="", short_name="TestName")
        db.session.add(service)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'Se produjo un error al efectuar los cambios',409

    def tearDown(self):
        '''Deleting Testing Data'''
        print('Deleting Testing Data')
        try:
            Plans.query.filter(Plans.short_name.like('TestName%')).delete()    
            db.session.commit()
        except Exception as e:
            print(str(e))
            db.session.rollback()
        finally: 
            db.session.close()
        
    def test_get_plans(self):
        print("\n- Get Planes\n")
        client = app.test_client(self)
        res = client.get('/plans')
        self.assertEqual(res.status_code, 200)
        
    def test_get_ping(self):
        print("\n- Get ping\n")
        client = app.test_client(self)
        res = client.get('/ping')
        self.assertEqual(res.status_code, 200)
            
if __name__ == "__main__":
    unittest.main()