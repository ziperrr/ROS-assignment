#!/usr/bin/python
import time
from geometry_msgs.msg import Twist
import rospy
import random
import math
from turtlesim.srv import *
from std_srvs.srv import *
from wk1_assignment_6.msg import *
from turtlesim.msg import Pose

from TurtleService import *




followerA =0
followerB =0
finish =0
can_do =0
turtle_leader = Turtle()
turtle_leader.x =5.5
turtle_leader.y =5.5
turtle_leader.name ="leader"
turtle_leader.theta = random.uniform(0,math.pi *2)
leader_pen = Pen()
leader_pen.r =255
leader_pen.g =0
leader_pen.b =0
leader_pen.width=2
pub_control_leader=rospy.Publisher("/leader/cmd_vel",Twist,queue_size=10)
pub_leader_to_f   =rospy.Publisher("/leader/for_followers",LeaderMessage6,queue_size=10)
end_control_leader=rospy.Publisher("/leader/end",End,queue_size=10)

def ok_callback(data):
    print("ok_callback")
    global followerA
    global followerB
    global finish
    global pub_control_leader
    global pub_leader_to_f
    global turtle_leader
    global leader_pen
    global can_do
    if data.message[0] == 'a':
        followerA =1
    elif data.message[0] =='b':
        followerB =1

def pos_callback(data):
    global followerA
    global followerB
    global finish
    global pub_control_leader
    global pub_leader_to_f
    global turtle_leader
    global leader_pen
    global can_do
    global end_control_leader
    #print("pos_callback")
    if can_do == 1:
	
	
	
        #print(str(data.x) +" "+ str(data.y))
        vel_msg = Twist()
        vel_msg.linear.x=1.0
        vel_msg.linear.y=0.0
        vel_msg.linear.z=0.0
        vel_msg.angular.x =0.0
        vel_msg.angular.y =0.0
        vel_msg.angular.z =0.0
        pub_control_leader.publish(vel_msg)
	end_control_leader.publish(End(False))
	
	#fa_c.publish(vel_msg)
	#fb_c.publish(vel_msg)
        turtle_leader.x = data.x
        turtle_leader.y = data.y
        '''message_f1 = LeaderMessage6()
        message_f2 = LeaderMessage6()
        message_f1.instructionID =0
        message_f2.instructionID =0
        message_f1.message = "f1:"+str(turtle_leader.x + math.cos(turtle_leader.theta))+":"+str(turtle_leader.y + math.sin(turtle_leader.theta))
        message_f2.message = "f2:"+str(turtle_leader.x + 2*math.cos(turtle_leader.theta))+":"+str(turtle_leader.y + 2*math.sin(turtle_leader.theta))
        pub_leader_to_f.publish(message_f1)
        pub_leader_to_f.publish(message_f2)'''
        if data.x <=0 or data.y <=0 or data.x >=11 or data.y >=11:
	    print("finish")

	    end_control_leader.publish(End(True))

            finish =1
	
	
    

def run():
    global followerA
    global followerB
    global finish
    global pub_control_leader
    global pub_leader_to_f
    global turtle_leader
    global leader_pen
    global can_do
    message_f1 = LeaderMessage6()
    message_f2 = LeaderMessage6()
    message_f1.instructionID =0
    message_f2.instructionID =0
    message_f1.message = "f1:"+str(turtle_leader.x + math.cos(turtle_leader.theta))+":"+str(turtle_leader.y + math.sin(turtle_leader.theta))
    message_f2.message = "f2:"+str(turtle_leader.x + 2*math.cos(turtle_leader.theta))+":"+str(turtle_leader.y + 2*math.sin(turtle_leader.theta))
    while followerA ==0 or followerB ==0:
	pub_leader_to_f.publish(message_f1)
        pub_leader_to_f.publish(message_f2)
        rate.sleep()
	rate.sleep()
	rate.sleep()
	rate.sleep()
    tmp = Turtle()
    tmp.name ="tmp"
    tmp.x  =5.5
    tmp.y  =5.5
    tmp.theta = random.uniform(0,math.pi *2)
    #click_absolute(turtle_leader,tmp)
    click_pen(Turtle(name='leader'),Pen(255,0,0,2))
    tmp.name ="followerA"
    tmp.x    =turtle_leader.x + math.cos(turtle_leader.theta)
    tmp.y    =turtle_leader.y + math.sin(turtle_leader.theta)
    click_absolute(tmp,tmp)
    tmp.name ="followerB"
    tmp.x    =turtle_leader.x + 2*math.cos(turtle_leader.theta)
    tmp.y    =turtle_leader.y + 2*math.sin(turtle_leader.theta)
    click_absolute(tmp,tmp)
    can_do =1


if __name__ =="__main__":
    rospy.init_node("leader")
    rate = rospy.Rate(10)
    click_kill("turtle1")
    click_spawn(turtle_leader)
    click_pen(turtle_leader,leader_pen)
    rospy.Subscriber("/leader/pose",Pose,pos_callback)
    fa_c=rospy.Publisher("/followerA/cmd_vel",Twist,queue_size=10)
    fb_c=rospy.Publisher("/followerB/cmd_vel",Twist,queue_size=10)
    a= rospy.Subscriber("/follower/ready",LeaderMessage6,ok_callback)
    print(a)
    run()
    while True:
        if finish ==1:
	    can_do =0
            finish =0
	    print("123")
	    end_control_leader.publish(End(True))
  	    message_f1 = LeaderMessage6()
    	    message_f2 = LeaderMessage6()
    	    message_f1.instructionID =1
    	    pub_leader_to_f.publish(message_f1)
	    
	    vel_msg = Twist()
            vel_msg.linear.x=0.0
            vel_msg.linear.y=0.0
            vel_msg.linear.z=0.0
            vel_msg.angular.x =0.0
            vel_msg.angular.y =0.0
            vel_msg.angular.z =0.0
            pub_control_leader.publish(vel_msg)
	    fa_c.publish(vel_msg)
	    fb_c.publish(vel_msg)
	    turtle_leader.x =5.5
	    turtle_leader.y =5.5
	    turtle_leader.theta = random.uniform(0,math.pi *2)
	    #click_absolute(turtle_leader,turtle_leader)
	    click_pen(Turtle(name='leader'),Pen(0,0,0,2))
	    
	    Turtle_init_msg=Turtle(5.5,5.5,0,'leader')
	    print(Turtle_init_msg)
    	    mov2goal(Turtle_init_msg)
	    click_clear()
	    followerA =0
    	    followerB =0
	    
	    
	    run()
