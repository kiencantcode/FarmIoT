import sys
from Adafruit_IO import MQTTClient
import os
from dotenv import *
dotenv = DotEnv() 


class Adafruit_MQTT:
    AIO_FEED_IDs_sub = ["data"]
    AIO_USERNAME = dotenv.get("AIO_USERNAME")
    AIO_KEY = dotenv.get("AIO_KEY")
    recvCallBack = None
    client = None

    def setRecvCallBack(self,func):
        self.recvCallBack = func

    def connected(self, client):
        print("Connected ...")
        for feed in self.AIO_FEED_IDs_sub:
            self.client.subscribe(feed)

    def subscribe(self, client , userdata , mid , granted_qos):
        print("Subscribeb to",self.AIO_FEED_IDs_sub[mid-1])

    def publish(self,topic,value):
        self.client.publish(topic,value)
        print("Publish to",topic,":",value)

    def disconnected(self, client):
        print("Disconnected...")
        sys.exit (1)

    def message(self, client , feed_id , payload):
        self.recvCallBack(feed_id, payload)

    def __init__(self):
        self.client = MQTTClient(self.AIO_USERNAME , self.AIO_KEY)
        self.client.on_connect = self.connected
        self.client.on_disconnect = self.disconnected
        self.client.on_message = self.message
        self.client.on_subscribe = self.subscribe
        self.client.connect()
        self.client.loop_background()