import zmq
import time
import const
import pickle
import sys
import string

class Mapper:
    def __init__(self,id):
        self.me = id
        self.context = zmq.Context()
        self.receiver = self.context.socket(zmq.PULL)
        self.recAddress = "tcp://" + const.SRC + ":" + const.PORTSPLITTER
        self.receiver.connect(self.recAddress)
        self.sender1 = self.context.socket(zmq.PUSH)
        self.sender2 = self.context.socket(zmq.PUSH)
        self.reducerAddress1 = "tcp://" + const.SRC + ":" + const.PORTREDUCER1
        self.reducerAddress2 = "tcp://" + const.SRC + ":" + const.PORTREDUCER2
        self.sender1.connect(self.reducerAddress1)
        self.sender2.connect(self.reducerAddress2)
        
    def run(self):
        while True:
            workload = pickle.loads(self.receiver.recv())
            print("Mapper{} received workload {} from {}".format(self.me, workload[1], workload[0]))
            sentence = workload[1]
            sentence = sentence.replace(",","") #remove all comma
            sentence = sentence.lower()         #all letters to lowercase
            wordlist = sentence.split(" ")         #split every word
            wordlist = list(filter(None, wordlist)) #remove empty list entrys because some sentences start wit a whitspace
            for word in wordlist:
                if(string.ascii_lowercase.index(word[0]) <= string.ascii_lowercase.index('m')):
                    print("Send word \'{}\' to Reducer 1".format(word))
                    self.sender1.send(pickle.dumps((self.me, word)))
                else:
                    print("Send word \'{}\' to Reducer 2".format(word))
                    self.sender2.send(pickle.dumps((self.me, word)))
                    
        

mapper = Mapper(str(sys.argv[1]))
mapper.run()