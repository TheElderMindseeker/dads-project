import os
import datetime

SQLALCHEMY_DATABASE_URI = os.environ["DADS_TEST_DATABASE_URI"]
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "test_secret_key"

REMEMBER_COOKIE_NAME = "livebook_remember_me"
# 6 hours should be enough for current testing
REMEMBER_COOKIE_DURATION = datetime.timedelta(hours=6)
