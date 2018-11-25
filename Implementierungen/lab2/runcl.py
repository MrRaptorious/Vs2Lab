import rpc
from context import lab_logging
import time
lab_logging.setup()

cl = rpc.Client()
cl.run()

base_list = rpc.DBList({'foo'})
callrequest = cl.append('bar', base_list)
if(callrequest):
    print("OK received")
    result = []
    asyncrecieve = rpc.AsyncMessageRec(cl,result)
    asyncrecieve.start()
    while result == []: 
        print("Pretending doing other stuff for 3 seconds and then check if result returned.")
        time.sleep(3)
        
    print("Result: {}".format(result[0].value))
else :
    print("No OK from Server received!")
    
cl.stop()
