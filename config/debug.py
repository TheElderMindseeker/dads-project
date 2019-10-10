import os
import datetime

SQLALCHEMY_DATABASE_URI = os.environ["DADS_DATABASE_URI"]
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "a3288c46f69ac98053230126df0e17bdba755dd814cdc259"

REMEMBER_COOKIE_NAME = "livebook_remember_me"
# 6 hours should be enough for current testing
REMEMBER_COOKIE_DURATION = datetime.timedelta(hours=6)
