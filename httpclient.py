#!/usr/bin/env python
# coding: utf-8
# Copyright 2015 Morgan Patzelt
# Based on code by Abram Hindle (2013)
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it
import string
import sys
import socket
import urllib
from urlparse import urlparse



def help():
    print "httpclient.py [GET/POST] [URL]\n"

# the HTTPRequest object contains the code and body of the server response
class HTTPRequest(object):
    def __init__(self, code, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):

    # connects the client to the server
    def connect(self, host, port):
        # use sockets!
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as msg:
            print ("Failed to create socket")
            print ("Error Code: " + str(msg[0]) + ", Error Message: " + str(msg[1]))
            sys.exit()
        print ("Socket created successfully")  
        
        try:
            parse = urlparse(host)
            remote_ip = parse.netloc
            remote_ip = string.split(remote_ip, ":", 1)[0]
        
        except urlparse.error:
            print("Host name could not be resolved")
            sys.exit()
        
        try:
            s.connect((remote_ip, port)) # need both brackets
            print ("Socket connected to " + host + " on IP " + remote_ip) 
        except socket.error as msg:
            print ("Failed to connect")
            print ("Error Code: " + str(msg[0]) + ", Error Message: " + str(msg[1]))
            sys.exit()
            
        return s
        
    # gets the host name from the url and returns it
    def get_host(self, url):
        words = string.split(url, "/")
        host = words[2]
        return host
    
    # gets the path from the url and returns it
    def get_path(self, url):
        words = string.split(url, "/")
        path = ""
        for x in range (3, len(words)):
            path = path + "/" + words[x]
        return path
    
    # creates the request line for the HTTP request and returns it
    def get_requestline(self, method, url):
        requestline = "%s %s HTTP/1.1\r\n" % (method, self.get_path(url))
        return requestline
    
    # adds a header to the list of headers
    def add_header(self, key, value):
        self.headers[key] = value
    
    # returns the list of headers
    def get_headers(self):
        return self.headers
    
    # prints headers in the correct format "Key: Value"
    def print_header(self, key, value):
        return "%s: %s\r\n" % (key, value)    
    
    # prints an empty line to indicate the end of headers
    def end_headers(self):
        return "\r\n"
    
    # prints the body of the POST requests with the arguments
    # the arguments are encoded
    def get_POSTbody(self, args):
        body = urllib.urlencode(args)
        return body
    
    # gets the code from the server response
    def get_code(self, data):
        words = data.split()
        code = words[1]
        return int(code)
    
    # gets the body from the server repsonse
    def get_body(self, data):
        words = data.split("\r\n\r\n")
        body = words[1]
        return body
    
    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    # performs a GET request
    # returns the HTTPRequest Object
    def GET(self, url, args=None):
        code = 500
        body = ""
        host = url
        base = string.split(url, "/")[2]
        try: 
            # retrieves the port number, if given
            port = int(string.split(base, ":")[1])
        except:
            # else port 80 is used
            port = 80
        try:
            # connects to socket
            sock = self.connect(host, port) 
            print "Connected"
        except:
            print "Not Connected"
            sys.exit()
        
        # get params for HTTP request message
        requestline = self.get_requestline("GET", host)
        self.headers = {}
        self.add_header("Host", self.get_host(url))
        headers = self.get_headers()
        
        message = requestline
        for key in headers:
            message = message + self.print_header(key, headers[key])
        message = message + self.end_headers()
        
        # sends the message to the server
        try:
            sock.sendall(message.encode("UTF8"))
        except socket.error:
            print("Send failed")
            sys.exit()
        print("Message sent successfully")  
        
        # receives response from server
        data = self.recvall(sock)
        print data
        
        # gets information from the response
        code = self.get_code(data)
        body = self.get_body(data)
            
        return HTTPRequest(code, body)      

    # performs a POST request
    # returns the HTTPRequest Object
    def POST(self, url, args=None):
        code = 500
        body = ""
        host = url
        base = string.split(url, "/")[2]
        try: 
            # retrieves the port number, if given
            port = int(string.split(base, ":")[1])
        except:
            # else port 80 is used
            port = 80        
        
        # connects to socket
        try:
            sock = self.connect(host, port) 
            print "Connected"
        except:
            print "Not Connected"
            sys.exit()
        
        # gets params for request message
        requestline = self.get_requestline("POST", host)
        self.headers = {}
        self.add_header("Host", self.get_host(url))
        if args:
            self.add_header("Content-Type", "application/x-www-form-urlencoded")
            self.add_header("Content-Length", len(self.get_POSTbody(args)))
            body = self.get_POSTbody(args)
        
        headers = self.get_headers()
        
        message = requestline
        for key in headers:
            message = message + self.print_header(key, headers[key])
        message = message + self.end_headers()
        if args:
            message = message + body
        
        # sends the request message
        try:
            sock.sendall(message.encode("UTF8"))
        except socket.error:
            print("Send failed")
            sys.exit()
        print("Message sent successfully")  
        
        # receives the response message
        data = self.recvall(sock)
        print data
        
        
        # gets information from response messasge
        code = self.get_code(data)
        body = self.get_body(data)
            
        return HTTPRequest(code, body)


    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            print "POST"
            return self.POST( url, args )
        else:
            print "GET"
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[1], sys.argv[2] )
    else:
        print client.command( command, sys.argv[1] )    
