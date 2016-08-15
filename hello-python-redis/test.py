import os
import uuid
import redis
import json
from flask import Flask


app = Flask(__name__)
my_uuid = str(uuid.uuid1())
BLUE = "#0099FF"
GREEN = "#33CC33"

COLOR = GREEN


# Get Redis credentials
if 'VCAP_SERVICES' in os.environ:
    services = json.loads(os.getenv('VCAP_SERVICES'))
    redis_env = services['rediscloud'][0]['credentials']
else:
    redis_env = dict(hostname='localhost', port=6379, password='')

redis_env['host'] = redis_env['hostname']
del redis_env['hostname']
redis_env['port'] = int(redis_env['port'])

# Connect to redis
try:
    r = redis.StrictRedis(**redis_env)
    r.info()
except redis.ConnectionError:
    r = None

@app.route('/')
def hello():

    if r:
        r=0
        #current_hits = r.incr('hits')
        return """
        <html>
        <body bgcolor="{}">

        <center><h1><font color="white">Hi, I'm GUID:<br/>
        {}</br>
        <br>
        Hits {}
        </center>

        </body>
        </html>
        """.format(COLOR,my_uuid,hits)
    else:
        return "no redis"

if __name__ == "__main__":
	app.run(debug=False,host='0.0.0.0', port=int(os.getenv('PORT', '5555')))
