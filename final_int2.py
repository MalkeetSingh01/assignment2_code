import base64
import datetime
import os
import sys
from contextlib import contextmanager
import multiprocessing
import logging
import signal
import time

logging.basicConfig(filename='log',level=logging.DEBUG,format='%(asctime)s:|:%(funcName)s:|:%(lineno)s:|:%(process)d:|:%(thread)d:|:%(threadName)s:||:%(message)s')


class context_manager:

    process_table={
        "producer":None,
        "consumer":None,
        "verifier":None
    }

    def __init__(self,process_name,process_id) -> None:
       self.process_table[process_name]=process_id 
    
    def worker_function(self,signum,next_process_id):
        pass

class initiator_class:

    key_size=int(8)

    def __init__(self,num_keys,file_path):
       self.seek=0
       self.num_keys=num_keys
       self.file_path=file_path
       self.file_size=num_keys*8
       self.verf_pid=None
       self.cons_pid=None
       self.prod_pid=None
       self.buffer=bytearray(1024)
    
    # @classmethod
    def signal_sender(self,pid,signal_number):
        msg=f'{pid},{signal_number}'
        logging.debug(msg)
        os.kill(pid,signal_number)


    @classmethod
    def change_keysize(self,size)->None:
        self.key_size=size


    def open_file(self,mode,action):
        try:
            with open(self.file_path,mode) as file:
                if int(action)==1:
                    file.seek(self.seek)
                    data=file.read(self.key_size)
                    encoded_data = base64.b64encode(data).decode('utf-8')
                    return encoded_data
                elif int(action)==2:
                    for i in range(num_keys):
                        key=os.urandom(initiator_class.key_size)
                        encoded_data = base64.b64encode(key).decode('utf-8')
                        print(f'Gen--{encoded_data}')
                        file.write(key)
        except IOError as i:
            logging.debug(f'io---{i}')
        except Exception as e:
            logging.debug(f'e---{e}')

    def generator(self,prod_pid=None):
        self.file_path=file_path
        self.open_file('wb','2')
        
    def producer(self,signum,cons_pid=None):
    #    while self.seek<self.file_size:
        if self.seek==self.file_size:
            sys.exit(0)
        data=self.open_file('rb','1')
        print(f'Pi--{data}')
        timestamp = datetime.datetime.now()
        buffer_data={
            'data':data,
            'timestamp':timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            'seek_value':self.seek
        }
        try:
            self.buffer.extend(buffer_data)
        except OSError as os1:
            logging.debug(os1)
        self.seek+=initiator_class.key_size

        self.signal_sender(self.cons_pid,signal.SIGUSR1)

    def consumer(self,signum,verf_pid=None):
            print("consumer logging",signum)

    def verifier(self,signum,prod_pid=None):
        print("verrifer logging",signum)

    def run(self):
        self.generator(self.verf_pid)
        gene_pid=os.getpid()
        consumer_process=multiprocessing.Process(target=self.consumer,args=[self.verf_pid])
        producer_process=multiprocessing.Process(target=self.producer,args=[self.cons_pid])
        verifier_process=multiprocessing.Process(target=self.verifier,args=[self.cons_pid])
        producer_process.start()
        consumer_process.start()
        verifier_process.start()
        self.prod_pid=producer_process.pid
        self.cons_pid=consumer_process.pid
        self.verf_pid=verifier_process.pid

        logging.debug(f'{gene_pid},{self.cons_pid},{self.prod_pid}')

        signal.signal(signal.SIGUSR1, self.consumer)
        signal.signal(signal.SIGUSR2, self.producer)
        signal.signal(signal.SIGUSR1, self.verifier)

        # initiator_class.signal_sender(self.prod_pid,signal.SIGUSR1)

        producer_process.join()
        consumer_process.join()



    

if __name__=="__main__":
    num_keys=int(sys.argv[1])
    file_path="./key_list"
    new_process=initiator_class(num_keys,file_path)
    new_process.run()
    print('-'*25)


