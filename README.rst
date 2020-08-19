================
**Anywheredoor**
================

.. image:: https://github.com/iayanpahwa/anywheredoor/blob/master/assets/logo.JPG


**AnywhereDoor** is a cross platform clipboard sharing utility written in Python.

**************
**Motivation**
**************

I felt the need of a cross platform clipboard sharing utility, while working on a project, requiring me to frequently switch between my OSX machine (for development), windows (for official communication) and single board linux computer like raspberry pi (for testing and deployments). 

I found a few solutions but most of them requires user to sign-up for a cloud service and send clipboard data on their private cloud which I am not very comfortable with, specially from the fact that I intuitively copy all kinds of things to my clipboard, hence I developed anywheredoor, it's server runs on your local network making it secure and flexible for your needs. 

Anywheredoor uses `MQTT protocol <http://mqtt.org>`_ which is usually meant for light weight IoT applications but it is equally effective for this utility. Thanks to it's Pub-Sub design any number of workstations can be easily added into the clipboard sharing network making it highly scaleable yet light weight on network bandwidth.

You can host any free and open source MQTT brokers(servers) like `mosquito <https://mosquitto.org/download/>`_ on any one of your home workstation or VPS platform such as Linux, windows, OSX, Raspberry Pi or even inside a `Docker Container <https://hub.docker.com/_/eclipse-mosquitto>`_ on any host with docker engine. 

The clipboard payloads are end-to-end encrypted using light weight yet effective `Fernet <https://asecuritysite.com/encryption/fernet>`_ based symmetrical key cryptography, so if anyone on local network tries to sniff the packets they cannot read your clipboard data, and even the MQTT Broker cannot see the actual payload making it "OK" to be used with free MQTT brokers available as sandboxes in public domain (Though not recommended).

**************
**Working**
**************

The applications when running, monitor changes in system's clipboard every few seconds (default = 1s) and if there is a new content on your clipboard it encrypts that and publishes it using MQTT protocol on a topic(defined in config file) to a MQTT broker. The other workstations (also subscribers) where this application is running receives the payload from the broker, decrypts it and copies it to the clipboard of the machine it's running and the user can then paste it whenever and wherever needed. Since it directly monitors the clipboard all traditional methods of copy and paste works including keyboard shortcuts across all platforms.

**Tested with Python 3.8 running on :**

- MAC OSX Catalina

- Ubuntu 20.04 

- Raspberry Pi 4 with Raspberry Pi OS

- Windows 10 (sketchy)

Since the publisher and subscriber are two different applications using a common library, it is possible to implement one way ot both way clipboard sharing based on user's needs.

**************
**Installation**
**************

Anywheredoor based on python 3.8 (officially tested version), in it's core uses `pyperclip <https://pypi.org/project/pyperclip/>`_ python module to monitor clipboard activity, which in turn uses OS native clipboard managers:

- Windows (built-in)
- Mac OSX (pcopy-pbpaste which are also built-in)
- Linux (external clipboard managers such as xclip or xsel)

**Step 1:**

If using on Windows or OSX no needs for the below step but if using linux install following using your package manager, for Debian based systems like ubuntu (you can download both), in your terminal execute::

    sudo apt install xclip

or::

    sudo apt install xsel 
    
**Step 2:**

For communicating with all the machines anywheredoor using MQTT protocol which requires MQTT Broker(server) to be hosted. Now you are free to use any publicly available brokers but for the sake of extra security it is highly recommended to downloaded and host a free open source broker on your local network. 

Technically the broker can be hosted on any compatible machine on your local network and can run silently in background or inside Docker Container (with port 1883 forwarded). For the sake of this guide let's install a free open source MQTT Broker known as Mosquitto on Debian based Linux machine, execute in your terminal :

**sudo apt install mosquitto**

This will install the mosquito broker and run it in background, listening to MQTT clients on port 1883 (default), you can change the broker configuration using it's config file. Alternatively you can run mosquitto in a docker container as well.

**step 3:**

Next clone this repository and install python dependencies using pip::
    
    cd anywheredoor/
    pip3 install -r requirements.txt

**Step 4:**

Next, create a new encryption key by execute following script::

    cd utils
    python3 generate-key.py

**Step 5:**

Next we need to configure the app, edit the config file anywherdoor/anywheredoor.conf using any text editor and change following parameters:

 - Change **BROKER** to hostname or IP address of broker to the workstation where you installed the MQTT broker

 - Change default **ENCRYPTION_KEY** the one you generate in step 4 

 - Change location of **LOG_FILE** to desired location
 
 - Optionally you can also change the default **TOPIC** to any string which is basically like the location where MQTT Broker publishes and clients subscribes to. Change it to a same unique string across all your machines running anywheredoor.

and save the config file after doing above changes

**Step 6:** 

Launch clipboard publisher by executing::

    python3 anywheredoor/anywheredoor_pub.py --config anywheredoor.conf

**Step 7:**

Execute clipboard subscriber by executing following in new terminal session::

    python3 anywheredoor/anywheredoor_sub.py --config anywheredoor.conf

Repeat step 5-7 on all your machines and keep them running until you want to sync all the clipboards

**************
**Future Plans / To-Dos**
**************

Please Note: Currently it's not very processor optimized because of always running background tasks and polling loops. 

- Optimize subscriber (Highest Priority)
- Implement clipboard sharing for images as well since currently only text is supported (Low priority/Maybe)
- Package the project for easy installation and deployment (High Priority)
- Implement GUI application (Require contributors)
- Create systems service for linux (Low Priority)
- Create app for android and possibly for iOS as well (Require contributors)
- Add MQTT username-password based optional authentication for extra security (low priority)

**************
**Common Gotchyas**
**************

- Make sure all the workstations are using same MQTT broker and can access it wherever it is running.
- Make sure all workstations running anywheredoor pub-sub on same MQTT topic (see config file).
- Make sure all workstations running anywheredoor uses same encryption key (see config file).
- To debug you can increase the default log level (see config file).
- If broker dies the application will wait and tries to reconnect to it every few seconds.
- xclip sometimes seems to not work with wayland .

**************
**Contributors**
**************

To contribute to anywheredoor, create an issue for the same, fork the repo, create a new branch for feature or bug fix and send a pull request. Read the `CONTRIBUTING.md <https://github.com/iayanpahwa/anywhereDoor/blob/master/CONTRIBUTING.md>`_ before sending your PRs. All sorts of contribution ranging from documentation to bug fixes to new features are welcome. 

**************
**License**
**************

Anywheredoor is licensed under MIT License. Refer to the LICENSE file for more information.

**************
**Credits**
**************

Project art has been created and contributed by `Nikhil Kumar a.k.a Mason <https://github.com/nk521>`_
