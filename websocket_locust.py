from websocket import create_connection
from locust import HttpLocust, TaskSet, task
from locust.events import request_success
import ssl, json, uuid, six, time,redis
import graphyte

class EchoTaskSet(TaskSet):
    
    def on_start(self):
        print("on_start")
        #print("Connecting to redis")
        #r = redis.Redis(host='localhost',port=6379)
        #vals = r.spop("locust_users",2)
        #print(vals)
        graphyte.init('perf-test-influxdb')

    @task
    def sendMessage(self):
        ws = create_connection("wss://echo.websocket.org",
            sslopt={"cert_reqs": ssl.CERT_NONE})

        user_id = six.text_type(uuid.uuid4())
        start_at = time.time()
        json_val = {
            'id':user_id,
            'salutation': "Hello",
            'name': "James",
            'start_at': start_at
        }
        msg = json.dumps(json_val)        
        ws.send(msg)
        print(f"Sent {msg}")
        res = ws.recv()
        data = json.loads(res)
        end_at = time.time()
        response_time = int((end_at - data['start_at']) * 1000)
        print(f"Received {res}")        
        print(f"Got back id {data['id']}")
        request_success.fire(            
            request_type='WebSocket Response',
            name='ws',
            response_time=response_time,
            response_length=len(res),
        )
        graphyte.send('websocket.response_time',response_time)

class SocketUser(HttpLocust):
    task_set = EchoTaskSet
    min_wait=0
    max_wait=0
    events.request_success +=
    events.request_failure +=


    def teardown(self):
        print("teardown")
