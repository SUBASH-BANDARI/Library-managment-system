from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
from celery import Celery
from flask_mail import Mail
from celery.schedules import crontab
from datetime import timedelta
from flask_caching import Cache
# from flask_uploads import UploadSet, configure_uploads, AUDIO

#app_password = yugclxjffzpmakel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = '7cc6619eb68e5c5f5d2ee4fc'
app.config['UPLOAD_FOLDER'] = '/Users/LENOVO-LP/OneDrive/Desktop/MAD-2/Muse/uploads'
app.config['UPLOADED_SONGS_DEST'] = '/Users/LENOVO-LP/OneDrive/Desktop/MAD-2/Muse/uploads'
db = SQLAlchemy(app)
api = Api(app)
CORS(app)
cache = Cache(app, config={
    'CACHE_TYPE': 'RedisCache',
    'CACHE_REDIS_URL': 'redis://default:umj1DuOzQYD5CkJwkRVaDzk15Mf3rAJB@redis-13479.c264.ap-south-1-1.ec2.cloud.redislabs.com:13479',
    'CACHE_DEFAULT_TIMEOUT': 300
})
celery = Celery(
     __name__,
    backend='redis://default:umj1DuOzQYD5CkJwkRVaDzk15Mf3rAJB@redis-13479.c264.ap-south-1-1.ec2.cloud.redislabs.com:13479',
    broker='redis://default:umj1DuOzQYD5CkJwkRVaDzk15Mf3rAJB@redis-13479.c264.ap-south-1-1.ec2.cloud.redislabs.com:13479',
    include=['application.celery_tasks'],
    imports = ('application.celery_tasks'),
)
app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '21f1002180@ds.study.iitm.ac.in'
app.config['MAIL_DEFAULT_SENDER'] = '21f1002180@ds.study.iitm.ac.in'
app.config['MAIL_PASSWORD'] = 'yugclxjffzpmakel'
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_ASCII_ATTACHMENTS'] = False
app.config['CELERY_BROKER_URL'] = 'redis://default:umj1DuOzQYD5CkJwkRVaDzk15Mf3rAJB@redis-13479.c264.ap-south-1-1.ec2.cloud.redislabs.com:13479'
app.config['CELERY_RESULT_BACKEND'] = 'redis://default:umj1DuOzQYD5CkJwkRVaDzk15Mf3rAJB@redis-13479.c264.ap-south-1-1.ec2.cloud.redislabs.com:13479'
app.config['CELERYBEAT_SCHEDULE'] = {
    'daily-visit': {
        'task': 'application.celery_tasks.daily_visit_reminder',
        'schedule': timedelta(days=1)
        # 'schedule': timedelta(seconds=10)
    },
    'monthly-report': {
        'task': 'application.celery_tasks.monthly_creator_report',
        'schedule': crontab(day_of_month=1, month_of_year='*')
        # 'schedule': timedelta(seconds=10)

    }
}

celery.conf.update(
    beat_schedule=app.config['CELERYBEAT_SCHEDULE']
)
mail = Mail(app)
# songs = UploadSet('songs', AUDIO)
# configure_uploads(app, songs)


from . import models
from . import controllers


with app.app_context():
    db.create_all()