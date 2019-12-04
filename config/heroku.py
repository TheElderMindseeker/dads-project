import os
import datetime

SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.environ["SECRET_KEY"]

REMEMBER_COOKIE_NAME = "livebook_remember_me"
# 6 hours should be enough for current testing
REMEMBER_COOKIE_DURATION = datetime.timedelta(hours=6)
