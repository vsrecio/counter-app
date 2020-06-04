import time
import redis
import socket
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

host_name = socket.gethostname() 
host_ip = socket.gethostbyname(host_name) 

@app.route("/hola")
def index():
    host = socket.gethostbyname(host_name) 
    return "Hola desde la instancia {} \n".format(host)

#counts 
def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return "Esta pagina ha sido visitada {} veces, deja de darle a F5  por favor! :).\n".format(count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
