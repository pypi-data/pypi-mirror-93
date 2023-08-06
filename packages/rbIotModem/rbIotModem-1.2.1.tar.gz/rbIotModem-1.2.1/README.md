# **Ringbeller IoT - Python bindings**

![Python Logo](https://www.python.org/static/community_logos/python-logo.png "Sample inline image")

## **Prerequisites**

Requirements:  

1. [Raspberry Pi OS (Buster)](https://www.raspberrypi.org/software/operating-systems/)
2. Python3.9

### Install dependencies  

```bash
# Install SWIG and dependencies
$ sudo apt-get install -y swig python3.9 python3.9-dev
# Configure python and install dependencies
$ sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1
$ sudo update-alternatives --set python3 /usr/bin/python3.9
$ python3.9 -m pip install --user --upgrade pip setuptools wheel

# Install audio packages
$ sudo apt-get install -y libasound2-dev libsndfile1-dev
```  

## **Installation**

```bash
# Local installation
$ make install

# Installation via PyPI
$ pip3 install rbIotModem
```

## **Usage**  

```python
# Import modem library.
from rbIotModem import rbIotModem

# Instantiate modem library.
ec25 = rbIotModem.EC25()
```

## **API**  

This module exposes the following functions

 * `ec25.initialize(int verbose, bool debug, string serialPort, string audioDevice)`  
Set `verbose` logging level.  
Set `debug` simulation value.  
Set `serialPort` name.  
(Optional) Set input/output `audioDevice` name.  

 * `ec25.on()`  
Turns on and connects to the modem.  

 * `ec25.off()`  
Turns off modem.  

 * `ec25.restart()`  
Restarts modem.  

 * `ec25.connect()`  
Connects to the modem.  

 * `ec25.disconnect()`  
Disconnects from the modem.  

 * `ec25.configure()`  
Turns on modem.  
Connects to the modem.  
Configures modem.  

 * `ec25.sendSMS(string number, string message)`  
Sends an SMS containing `message` to `number`.

 * `ec25.receiveSMS()`  
Returns `sms` with unread SMS.

 * `ec25.placeVoiceCall(string number)`  
Places an outgoing voice call to `number`.  

 * `ec25.receiveVoiceCall()`  
Receives an incoming voice call.  

 * `ec25.getCallStatus()`  
Returns `True` when call is ongoing.  

 * `ec25.endCall()`  
Ends an active voice call.

 * `ec25.beginAudioPlayback(string playbackFile)`  
Plays `playbackFile` to the active voice call.   

 * `ec25.waitForAudioPlayback()`  
Waits until audio stops playing (blocking function).   

 * `ec25.endAudioPlayback()`  
Stops playing audio to the active voice call.   

 * `ec25.beginAudioRecording(string recordFile)`  
Records audio from the active voice call to `recordFile`.   

 * `ec25.endAudioRecording()`  
Stops recording audio from the active voice call.   

 * `ec25.sendMMS(MmsConfiguration mmsConfig, string recipient, string cc, string bcc, string title, string attachment)`  
Sets MMS configuration settings to `mmsConfig`.  
Sends an MMS with `title` and `attachment` to `recipient`, `cc` & `bcc`.

 * `ec25.getKeypadInput(int length, string audioFile)`  
(Optional) Plays `audioFile` to the active voice call.  
Returns keypad `input` of `length`.  
