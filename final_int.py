import base64
import os
import queue
import sys
from contextlib import contextmanager
import multiprocessing
import logging

logging.basicConfig(filename='log',level=logging.DEBUG,format='%(asctime)s:|:%(funcName)s:|:%(lineno)s:|:%(process)d:|:%(thread)d:|:%(threadName)s:||:%(message)s')

class initiator_class:

    key_size=int(8)
    buffer=bytearray(1024)

    def __init__(self,num_keys,file_path):
       self.seek=0
       self.num_keys=num_keys
       self.file_path=file_path
       self.file_size=num_keys*8
    
    def open_file(self,mode,action):
        try:
            with open(self.file_path,mode) as file:
                if int(action)==1:
                    file.seek(self.seek)
                    data=file.read(self.key_size)
                    encoded_data = base64.b64encode(data).decode('utf-8')
                    print(f'P--{encoded_data}')
                    try:
                        initiator_class.buffer.append(data)
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
    def generator(self):
        self.file_path=file_path
        self.open_file('wb','2')
        
    def provider(self):#shared memory segmwnts
       while self.seek<self.file_size:
            self.open_file('rb','1')
            self.seek+=initiator_class.key_size

    def consumer():
            print("logging consumer")

    @classmethod
    def run(cls):
        producer_process=multiprocessing.Process(target=cls.provider)
        consumer_process=multiprocessing.Process(target=cls.consumer)


    @classmethod
    def change_keysize(self,size)->None:
        self.key_size=size


    

if __name__=="__main__":
    num_keys=int(sys.argv[1])
    file_path="./key_list"
    new_process=initiator_class(num_keys,file_path)
    new_process.generator()
    print('-'*20)
    new_process.provider()


