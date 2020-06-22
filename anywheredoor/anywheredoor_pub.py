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
import pyperclip
import configparser
from time import sleep 
import anywheredoor as ad
from sys import exit
import paho.mqtt.client as mqtt


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
    logger_name = platform.system() + '_' + 'publisher'
    logger_name = ad.configureLogger(config, logger_name)
    
    client_pub = mqtt.Client()
    recent_value = ''
    
    try:
        while True:
            tmp_value = pyperclip.paste()  
            if tmp_value != recent_value:
                recent_value = tmp_value
                logger_name.info(f'Encrypting {recent_value}')
                encryptedPayload = ad.encryptPayload(cipher, recent_value)
                logger_name.info(f'publishing encrypted message: {encryptedPayload}')
                checkPublish = ad.publishPayload(config, client_pub, encryptedPayload)
                if checkPublish:
                    logger_name.info('Payload published successfully')
                else:
                    logger_name.critical('Connection to broker failed!!! \
                                         Check your connection and broker address !!!')

                sleep(int(config['DEFAULT']['WAIT']))
    except KeyboardInterrupt:
        logger_name.critical('Interrupt Received!! Exiting')

if __name__ == '__main__':
    main()    
