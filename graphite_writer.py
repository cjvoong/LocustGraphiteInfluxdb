import platform, socket, time

class GraphiteWriter:
    def __init__(self,GRAPHITE_SERVER,GRAPHITE_PORT):
        try:
            self.sock = socket.socket()
            self.sock.connect((GRAPHITE_SERVER,GRAPHITE_PORT))
        except(Exception as e):
            print(f"An exception occurred whilst connecting to graphite: {e}")

            
    def send(self,metric_path,metric_value,timestamp):
        print("sending message")
        message = '%s %s %d\n' % (metric_path, metric_value, timestamp)
        self.sock.sendall(message)

    def close(self):
        self.sock.close()
