from locust.events import request_success
import graphyte

class LocustStats:
    def __init__(self):
        graphyte.init('perf-test-influxdb')
    
    def collect(self):        
        graphyte.send('websocket.response_time',response_time)
