from src import create_app
from flask_restful import Api
from flask_cors import CORS
from .views import ViewPlans, ViewService, ViewServices, ViewNotifications, ViewNotification
from .models import db

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

CORS(app)
api = Api(app)
api.add_resource(ViewPlans, '/plans') #obtiene planes
api.add_resource(ViewServices, '/partner/service') #services
api.add_resource(ViewService, '/partner/service/<uuid:uuid_service>')
api.add_resource(ViewNotifications, '/notifications/<uuid:id_sportman>') # obtiene las notificaciones del deportista
api.add_resource(ViewNotification, '/notification/<uuid:id_notification>') # actualiza Notificacion (leida)

@app.route('/ping')
def home():
    return 'pong'


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug = True)

