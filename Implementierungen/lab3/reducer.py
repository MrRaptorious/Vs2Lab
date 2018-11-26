import zmq
import time
import const
import sys
import pickle

class Reducer:
    def __init__(self,id):
        self.me = id
        prt = const.PORTREDUCER1 if id == '1' else const.PORTREDUCER2
        self.context = zmq.Context()
        self.receiver = self.context.socket(zmq.PULL)
        self.recAddress = "tcp://" + const.SRC + ":" + prt
        self.receiver.bind(self.recAddress)
        self.wordcountDict = {}
    
    def run(self):
        while True:
            workload = pickle.loads(self.receiver.recv())
            print("Reducer{} received workload \'{}\' from Mapper{}".format(self.me, workload[1], workload[0]))
            word = workload[1]
            if word in self.wordcountDict:
                self.wordcountDict[word] += 1
                print("Word \'{}\' exists already. This word now exists {} times".format(word,self.wordcountDict[word]))
            else:
                self.wordcountDict[word] = 1
                print("New word \'{}\' added to wordcountDict".format(word))
        pass
    
reducer = Reducer(str(sys.argv[1]))
reducer.run()