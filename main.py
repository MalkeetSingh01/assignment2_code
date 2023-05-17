import base64
import os
import queue
import sys
from contextlib import contextmanager
import multiprocessing
import logging

logging.basicConfig(filename='log',level=logging.DEBUG,format='%(asctime)s:|:%(funcName)s:|:%(lineno)s:|:%(process)d:|:%(thread)d:|:%(threadName)s:||:%(message)s')

# @contextmanager
# def custom_sender():
#     try:
#     except:
#     finally:




class initiator_class:

    key_size=int(8)
    # buffer = queue.Queue()
    buffer=bytearray(1024)

    # encoders=['i','i','H','f','d','c']

    def __init__(self,num_keys,file_path):
    #  self.file_mode='r'
       self.seek=0
       self.num_keys=num_keys
       self.file_path=file_path
    #  self.file=open(file_path,initiator_class.file_mode)

    def open_file(self,mode,action):
        try:
            with open(self.file_path,mode) as file:
                if int(action)==1:
                    data=file.read(8)
                    encoded_data = base64.b64encode(data).decode('utf-8')
                    print(encoded_data)
                    try:
                        initiator_class.buffer.put(encoded_data) 
                    except OSError as os1:
                        logging.debug(os1)
                elif int(action)==2:
                    for i in range(num_keys):
                        key=os.urandom(initiator_class.key_size)
                        encoded_data = str(base64.b64encode(key).decode('utf-8'))
                        print(encoded_data)
                        file.write(key)
        except IOError as i:
            logging.debug(i)
        except Exception as e :
            logging.debug(e) 


    def generator(self):
        self.file_path=file_path
        # print(sys.getsizeof(key))
        # print(sys.getsizeof(str(key)))
        self.open_file('wb','2')
        # try:
        #     with open(self.file_path,'wb') as file:
        #         for i in range(num_keys):
        #             key=os.urandom(initiator_class.key_size)
        #             file.write(key)
        # except IOError as i:
        #     logging.error(i)
        # except Exception as e :
        #     logging.error(e)
            # encoded_data = str(base64.b64encode(key).decode('utf-8'))
            # print(encoded_data)
            # self.file.write(encoded_data)
    
    def provider(self):#shared memory segmwnts
        self.seek+=initiator_class.key_size
        self.file.seek=self.seek
        self.open_file('r','1')
        # try:
        #     with open(self.file_path,'r') as file:
        #         data=file.read(8)
        #         encoded_data = base64.b64encode(data).decode('utf-8')
        #         print(encoded_data)
        #         try:
        #             initiator_class.buffer.put(encoded_data) 
        #         except OSError as os:
        #             logging.warning(os)
        # except IOError as i:
        #     logging.error(i)
        # except Exception as e :
        #     logging.error(e) 

    def consumer():
        print("logging consumer")

    # def verifier():
    @classmethod
    def run(cls):
       producer_process=multiprocessing.Process(target=cls.provider)
       consumer_process=multiprocessing.Process(target=cls.consumer)


    @classmethod
    def change_keysize(self,size)->None:
        self.key_size=size


    def signal_sender(pid,signal_number):
        os.kill(pid,signal_number)

if __name__=="__main__":
    num_keys=int(sys.argv[1])
    file_path="./key_list"
    new_process=initiator_class(num_keys,file_path)
    # new_process.open_file_mode('wb')
    new_process.generator()
    # new_process.open_file_mode('rb')
    # new_process.provider()
    # for i in range(num_keys):
    #     new_process.provider()
    
