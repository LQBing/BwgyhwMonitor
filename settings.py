
MAILL_SETTING={
    "from":"notification@yourdomain.com",
    "to":"",
    "password":"",
    "smtp":"smtp.yourdomain.com"
}


try:
    from local_settings import *
except ImportError:
    pass
