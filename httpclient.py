#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
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

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib
from urlparse import urlparse
import string
from StringIO import StringIO

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPRequest(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body
    

        

class HTTPClient(object):
    #def get_host_port(self,url):

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
            #remote_ip = socket.gethostbyname(host)
            parse = urlparse(host)
            remote_ip = parse.netloc
            remote_ip = string.split(remote_ip, ":", 1)[0]
            print "Remote IP: " + remote_ip
        
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
        
    def get_host(self, url):
        words = string.split(url, "/")
        host = words[2]
        return host
            
    def get_path(self, url):
        words = string.split(url, "/")
        path = ""
        for x in range (3, len(words)):
            path = path + "/" + words[x]
        return path

    def print_requestline(self, method, url):
        requestline = "%s %s HTTP/1.1\r\n" % (method, self.get_path(url))
        return requestline
    
    def print_header(self, key, value):
        header = "%s: %s\r\n" % (key, value)
        return header
    
    def end_headers(self):
        return "\r\n"
    
        
    def get_body(self, method, url):
        body = self.print_requestline(method, url) + self.print_header("Host", self.get_host(url)) + self.end_headers()
        print body
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

    def GET(self, url, args=None):
        code = 500
        body = ""
        host = url
        base = string.split(url, "/")[2]
        port = int(string.split(base, ":")[1])
        try:
            self.connect(host, port) 
            print "Connected"
            code = 200
        except:
            code = 404
            print "Not Found"
            print "Did Not Connect"
        
        body = self.get_body("GET", host)
            
        return HTTPRequest(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        host = url
        base = string.split(url, "/")[2]
        port = int(string.split(base, ":")[1])

        try:
            self.connect(host, port) 
            "Connected"
            code = 200
        except:
            code = 404
            print "Not Connected"
        
        body = self.get_body("POST", host)
            
        return HTTPRequest(code, body)

    # gets called first
    # tests to see if it is a POST or GET request
    # calls .POST or .GET respectively
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
