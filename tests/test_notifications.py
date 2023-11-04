import unittest
import uuid
from sqlalchemy.exc import IntegrityError
from src.app import app
from sqlalchemy import text
from src.models.models import db, Notifications
import json
import datetime

class NotificationsTestCase(unittest.TestCase):
    def setUp(self):
        '''Creating Testing Data'''
        print('Creating Testing Data')
        try:
            notificacion = Notifications(id=uuid.uuid4(), 
                                         is_read=False, 
                                         description='Test event',
                                         creation_timestamp=datetime.datetime.now(),
                                         sportman='b1fb35a0-7061-708d-6d60-ba52bac9a883',
                                         event = 'b460327a-ff28-4c61-bdd4-a970a3f0f481')
            db.session.add(notificacion)
            db.session.commit()
        except Exception as e:
            print(str(e))
            db.session.rollback()

    def tearDown(self):
        '''Deleting Testing Data'''
        print('Deleting Testing Data')
        try:
            
            notifications = Notifications.query.filter(Notifications.description.like('Test%')).all()

            for notification in notifications:
                Notifications.query.filter(Notifications.id.__eq__(notification.id)).delete()
            
            db.session.commit()
        except Exception as e:
            print(str(e))
            db.session.rollback()
        finally: 
            db.session.close()

    def test_get_notifications(self):
        print("\n- Get Notifications by sportman\n")
        client = app.test_client(self)
        res = client.get('/notifications/' + str('b1fb35a0-7061-708d-6d60-ba52bac9a883'))
        self.assertEqual(res.status_code, 200)

    def test_get_and_update_notification(self):
        print("\n- Get and Update Notification \n")
        client = app.test_client(self)
        notification = Notifications.query.filter(Notifications.description.like('Test%')).first()
        print("notificacion devuelta")
        print(notification.id)

        body = {"is_read": True }

        res = client.put('/notification/' + str(notification.id), json=body)
        self.assertEqual(res.status_code, 204)

if __name__ == "__main__":
    unittest.main()