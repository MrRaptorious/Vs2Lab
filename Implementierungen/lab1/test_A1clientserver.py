'''
Created on Nov 7, 2018

@author: markus
'''
import unittest
import os
import time
import A1clientserver


class TestTelefonservice(unittest.TestCase):

    def setUp(self):
        pid = os.fork()
        if pid == 0 :
            server = A1clientserver.Telefonauskunft()
            server.serve()
            os._exit(0)
        time.sleep(.01)  # fork needs some time
        self.user = A1clientserver.Benutzerschnittstelle()
        
    def testGetall(self):
        data = self.user.call("getall")
        self.assertEqual(data, "jack 4098\nsape 4139\n")
        
    def testGet(self):
        data = self.user.call("get sape")
        self.assertEqual(data, "4139")
    
    def testNoEntry(self):
        data = self.user.call("get KeinEintrag!")
        self.assertEqual(data, "Kein Eintrag vorhanden!")

        
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
