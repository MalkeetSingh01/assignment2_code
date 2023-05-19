import base64
import datetime
import json
import os
import signal
import sys
from contextlib import contextmanager
import logging
import concurrent.futures
import time
from multiprocessing import Pipe

logging.basicConfig(filename='log',level=logging.DEBUG,format='%(asctime)s:|:%(funcName)s:|:%(lineno)s:|:%(process)d:|:%(thread)d:|:%(threadName)s:||:%(message)s')

class initiator_class:

    key_size=int(8)

    producer_index=0
    consumer_index=0
    
    def __init__(self,num_keys,file_path):
       self.seek=0
       self.num_keys=num_keys
       self.buffer_unit=200
       self.file_path=file_path
       self.file_size=num_keys*8
       self.buffer=bytearray(1024)
       signal.signal(signal.SIGUSR1, self.run)

    @classmethod
    def change_keysize(self,size)->None:
        self.key_size=size
    
    @classmethod
    def signal_sender(cls,pid,signal_number):
        msg=f'{pid},{signal_number}'
        logging.debug(msg)
        os.kill(pid,signal_number)

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

    def generator(self):
        self.file_path=file_path
        self.open_file('wb','2')
        # logging.debug(self.__dict__)
        
    def producer(self):
        while(self.seek<self.file_size):  
            data=self.open_file('rb','1')
            timestamp = datetime.datetime.now()
            buffer_data={
                'data':data,
                'timestamp':timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                'seek_value':self.seek,
                'overrider':0,
                "index_producer":initiator_class.producer_index
            }
            self.seek+=initiator_class.key_size
            try:
                start_index=initiator_class.producer_index*self.buffer_unit
                start_index = 0 if start_index+self.buffer_unit > 1024 else start_index
                end_index=start_index+self.buffer_unit
                json_string = self.buffer[start_index:end_index].decode()
                print(json_string)
                # if(json_string!=None):random_data=json.loads(json_string)
                # print(type(random_data))
                random1=0
                if(random1!=None):
                    print(start_index,end_index)
                    self.buffer[start_index:end_index]=json.dumps(buffer_data).encode()
                    # print(sys.getsizeof(json.dumps(buffer_data).encode()))
                    print(f'p---{self.buffer[start_index:end_index].decode()}--')
                    initiator_class.producer_index+=1
                    print(initiator_class.consumer_index," ",initiator_class.producer_index)
                    time.sleep(1)
            except Exception as e:
                logging.debug(e)
        sys.exit(0)

    def consumer(self):
        while(True):
            if(initiator_class.consumer_index<initiator_class.producer_index):
                start_index=initiator_class.consumer_index*self.buffer_unit
                start_index = [0 if start_index > 1024 else start_index]
                end_index=start_index+self.buffer_unit
                data=self.buffer[start_index:end_index].decode()
                data['overrider']=1
                self.buffer[start_index:end_index]=json.dumps(data).encode()
                print(f'c---{data}')              
                initiator_class.consumer_index+=1
            # time.sleep(1)


    def verifier(self):
        # while(True):    
        #     print("verrifer logging")
        pass
        

    def run(self):
        self.generator()
        with concurrent.futures.ProcessPoolExecutor() as executor:
            future1 = executor.submit(self.producer)
            future2 = executor.submit(self.consumer)
            # future3 = executor.submit(self.verifier)
            # result = future1.result() 
            if future1.done():
                print("future1 done")
                print(new_process.buffer[0:1024].decode())
            if future2.done():
                print("future12 done")
    

if __name__=="__main__":
    num_keys=int(sys.argv[1])
    file_path="./key_list"
    new_process=initiator_class(num_keys,file_path)
    new_process.run()
    print('-'*25)
    
