from flask import Flask
from threading import Thread, Lock
from components import *

import random
import requests
import time

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

THREADS = 5
TIME_UNIT = 5

app = Flask(__name__)
threads = []

# thread safe counter class
class ThreadSafeCounter():
    # constructor
    def __init__(self):
        # initialize counter
        self._counter = -1
        # initialize lock
        self._lock = Lock()
    
    # increment the counter
    def increment(self):
        with self._lock:
            self._counter += 1
 
    # get the counter value
    def value(self):
        self.increment()
        with self._lock:
            return self._counter

counter = ThreadSafeCounter()

@app.route('/distribution', methods=['POST'])
def distribution():
    return {'status_code': 200}

class Factory(Thread):
    def __init__(self, factory_id, *args, **kwargs):
        self.factory_id = factory_id
        self.id = 0
        super(Factory, self).__init__(*args, **kwargs)


    def generate_delivery(self):

        new_object = {
            'object': random.choice(objects),
            'object_id': counter.value(),
            'status' : 'undelivered',
            'package' : random.choice(['packed', 'unpacked'])
        }

        requests.post(
            url='http://aggregator:8002/aggregator/producer',
            json=new_object
        )

        if new_object['package'] == 'packed':
            print(f"Object : {new_object['object']}, Object_ID : {new_object['object_id']}, Package : {BCOLORS.WARNING}{new_object['package']}{BCOLORS.ENDC}")
        else:
            print(f"Object : {new_object['object']}, Object_ID : {new_object['object_id']}, Package : {BCOLORS.FAIL}{new_object['package']}{BCOLORS.ENDC}")


    def run(self):
        while True:
            try:
                self.generate_delivery()
            except requests.ConnectionError as e:
                print(e)
            time.sleep(1 * TIME_UNIT)


def run_factory_module():
    threads = list()

    main_thread = Thread(target=lambda: app.run(
        host='0.0.0.0', 
        port=8001))
    
    threads.append(main_thread)

    for i in range(1, THREADS + 1):
        factory = Factory(i)
        threads.append(factory)
    
    for i, thread in enumerate(threads):
        thread.start()

if __name__ == '__main__':
    run_factory_module();