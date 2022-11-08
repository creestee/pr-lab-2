from flask import Flask, request, json
from threading import Thread, Lock
from components import *

import time
import queue
import requests

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

THREADS = 5

app = Flask(__name__)
aggregator_producer = queue.Queue()
aggregator_consumer = queue.Queue()

@app.route('/aggregator/producer', methods=['POST'])
def producer():
    aggregator_producer.put(json.loads(request.data))
    return {'status_code': 200}

@app.route('/aggregator/consumer', methods=['POST'])
def consumer():
    aggregator_consumer.put(json.loads(request.data))
    return {'status_code': 200}

class Aggregator(Thread):
    def __init__(self, aggregator_id, *args, **kwargs):
        self.agreggator_id = aggregator_id
        super(Aggregator, self).__init__(*args, **kwargs)

    def deliver(self):

        if aggregator_producer.empty():
            pass

        else:
            object = aggregator_producer.get()

            if object['package'] == 'packed':
                r = requests.post(
                    url='http://delivery:8003/deposit',
                    json=object
                )

                print(f"Object : {object['object']}, Object_ID : {object['object_id']}, Package : {BCOLORS.WARNING}{object['package']}{BCOLORS.ENDC}")

        if aggregator_consumer.empty():
            pass

        else:
            object_deliver = aggregator_consumer.get()
            if object_deliver['status'] == 'delivered':
                r = requests.post(
                    url='http://factory:8001/distribution',
                    json=object_deliver
                    )
                
                print(f"------------Delivery------------ : {object_deliver['object']}")

    def run(self):
        while True:
            try:
                self.deliver()
            except requests.ConnectionError as e:
                print(e)
            time.sleep(1)

def run_aggregator_module():
    threads = list()

    main_thread = Thread(target=lambda: app.run(
        host='0.0.0.0', 
        port=8002))
    
    threads.append(main_thread)

    for i in range(1, THREADS + 1):
        aggregator = Aggregator(i)
        threads.append(aggregator)
    
    for i, thread in enumerate(threads):
        thread.start()

if __name__ == '__main__':
    run_aggregator_module()