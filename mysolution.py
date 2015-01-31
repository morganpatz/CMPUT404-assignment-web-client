import socket
import sys
import thread

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as msg:
    print ("Failed to create socket")
    print ("Error Code: " + str(msg[0]) + ", Error Message: " + str(msg[1]))
    sys.exit()
print ("Socket created successfully")
           
host = ''
port = 8880

try:
    s.bind((host, port))
except socket.error:
    msg = str(socket.error)
    print ("Bind Failed! Error code: " + str(msg[0]) + ", Error Message: " + str(msg[1]))
    sys.exit()
print ("Socket bind complete")
s.listen(10) # 10 = number of connections that can be in the queue
print ("Socket is now listening...")

while 1:
    # we wait for client to connect
    # this is a blocking call
    # the first client to connect gets the port
    conn, addr = s.accept()  
    
    # IP Address : Port Number
    print ("Connected with " + addr[0] + " : " + str(addr[1]))   
    # Start new thread
    thread.start_new_thread(handler, (conn, addr))




conn.close()
s.close()
