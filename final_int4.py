import base64
import datetime
import json
import multiprocessing
import os
import signal
import sys
from contextlib import contextmanager
import logging
import concurrent.futures
import time
from multiprocessing import Array,Value



logging.basicConfig(filename='log',level=logging.DEBUG,format='%(asctime)s:|:%(funcName)s:|:%(lineno)s:|:%(process)d:|:%(thread)d:|:%(threadName)s:||:%(message)s')

class MyData:
    def __init__(self) -> None:
        for i in range(10):
            self[i]=None

class initiator_class:

    key_size=int(8)
    
    def __init__(self,num_keys,file_path):
       self.seek=0
       self.num_keys=num_keys
       self.file_path=file_path
       self.file_size=num_keys*8
       signal.signal(signal.SIGUSR1, self.run)
       self.shared_buffer = Array('c', 1024)
       self.producer_index=0
       self.consumer_index=0
       self.verifier_index=0
       self.buffer_unit=125
       self.max_index=10
       self.shared_buffer=Value(MyData)

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

    def put_data(self,index, data):
        print(data,sys.getsizeof(json.dumps(data)))
        start_index = index*self.buffer_unit
        end_index = start_index +self.buffer_unit
        self.shared_buffer[start_index:end_index] = json.dumps(data).encode()
        print("put----",self.shared_buffer[start_index:end_index])

    def get_data(self,index):
        start_index = index *self.buffer_unit
        end_index = start_index +self.buffer_unit
        data = self.shared_buffer[start_index:end_index]
        print(data.decode())
        return data.decode()
        
    def producer(self):
        print('---producer---')
        while(self.seek<self.file_size):  
            data=self.open_file('rb','1')
            timestamp = datetime.datetime.now()
            buffer_data={
                'data':data,
                'timestamp':timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                # 'seek_value':self.seek,
                'overrider':0,
                # "index_producer":self.producer_index
            }
            # print(json.dumps(buffer_data).encode()," ",json.dumps(buffer_data)," ",sys.getsizeof(json.dumps(buffer_data).encode()))
            time.sleep(1)
            self.seek+=initiator_class.key_size
            random=self.get_data(self.producer_index)
            print(f'p---{random}',sys.getsizeof(random),type(random))
            try:
                self.producer_index=0 if self.producer_index*self.buffer_unit+ self.buffer_unit>1024 else self.producer_index
                self.put_data(self.producer_index,buffer_data)
                self.producer_index+=1
            except Exception as e:
                logging.debug(e)
        sys.exit(0)

    def consumer(self):
        print('---consumer---')
        time.sleep(1)
        while(True):
            random=json.loads(self.get_data(self.consumer_index))
            print(random," ",json.dumps(buffer_data)," ",sys.getsizeof(random))
            try:
                if(random!=None or int(random['overrider'])==0):
                    random['overrider']=1
                    print(f'c---{random}')
                    self.consumer_index=0 if self.consumer_index*self.buffer_unit+ self.buffer_unit>1024 else self.consumer_index
                    self.put_data(self.consumer_index,random)
                    self.consumer_index+=1
                    with open('./consumed_keys','w') as f:
                        f.write(random['data'])
            except Exception as e:
                logging.debug(e)


    def verifier(self):
        pass
        

    def run(self):
        self.generator()
        proces_producer=multiprocessing.Process(target=self.producer)
        # proces_consumer=multiprocessing.Process(target=self.consumer)

        proces_producer.start()
        proces_consumer.start()

        proces_producer.join()
        # proces_consumer.join()



if __name__=="__main__":
    num_keys=int(sys.argv[1])
    file_path="./key_list"
    new_process=initiator_class(num_keys,file_path)
    try:
        new_process.run()
    except Exception as e:
        logging.debug(e)
    print('-'*25)
    
