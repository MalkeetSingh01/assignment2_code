import base64
import os
import queue
import sys


class initiator_class:

    key_size=int(8)
    buffer = queue.Queue()

    # encoders=['i','i','H','f','d','c']

    def __init__(self,num_keys,file_path):
    #  self.file_mode='r'
       self.seek=0
       self.num_keys=num_keys
       self.file_path=file_path
    #  self.file=open(file_path,initiator_class.file_mode)

    def generator(self):
        self.file_path=file_path
        # print(sys.getsizeof(key))
        # print(sys.getsizeof(str(key)))
        for i in range(num_keys):
            key=os.urandom(initiator_class.key_size)
            self.file.write(key)
            # encoded_data = str(base64.b64encode(key).decode('utf-8'))
            # print(encoded_data)
            # self.file.write(encoded_data)
    
    def provider(self):#shared memory segmwnts
        # self.seek+=initiator_class.key_size
        # self.file.seek=self.seek
        data=self.file.read(8)
        encoded_data = base64.b64encode(data).decode('utf-8')
        print(encoded_data)
        buffer.put(encoded_data) 
        

    # def consumer():

    # def verifier():

    def run():
        thread t1=

    def open_file_mode(self,mode):
        self.file=open(self.file_path,mode)
    

    @classmethod
    def change_keysize(self,size):
        self.key_size=size

if __name__=="__main__":
    num_keys=int(sys.argv[1])
    file_path="./key_list"
    new_process=initiator_class(num_keys,file_path)
    new_process.open_file_mode('wb')
    new_process.generator()
    new_process.open_file_mode('rb')
    new_process.provider()
    # for i in range(num_keys):
    #     new_process.provider()

