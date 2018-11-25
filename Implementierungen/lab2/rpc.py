import constRPC
import threading
import rpc
import rpyc
from context import lab_channel
import time

class DBList:
    def __init__(self, basic_list):
        self.value = list(basic_list)

    def append(self, data):
        self.value = self.value + [data]
        return self

class AsyncMessageRec(threading.Thread):
    def __init__(self, cl, result):
        threading.Thread.__init__(self)
        self.cl = cl
        self.result = result
        
    def run(self):
        msgrcv = self.cl.chan.receive_from(self.cl.server)
        self.result.append(msgrcv[1])
        return msgrcv[1]
    
class Client():
    def __init__(self):
        self.chan = lab_channel.Channel()
        self.client = self.chan.join('client')
        self.server = None

    def run(self):
        self.chan.bind(self.client)
        self.server = self.chan.subgroup('server')
    def stop(self):
        self.chan.leave('client')

    def append(self, data, db_list):
        assert isinstance(db_list, DBList)
        msglst = (constRPC.APPEND, data, db_list)  # message payload
        self.chan.send_to(self.server, msglst)  # send msg to server
        print("Sent rpc-\"append\" to server. Waiting for a response from server.")
        msgrcv = self.chan.receive_from(self.server)  # wait for response
        return msgrcv[1][0] == constRPC.OK  #return msgrcv[1]  # pass it to caller


class Server:
    def __init__(self):
        self.chan = lab_channel.Channel()
        self.server = self.chan.join('server')
        self.timeout = 3

    @staticmethod
    def append(data, db_list):
        assert isinstance(db_list, DBList)  # - Make sure we have a list
        return db_list.append(data)

    def run(self):
        self.chan.bind(self.server)
        while True:
            print("Wait for request")
            msgreq = self.chan.receive_from_any(self.timeout)  # wait for any request
            if msgreq is not None:
                client = msgreq[0]  # see who is the caller
                msgrpc = msgreq[1]  # fetch call & parameters
                if constRPC.APPEND == msgrpc[0]:  # check what is being requested
                    print("Received rpc-\"append\". Wait 3 sec before sending OK to Client.")
                    time.sleep(3)
                    self.chan.send_to({client},[constRPC.OK])
                    print("Pretend to work hard for 10 seconds.")
                    time.sleep(10)  # pretend to work
                    result = self.append(msgrpc[1], msgrpc[2])  # do local call
                    print("Send result back to Client.")
                    self.chan.send_to({client}, result)  # return response
                else:
                    pass  # unsupported request, simply ignore
