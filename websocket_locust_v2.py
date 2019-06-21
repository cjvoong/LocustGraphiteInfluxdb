from websocket import create_connection
from locust import HttpLocust, TaskSet, task, events
import ssl, json, uuid, six, time,redis,random,graphyte
from locust.events import request_success, request_failure

class EchoTaskSet(TaskSet):
    
    def on_start(self):
        print("on_start")
        #print("Connecting to redis")
        #r = redis.Redis(host='localhost',port=6379)
        #vals = r.spop("locust_users",2)
        #print(vals)
        #graphyte.init('perf-test-influxdb')

    @task
    def send_message(self):
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

        myrandom = random.randint(1,10)

        if myrandom == 1:
            request_failure.fire(            
                request_type='WebSocket Response',
                name='ws',
                response_time=response_time,
                exception = Exception("My Exception")
            )
        else:
            request_success.fire(            
                request_type='WebSocket Response',
                name='ws',
                response_time=response_time,
                response_length=len(res)
                )

    @task
    def http_index(self):
        self.client.get("/echo.html")

class SocketUser(HttpLocust):
    task_set = EchoTaskSet
    min_wait=0
    max_wait=0

    def __init__(self):
        super(SocketUser,self).__init__()
        graphyte.init('perf-test-influxdb',2003)
        events.request_success += self.hook_request_success
        events.request_failure += self.hook_request_failure
        events.quitting += self.exit_handler

    def format_name(self, name):
        return name.replace(',','-').replace('.','-').replace('/','_')

    def hook_request_success(self, request_type, name, response_time, response_length):
        graphyte.send("perf." + self.format_name(name) + ".response_time",response_time)
        graphyte.send("perf." + self.format_name(name) + ".response_length",response_length)

    def hook_request_failure(self,request_type, name, response_time, exception):
        graphyte.send("perf." + self.format_name(name) + ".failures",1)
        graphyte.send("perf." + self.format_name(name) + ".exceptions." + type(exception).__name__.replace(" ","_"),1)

    def exit_handler(self):
        print("Quitting...")