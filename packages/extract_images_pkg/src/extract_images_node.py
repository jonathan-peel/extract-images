#!/usr/bin/env python3

import os
import rospy
from duckietown.dtros import DTROS, NodeType
from std_msgs.msg import String
import cv2
from sensor_msgs.msg import CompressedImage
import numpy as np

class MyPublisherNode(DTROS):

    def __init__(self, node_name):
        # initialize the DTROS parent class
        super(MyPublisherNode, self).__init__(node_name=node_name, node_type=NodeType.GENERIC)
        # construct publisher
        self.pub = rospy.Publisher('chatter', String, queue_size=10)

    def run(self):
        # publish message every 0.5 second
        rate = rospy.Rate(2) # 2Hz
        # set cap to continuously capture images from the camera
        cap = cv2.VideoCapture(2)

        while not rospy.is_shutdown():
            ret, frame = cap.read()
            msg = CompressedImage()
            msg.format = "jpeg"
            msg.data = np.array(cv2.imencode('.jpg', frame)[1]).tostring()
            rospy.loginfo("Publishing message: '%s'" % message)
            self.pub.publish(msg)
            rate.sleep()

if __name__ == '__main__':
    # create the node
    node = MyPublisherNode(node_name='extract_images_node')
    # run node
    node.run()
    # keep spinning
    rospy.spin()