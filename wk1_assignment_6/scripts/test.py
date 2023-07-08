#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import *
from std_srvs.srv import Empty
from wk1_assignment_6.srv import ServicePID
import random

x,y,theta=0,0,0

def init_turtle():
    
    
    
    rospy.wait_for_service('/kill')
    try:
	kill=rospy.ServiceProxy('kill',Kill)
    except rospy.ServiceException:
	rospy.loginfo("fail")
    kill('turtle1')
    create_turtle('hunter')
    create_turtle('runner',x,y)
    try:
        rospy.wait_for_service('/hunter/set_pen')
        try:
	    setpen=rospy.ServiceProxy('/hunter/set_pen',SetPen)
        except rospy.ServiceException:
	    rospy.loginfo("fail")
        setpen(231,15,37,2,0)
    except rospy.ServiceException:
	rospy.loginfo("set pen fail")


def clear():
    
    global x,y,theta
    rospy.wait_for_service("/hunter/teleport_absolute")
    try:
       	tele=rospy.ServiceProxy("/hunter/teleport_absolute",TeleportAbsolute)
	    
    except rospy.ServiceException as e:
        rospy.loginfo("Service call failed: %s"%e)
    tele(5.5,5.5,0)

    rospy.wait_for_service("/runner/teleport_absolute")
    try:
       	tele=rospy.ServiceProxy("/runner/teleport_absolute",TeleportAbsolute)
	    
    except rospy.ServiceException as e:
        rospy.loginfo("Service call failed: %s"%e)
    x,y=random.uniform(0,11),random.uniform(0,11)
    tele(x,y,0)

    
    rospy.wait_for_service("/clear")
    try:
       	clear=rospy.ServiceProxy("/clear",Empty)
	    
    except rospy.ServiceException as e:
        rospy.loginfo("Service call failed: %s"%e)
    clear()

def create_turtle(name,x=5.5,y=5.5):

    """
    rospy.wait_for_service('/spawn')
    try:
	spawn=rospy.ServiceProxy('/spawn',Spawn)
    except rospy.ServiceException as identifier:
        rospy.loginfo("fail")
    spawn(2.0,2.0,0,'runner')
    
    """
    client = rospy.ServiceProxy("/spawn",Spawn)
    client.wait_for_service()
    req = SpawnRequest()
    req.x = x
    req.y = y
    req.theta = 0
    req.name = name
    try:
        response = client.call(req)
        rospy.loginfo("s :%s",response.name)
    except rospy.ServiceException as identifier:
        rospy.loginfo("fail")
if __name__=="__main__":
    rospy.init_node('control')
    init_turtle()
    
	
    
    while True:
	clear()
        rospy.wait_for_service('/PID_Server')
	
        try:
	    PID=rospy.ServiceProxy('/PID_Server',ServicePID)
        except rospy.ServiceException as identifier:
            rospy.loginfo("fail")
        PID(x,y,0.5,'hunter')
	rospy.loginfo('Service End')
	
    
    
    
