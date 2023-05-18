import base64
import datetime
import json
import os
import sys
from contextlib import contextmanager
import logging
import concurrent.futures

logging.basicConfig(filename='log',level=logging.DEBUG,format='%(asctime)s:|:%(funcName)s:|:%(lineno)s:|:%(process)d:|:%(thread)d:|:%(threadName)s:||:%(message)s')

class initiator_class:

    key_size=int(8)

    def __init__(self,num_keys,file_path):
       self.seek=0
       self.producer_index=0
       self.consumer_index=0
       self.num_keys=num_keys
       self.buffer_unit=200
       self.file_path=file_path
       self.file_size=num_keys*8
       self.buffer=bytearray(102400)

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
                'overrider':0
            }
            self.seek+=initiator_class.key_size
            try:
                start_index=int((self.consumer_index*self.buffer_unit)%1024)
                end_index=start_index+self.buffer_unit
                self.buffer[start_index:end_index]=json.dumps(buffer_data).encode()
                # print(sys.getsizeof(json.dumps(buffer_data).encode()))
                print(f'p---{self.buffer[start_index:end_index].decode()}')
                self.producer_index+=1
            except Exception as e:
                logging.debug(e)
        sys.exit(0)

    def consumer(self):
        while(True):
            start_index=int((self.consumer_index*self.buffer_unit)%1024)
            end_index=start_index+self.buffer_unit
            data=self.buffer[start_index:end_index].decode()
            print(f'c---{data}')
            self.consumer_index+=1
    # def verifier(self):
    #     while(True):    
    #         print("verrifer logging")

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
    
if __name__=="__main__":
    num_keys=int(sys.argv[1])
    file_path="./key_list"
    new_process=initiator_class(num_keys,file_path)
    new_process.run()
    print('-'*25)
    
