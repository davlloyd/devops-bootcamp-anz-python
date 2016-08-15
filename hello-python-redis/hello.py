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

if os.getenv('VCAP_SERVICES'):
    stringstuff = os.getenv('VCAP_SERVICES')
    #Get my connection details
    services = json.loads(stringstuff)
    redis_env = services['rediscloud'][0]['credentials']

    #Create my connection details variable
    redis_env['host'] = redis_env['hostname']
    del redis_env['hostname']
    redis_env['port'] = int(redis_env['port'])
else:
    connect = redis.Redis(host='localhost', port='19226', password='')
            
try:
     myredis = redis.StrictRedis(**redis_env)
     redis.init
     status = "good"
except:
     status = "bad"


@app.route('/')
def hello():

    # check if I got a connection
    if myredis:

        #increment my value by 1
        current_hits = myredis.incr('dlhits')

        return """
        <html>
        <body bgcolor="{}">

        <center><h1><font color="white">Hi, I'm GUID:<br/>
        {}</br>

        Hits {}
        </center>

        </body>
        </html>
        """.format(COLOR,my_uuid, current_hits)
    else:
        return "no redis"
        
if __name__ == "__main__":
	app.run(debug=True,host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
