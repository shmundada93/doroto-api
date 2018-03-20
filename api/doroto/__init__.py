import os
from flask import Flask, jsonify, g
from flask.ext.sqlalchemy import SQLAlchemy
from celery import Celery
from .decorators import json, no_cache, rate_limit
import boto3

db = SQLAlchemy()


def create_app(config_name):
    """Create an application instance."""
    app = Flask(__name__)

    # apply configuration
    cfg = os.path.join(os.getcwd(), 'config', config_name + '.py')
    app.config.from_pyfile(cfg)

    # initialize extensions
    db.init_app(app)

    # register blueprints
    from .api_v1 import api as api_blueprint
    from .api_v1_public import api as api_public_blueprint

    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    app.register_blueprint(api_public_blueprint, url_prefix='/api/v1/p')

    # register an after request handler
    @app.after_request
    def after_request(rv):
        headers = getattr(g, 'headers', {})
        rv.headers.extend(headers)
        return rv

    # authentication token route
    from .auth import auth
    @app.route('/get-auth-token')
    @auth.login_required
    @rate_limit(1, 600)  # one call per 10 minute period
    @no_cache
    @json
    def get_auth_token():
        return {'token': g.user.generate_auth_token(), 'role': g.user.role.name, 'id': g.user.id}

    return app

def make_celery(config_name):
    """Create an application instance."""
    app = Flask(__name__)

    # apply configuration
    cfg = os.path.join(os.getcwd(), 'config', config_name + '.py')
    app.config.from_pyfile(cfg)

    # Initialize aws client
    aws_client = boto3.Session(
        aws_access_key_id=app.config['AWS_ACCESS_KEY'],
        aws_secret_access_key=app.config['AWS_ACCESS_KEY_SECRET'],
        region_name=app.config['AWS_REGION']
    )

    # initialize extensions
    db.init_app(app)

    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_BACKEND_URL']
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery, app, aws_client