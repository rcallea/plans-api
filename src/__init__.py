from flask import Flask


def create_app(config_name):
    app = Flask(__name__)
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@dbmetricas.cabyk5komby1.us-east-1.rds.amazonaws.com:5432/planes'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True, "pool_recycle": 600}
    return app
