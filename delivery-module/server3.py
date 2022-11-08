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
deposit = queue.Queue()

@app.route('/deposit', methods=['POST'])
def process_json():
    deposit.put(json.loads(request.data))
    return {'status_code': 200}

class Delivery(Thread):
    def __init__(self, delivery_id, *args, **kwargs):
        self.delivery_id = delivery_id
        super(Delivery, self).__init__(*args, **kwargs)

    def deliver(self):
        if deposit.empty():
            pass
        else:
            object = deposit.get()
            object['status'] = 'delivered'

            r = requests.post(
                url='http://aggregator:8002/aggregator/consumer',
                json=object
            )

            print(f"Object : {object['object']}, Object_ID : {object['object_id']}, Status : {BCOLORS.OKGREEN}{object['status']}{BCOLORS.ENDC}")


    def run(self):
        while True:
            try:
                self.deliver()
            except requests.ConnectionError:
                pass
            time.sleep(1)

def run_delivery_module():
    threads = list()

    main_thread = Thread(target=lambda: app.run(
        host='0.0.0.0', 
        port=8003))
    
    threads.append(main_thread)

    for i in range(1, THREADS + 1):
        delivery = Delivery(i)
        threads.append(delivery)
    
    for i, thread in enumerate(threads):
        thread.start()

if __name__ == '__main__':
    run_delivery_module()