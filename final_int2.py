import base64
import os
import sys
from contextlib import contextmanager
import multiprocessing
import logging
import signal

logging.basicConfig(filename='log',level=logging.DEBUG,format='%(asctime)s:|:%(funcName)s:|:%(lineno)s:|:%(process)d:|:%(thread)d:|:%(threadName)s:||:%(message)s')

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
    
    def open_file(self,mode,action):
        try:
            with open(self.file_path,mode) as file:
                if int(action)==1:
                    file.seek(self.seek)
                    data=file.read(self.key_size)
                    encoded_data = base64.b64encode(data).decode('utf-8')
                    print(f'P--{encoded_data}')
                    try:
                        self.buffer.extend(data)
                    except OSError as os1:
                        logging.debug(os1)
                elif int(action)==2:
                    for i in range(num_keys):
                        key=os.urandom(initiator_class.key_size)
                        encoded_data = base64.b64encode(key).decode('utf-8')
                        print(f'G--{encoded_data}')
                        file.write(key)
        except IOError as i:
            logging.debug(f'io---{i}')
        except Exception as e:
            logging.debug(f'e---{e}')

    def generator(self,prod_pid=None):
        self.file_path=file_path
        self.open_file('wb','2')
        
    def provider(self,signum, frame,cons_pid=None):
    #    while self.seek<self.file_size:
        self.open_file('rb','1')
        self.seek+=initiator_class.key_size

    def consumer(self,verf_pid=None):
            print("consumer logging consumer")

    def verifier(self,prod_pid=None):
        print("verrifer logging")

    def run(self):
        self.generator(self.verf_pid)
        gene_pid=os.getpid()
        verifier_process=multiprocessing.Process(target=self.consumer,args=[self.prod_pid])
        verifier_process.start()
        self.verf_pid=verifier_process.pid
        consumer_process=multiprocessing.Process(target=self.consumer,args=[self.verf_pid])
        consumer_process.start()
        self.cons_pid=consumer_process.pid
        producer_process=multiprocessing.Process(target=self.provider,args=[self.cons_pid])
        producer_process.start()
        self.prod_pid=producer_process.pid

        logging.debug(f'{gene_pid},{self.verf_pid},{self.cons_pid},{self.prod_pid}')

        signal.signal(signal.SIGUSR1,self.verifier)
        signal.signal(signal.SIGUSR1, self.consumer)
        signal.signal(signal.SIGUSR1, self.provider
        )

        initiator_class.signal_sender(self.prod_pid,signal.SIGUSR1)

    @classmethod
    def signal_sender(cls,pid,signal_number):
        msg=f'{pid},{signal_number}'
        logging.debug(msg)
        os.kill(pid,signal_number)


    @classmethod
    def change_keysize(self,size)->None:
        self.key_size=size


    

if __name__=="__main__":
    num_keys=int(sys.argv[1])
    file_path="./key_list"
    new_process=initiator_class(num_keys,file_path)
    new_process.run()
    print('-'*20)
    # new_process.provider()


