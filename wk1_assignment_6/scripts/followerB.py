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
from TurtleService import *


finish =0
ft  =1
sd =0
turtle_followerA = Turtle()
turtle_followerA.x =random.uniform(0,11)
turtle_followerA.y =random.uniform(0,11)
turtle_followerA.name ="followerB"
turtle_followerA.theta = random.uniform(0,math.pi *2)
followerA_pen = Pen()
followerA_pen.r =255
followerA_pen.g =255
followerA_pen.b =255
followerA_pen.width=2
#pub_control_fa	=rospy.Publisher("followerB/cmd_vel",Twist,queue_size=10)
pub_fa_to_leader    =rospy.Publisher("/follower/ready",LeaderMessage6,queue_size=10)
follow_start=End(True)
def end_callback(data):
    global follow_start
    
    follow_start=data
    
rospy.Subscriber("/leader/end",End,end_callback)

def leader_callback(data):
	global pub_control_fa
        global pub_fa_to_leader
	global finish
	global ft
	global turtle_followerA
	global followerA_pen
	global sd
	global follow_start
	if data.instructionID ==1:
	    finish=1
	elif data.instructionID ==0 and data.message.split(':')[0] =="f2" and sd ==0:
	    sd=1
	    tmp = Turtle()
 	    tmp.x =float(data.message.split(':')[1])
	    tmp.y =float(data.message.split(':')[2])
	    tmp.name = "followerB"
	    print("followerB " +str(tmp.x)+" "+str(tmp.y))
	    ret = mov2goal(tmp)
	    
	    
	    if ft >=1:
	   	print("b follow")	
	        ft -=1
		message_a = LeaderMessage6()
		message_a.message="b"
	        message_a.instructionID =0
		pub_fa_to_leader.publish(message_a)
	    while follow_start.end==True:
		
		
		continue
	    ret = follow2goal('followerA','followerB',0.5)
	    
	    
	    	

	

if __name__ =="__main__":
    rospy.init_node("followerB")
    rate = rospy.Rate(10)
    click_spawn(turtle_followerA)
    click_pen(turtle_followerA,followerA_pen)
    rospy.Subscriber("/leader/for_followers",LeaderMessage6,leader_callback)
    while True:
	
        if finish ==1:
            finish =0
	    ft   =1
	    sd   =0
	    click_absolute(turtle_followerA,turtle_followerA)
	    
