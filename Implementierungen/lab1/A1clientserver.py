import socket
import constCS
import logging
from lib import lab_logging
lab_logging.setup()

class Benutzerschnittstelle:
    logger = logging.getLogger("vs2lab.a1_Benutzerschnittstelle(Client)")
    
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((constCS.HOST, constCS.PORT))  # connect to server (block until accepted)
        self.logger.info("\nClient gebunden an Socket \n" + str(self.s) + "\n")

    def call(self, befehl):     #better use getCommand if you want to use it on a consol!
        while True:
            inputtext = befehl.split(" ")
            if inputtext[0] == "get":
                if len(inputtext) > 1:
                    self.s.send(inputtext[1].encode('utf-8'))
                    self.logger.info(inputtext[1] + " über " + str(self.s) + " geschickt!\n")
                    break
                print("Name angeben!/n")
            elif inputtext[0] == "getall":
                self.s.send(inputtext[0].encode('utf-8'))
                self.logger.info("\n\"" + inputtext[0] + "\"-über Socket\n" + str(self.s) + "\ngeschickt!\n")
                break
            else:
                befehl = input("get NAME oder getall benutzen! \n")
            
        data = self.s.recv(1024)  # receive the response
        self.logger.info("\n\"" + str(data) + "\"" + " als Antwort erhalten!\n")
        print(data.decode('utf-8'))  # print the result
        self.s.close()  # close the connection
        self.logger.info("\nBenutzerschnittstelle(Client)-Socket geschlossen.\n")
        return data.decode('utf-8')
    
    def getCommand(self):
        self.call(input("Funktion wählen: \n"))
        
    
class Telefonauskunft:
    tel = {'jack': 4098, 'sape': 4139}
    logger = logging.getLogger("vs2lab.a1_Telefonauskunft(Server)")
    
    def __init__(self):        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((constCS.HOST, constCS.PORT))
        self.logger.info("\nTelefonauskunft gebunden an Socket\n" + str(self.s) + "\n")    
    
    def serve(self):
        self.s.listen(1)
        (connection, address) = self.s.accept()  # returns new socket and address of client
        while True:  # forever
            data = connection.recv(1024)  # receive data from client
            self.logger.info("\n\"" + str(data) + "\"-Nachricht erhalten! \n")
            if data.decode('utf-8') == "getall":
                data = ""
                for k, v in self.tel.items():
                    data = data + k +" " + str(self.tel[k]) + "\n"
            elif data.decode("utf-8") in self.tel:
                data = self.tel[data.decode('utf-8')]
            else:
                data = ("Kein Eintrag vorhanden!")
            if not data:
                break  # stop if client stopped
            self.logger.info("\n\"" + str(str(data).encode('utf-8')) + "\" antwort zum Client(" + str(connection) + ").\n")
            connection.send(str(data).encode('utf-8'))
            break
        connection.close()  # close the connection
        self.logger.info("\nServer Socket geschlossen.\n")
        return data
    
    def shutmedown(self):
        self.s.close()        