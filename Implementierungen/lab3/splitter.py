import zmq
import time
import const
import pickle
class Splitter:
    def __init__(self, textfile):
        self.textfile = textfile
        self.context = zmq.Context()
        self.sender = self.context.socket(zmq.PUSH)
        self.address = "tcp://" + const.SRC + ":" + const.PORTSPLITTER
        self.sender.bind(self.address)
        
    def run(self):
        text = open(self.textfile,"r")
        allSentences = text.read().split(".")
        for i in range(len(allSentences)-1):
            print(str(i) + " " + allSentences[i])
            self.sender.send(pickle.dumps(("Splitter",allSentences[i])))
            
    def recSolution(self):
        
        pass
        
splitter = Splitter("mydata.txt")
print("Press Enter when the mappers are ready: ")
_ = input()
splitter.run()
splitter.recSolution()