#!/usr/bin/python
import time
from geometry_msgs.msg import Twist
import rospy
import random
import math
from turtlesim.srv import *
from std_srvs.srv import *
from wk1_assignment_6.msg import *
from wk1_assignment_6.srv import *
from turtlesim.msg import Pose


def click_clear():
    service_name = '/clear'
    client = rospy.ServiceProxy(service_name, Empty)
    client.wait_for_service()
    client.call(EmptyRequest())
    client.close()

def click_reset():
    service_name = '/reset'
    client = rospy.ServiceProxy(service_name, Empty)
    client.wait_for_service()
    client.call(EmptyRequest())
    client.close()

def click_spawn(turtle):
    service_name = '/spawn'
    client = rospy.ServiceProxy(service_name, Spawn)
    client.wait_for_service()
    x = turtle.x
    y = turtle.y
    theta = turtle.theta
    name = turtle.name
    request = SpawnRequest()
    request.x = x
    request.y = y
    request.theta = theta
    request.name = name
    client.call(request)
    client.close()

def click_kill(name):
    service_name = '/kill'
    client = rospy.ServiceProxy(service_name,Kill)
    client.wait_for_service()
    request = KillRequest()
    request.name = name
    client.call(request)
    client.close()

def click_pen(turtle,pen):
    name = turtle.name
    r = pen.r
    g = pen.g
    b = pen.b
    width = pen.width
    off = 0
    service_name = '/{}/set_pen'.format(name)
    client = rospy.ServiceProxy(service_name, SetPen)
    client.wait_for_service()
    request = SetPenRequest()
    request.r = r
    request.g = g
    request.b = b
    request.width = width
    request.off = off
    client.call(request)
    client.close()

def click_absolute(turtle_a,turtle_b):
    name = turtle_a.name
    x = turtle_b.x
    y = turtle_b.y
    theta = turtle_b.theta
    service_name = '/{}/teleport_absolute'.format(name)
    client = rospy.ServiceProxy(service_name, TeleportAbsolute)
    client.wait_for_service()
    request = TeleportAbsoluteRequest()
    request.x = x
    request.y = y
    request.theta = theta
    client.call(request)
    client.close()

def mov2goal(turtle):
    service_name = 'PID_Server'
    rospy.wait_for_service(service_name)
    PID = rospy.ServiceProxy(service_name,ServicePID)
    ans  = PID(turtle.x,turtle.y,0.1,turtle.name)
    return ans

def follow2goal(leader,follower,tolerance):
    service_name = 'PID_follow'
    rospy.wait_for_service(service_name)
    PID = rospy.ServiceProxy(service_name,FollowPID)
    ans  = PID(leader,follower,tolerance)
    return ans

