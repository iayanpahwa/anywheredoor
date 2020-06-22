# -----------------------------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2020 Ayan Pahwa 
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# Author : Ayan Pahwa <codensolder@gmail.com>
# -----------------------------------------------------------------------------------------

import logging
import argparse
import pyperclip
from sys import argv
from time import sleep
from cryptography.fernet import Fernet

def setArgParser(numArgs):
    '''
    Set command line arguments:
    numArgs is the number of expected arguments
    '''
    if len(argv) < numArgs:
        args = False
    else:
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                            help='Cross Platform clipboard sharing utility')
        parser.add_argument('-c', '--config', help='Use config file')
        args = parser.parse_args()
    return args

def checkConfigFile(configFile):
    '''
    Verify config file is present and is readable:
    configFile is filename present in the filesystem 
    '''
    try:
        f = open(configFile, mode="r")
        f.close()
    except IOError:
        return False
    else:
        return True

def checkEncryptionKey(key):
    '''
    Verify encryption key validity:
    key is the encryption key used
    '''
    try:
        checkKeyAuthenticity = Fernet(key)
    except:
        return False
    else:
        return checkKeyAuthenticity

def configureLogger(configFile, loggerName):
    '''
    Set logger to log different events happen during program lifecycle:
    configFile is file where log file location is present, 
    loggerName is name of the logger to be used
    '''
    loggerName = logging.getLogger(loggerName)
    loggerName.setLevel(int(configFile['DEFAULT']['LOG_LEVEL']))
    formatter = logging.Formatter('%(name)s:%(levelname)s:%(asctime)s:%(message)s')    
    file_handler = logging.FileHandler(configFile['DEFAULT']['LOG_FILE'])
    file_handler.setFormatter(formatter)
    loggerName.addHandler(file_handler)
    return loggerName

def encryptPayload(cipher, payload):
    '''
    Encrypt clipboard payloads using Fernet:
    cipher is the encryption key, 
    payload is string message to be encrypted
    '''
    message = str.encode(payload) 
    encrypted_message = cipher.encrypt(message)
    out_message = encrypted_message.decode()   # Encryption exception 
    return out_message

def decryptPayload(cipher, payload):
    '''
    Decrypt payloads using Fernet:
    cipher is the encryption key, 
    payload is string message to be encrypted
    '''
    decrypted_message = cipher.decrypt(payload)   
    return str(decrypted_message.decode("utf-8"))

def publishPayload(configFile, client, payload):
    '''
    Publish the payload using MQTT protocol:
    configFile is file where broker details are present, 
    client is MQTT client instance, 
    payload is string message to be published
    '''
    try:
        client.connect(configFile['DEFAULT']['BROKER'], 
                        int(configFile['DEFAULT']['PORT']), 
                        int(configFile['DEFAULT']['KEEP_ALIVE']))
    except:
        return False
    else:
        client.loop_start()       
        client.publish(configFile['DEFAULT']['TOPIC'], payload)
        sleep(0.2)
        client.disconnect() 
        client.loop_stop()
        return True

def copytoClipboard(payload):
    '''
    Copy to the os clipboard:
    payload is string or URL to be copied
    '''
    try:
        pyperclip.copy(payload)
    except:
        return False
    else:
        return True

def generateNewKey():
    '''
    Generate New Excryption Key in utf-8 format to be used within config file
    '''
    return Fernet.generate_key().decode("utf-8")
