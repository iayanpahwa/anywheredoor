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


import platform
import configparser
from time import sleep
import anywheredoor as ad
from sys import exit
import paho.mqtt.client as mqtt

# Callback function for successful connection to broker 
def on_connect(client_sub, obj, flags, rc):
    if rc==0:         # Subscribe to the topic
        client_sub.subscribe(obj['conifgFile']['DEFAULT']['TOPIC'])
    else:
        return rc

# Callback function when disconnect to broker 
def on_disconnect(client_sub, obj, rc):
    if rc != 0:
        obj['logger'].critical('Unexpected disconnected from broker.\
                                attempting auto-reconnect')

# Callback function for successful subscribe to the topic 
def on_subscribe(client_sub, obj, mid, granted_qos):
    obj['logger'].info('Listening to incoming payloads')    

# Callback function for successful reception of new payload
def on_message(client_sub, obj, msg):
    obj['logger'].info(f'New payload received = {msg.payload}')
    obj['logger'].info(f'Deciphering Payload = {msg.payload}')
    decoded_message = ad.decryptPayload(obj['encKey'], msg.payload)
    isCopy = ad.copytoClipboard(decoded_message)
    if isCopy:
        obj['logger'].info(f'Copied {decoded_message} to clipboard')
    else:
        obj['logger'].critical(f'Failed to clipboard')

def main():
    numExpectedArguments = 3
    arguments = ad.setArgParser(numExpectedArguments)
    if not arguments:
        print('Please provide config file using --config option')
        exit(1)
    else:
        if arguments.config:
            configFile = arguments.config
            
            if ad.checkConfigFile(configFile):
                config = configparser.ConfigParser()
                config.read(configFile) 
            else:
                print('Config file not found or not readable, please refer docs')
                exit(2)

    cipher = ad.checkEncryptionKey(bytes(config['DEFAULT']['ENCRYPTION_KEY'], 'utf-8'))
    if not cipher:
        print('INVALID EXCRYPTION KEY!! Please generate key as per the documentation')
        exit(3)

    # Set Logger
    logger_name = platform.system() + '_' + 'subscriber'
    logger_name = ad.configureLogger(config, logger_name)

    # objects to pass to callback functions 
    objects = {'conifgFile': config, 'encKey': cipher, 'logger': logger_name}

    client_sub = mqtt.Client(userdata=objects)
    client_sub.on_message = on_message
    client_sub.on_connect = on_connect
    client_sub.on_subscribe = on_subscribe
    client_sub.on_disconnect = on_disconnect

    # Retry until connected
    try:
        isConnected = client_sub.connect(config['DEFAULT']['BROKER'], 
                                    int(config['DEFAULT']['PORT']), 
                                    int(config['DEFAULT']['KEEP_ALIVE']))
    except ConnectionRefusedError:
        print('Broker refused the connection, Exiting')
        logger_name.critical('Broker refused the connection, Exiting')
        exit(4)

    while isConnected:   
        logger_name.critical('Attempting connection')
        sleep(int(config['DEFAULT']['WAIT']))
    
    logger_name.info('Successfully connected to broker')
    client_sub.loop_start()

    try:
        while True:
            sleep(int(config['DEFAULT']['WAIT']))
            
    except  KeyboardInterrupt:
        logger_name.critical('Interrupt Received!! Exiting')
        client_sub.disconnect()
        
if __name__ == '__main__':
    main()