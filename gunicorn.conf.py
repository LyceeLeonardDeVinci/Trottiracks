bind = '127.0.0.1:8300'
workers = 1
loglevel = 'debug'
accesslog = '/var/log/gunicorn/access_log_trottiracks.log'
acceslogformat ="%(h)s %(l)s %(u)s %(t)s %(r)s %(s)s %(b)s %(f)s %(a)s"
errorlog =  '/var/log/gunicorn/error_log_trottiracks.log'
capture_output = True
