import base64
import datetime
import multiprocessing
import os
import signal
import sys
from contextlib import contextmanager
import logging
from multiprocessing import Manager,Lock
import time



logging.basicConfig(filename='log',level=logging.DEBUG,format='%(asctime)s:|:%(funcName)s:|:%(lineno)s:|:%(process)d:|:%(thread)d:|:%(threadName)s:||:%(message)s')

class CustomError(Exception):
    pass

class MyData:
    def __init__(self) -> None:
        self.value=[None]*10

class initiator_class:

    key_size=int(8)     

    def __init__(self,num_keys,file_path):
       self.seek=0
       self.num_keys=num_keys
       self.file_path=file_path
       self.file_size=num_keys*8
       signal.signal(signal.SIGUSR1, self.run)
       self.producer_index=0
       self.consumer_index=0
       self.verifier_index=0
       self.buffer_unit=125
       self.manager=Manager()
       self.shared_buffer=self.manager.dict()
       self.max_index=4
       self.lock = multiprocessing.Lock()

    @classmethod
    def change_keysize(self,size)->None:
        self.key_size=size
    
    @classmethod
    def signal_sender(cls,pid,signal_number):
        msg=f'{pid},{signal_number}'
        logging.debug(msg)
        os.kill(pid,signal_number)

    @classmethod
    def clear_files(cls):
        with open('decripted_keys','w') as f1:
            f1.truncate(0)
        with open('consumed_keys' ,'w') as f1:
            f1.truncate(0)

    @classmethod
    def raiseException(cls):
        corruption=os.urandom(initiator_class.key_size)
        corruption=base64.b64encode(corruption).decode('utf-8')
        return corruption

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
                        with open('decripted_keys','a') as f1:
                            f1.write(encoded_data)
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
        self.lock.acquire()
        try:
            self.shared_buffer[index]=data
        finally:
            self.lock.release()

    def get_data(self,index):
        data=self.shared_buffer.get(index)
        return data
        
    def producer(self):
        if(self.seek>self.file_size):exit(0)
        while(self.seek<self.file_size):  
            data=self.open_file('rb','1')
            timestamp = datetime.datetime.now()
            if(self.producer_index%4==0):
                data=initiator_class.raiseException()
                print("-"*30,"raised exception--",f'file_seek-{self.seek}')
            # time.sleep(2)
            self.producer_index=0 if self.producer_index >= self.max_index else self.producer_index
            buffer_data={
                'data':data,
                'timestamp':timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                'seek_value':self.seek,
                'overrider':False,
                'file_size':self.file_size,
                "index":self.producer_index,
            } 
            try:
                random=self.get_data(self.producer_index)
                # print(f'ran--{random}')
                if(random==None or random.get('overrider')==True):
                    # print(random)
                    print(f'p---{buffer_data}')
                    self.put_data(self.producer_index,buffer_data)
                    self.producer_index+=1
                    self.seek+=initiator_class.key_size
            except Exception as e:
                logging.debug(e)
        sys.exit(0)

    def consumer(self):
        c_int=0
        while(c_int<self.file_size):
            # time.sleep(1)
            self.consumer_index=0 if self.consumer_index >= self.max_index else self.consumer_index
            random=self.get_data(self.consumer_index)
            try:
                if(random!=None and random.get('overrider')!=True):
                    random['overrider']=True
                    c_int=int(random['seek_value'])+self.key_size+1
                    print(f'c---{random}')
                    self.put_data(self.consumer_index,random)
                    self.consumer_index+=1
                    self.verifier(random)
            except Exception as e:
                logging.debug(e)
        sys.exit(0)

    def verifier(self,random):
        print('-------verifier---------')
        try:
            with open(self.file_path,'r') as file:
                print('-------verifier_file_opener---------')
                file.seek(int(random.get('seek_value')))
                data=file.read(self.key_size)
                data=base64.b64encode(data).decode('utf-8')
                print(data)
                if(data!=random.get('data')): 
                    raise CustomError("Corrupted data")
                with open('./consumed_keys','a') as f:
                    f.write(random['data'])
        except CustomError as e:
            logging.debug(e,self.producer_index)
        

    def run(self):
        self.generator()
        proces_producer=multiprocessing.Process(target=self.producer)
        proces_consumer=multiprocessing.Process(target=self.consumer)

        proces_producer.start()
        proces_consumer.start()

        proces_producer.join()
        proces_consumer.join()

        print("Finally Done  :)")


if __name__=="__main__":
    num_keys=int(sys.argv[1])
    initiator_class.clear_files()
    file_path="./key_list"
    new_process=initiator_class(num_keys,file_path)
    try:
        new_process.run()
    except KeyboardInterrupt:
        print("KeyboardInterrup")
    except Exception as e:
        logging.debug(e)
    print('-'*25)
    
