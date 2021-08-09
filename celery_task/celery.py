import os

from celery import Celery
import django

# 加载Django环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookshop.settings.pro")
django.setup()

broker = 'redis://127.0.0.1:6379/1'  # 任务队列
backend = 'redis://127.0.0.1:6379/2'  # 结果存储

app = Celery(__name__, broker=broker, backend=backend, include=['bookshop.apps.goods.task'])

# 时区
app.conf.timezone = 'Asia/Shanghai'
# 是否使用UTC
app.conf.enable_utc = False

# # 执行定时任务配置
# from celery.schedules import crontab
#
# app.conf.beat_schedule = {
#     'add-task': {
#         'task': 'celery_task.home_task.banner_update',
#         # 'schedule': timedelta(seconds=30),
#         'schedule': crontab(hour=8, day_of_week=1),  # 每周一早八点
#     }
# }

# 启动beat
# celery beat -A celery_task -l info
