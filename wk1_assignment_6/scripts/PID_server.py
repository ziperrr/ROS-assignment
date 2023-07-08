#!/usr/bin/env python
# coding=utf-8

import rospy
from wk1_assignment_6.srv import *
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import *
from math import pow, atan2, sqrt, pi
import random



class Turtle_Controller:
    def __init__(self,name,x,y,tolerance):
	self.pose=Pose()
	self.goal_pose=Pose()
	self.goal_pose.x=x
	self.goal_pose.y=y
	self.tolerance=tolerance
	self.turtle_name=name
	self.rate = rospy.Rate(10)
	


	self.vel_pub=rospy.Publisher('/'+self.turtle_name+'/cmd_vel',Twist,queue_size=10)
	self.pose_sub=rospy.Subscriber('/'+self.turtle_name+'/pose',Pose,self.update_pose)
	



    def euclidean_distance(self, goal_pose):
        """Euclidean distance between current pose and the goal."""
        return sqrt(pow((goal_pose.x - self.pose.x), 2) +
                    pow((goal_pose.y - self.pose.y), 2))

    def linear_vel(self, goal_pose, constant=1.5):
        """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
        return constant * self.euclidean_distance(goal_pose)

    def steering_angle(self, goal_pose):
        """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
        return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)

    def angular_vel(self, goal_pose, constant=6):
        """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
	pose_theta=self.pose.theta
	
	theta= (self.steering_angle(goal_pose) - pose_theta)
	if theta>pi:
	    theta=theta-pi*2
	elif theta<-pi:
	    theta=pi*2+theta
        return constant*theta
	
	#return constant * (self.steering_angle(goal_pose) - self.pose.theta)

    def update_pose(self,data):
	self.pose.x=data.x
	self.pose.y=data.y
	self.pose.theta=data.theta
	

    def move2goal(self):
	rospy.loginfo('move to goal\n')
	# Please, insert a number slightly greater than 0 (e.g. 0.01).
        distance_tolerance = self.tolerance

        vel_msg_Turtle = Twist()

	start=rospy.Time.now()
	end=rospy.Time.now()
	rospy.loginfo('PID_server start working\n')
        while self.euclidean_distance(self.goal_pose) >= distance_tolerance:
	    
            # Porportional controller.
            # https://en.wikipedia.org/wiki/Proportional_control

            # Linear velocity in the x-axis.
            vel_msg_Turtle.linear.x = self.linear_vel(self.goal_pose)
            vel_msg_Turtle.linear.y = 0
            vel_msg_Turtle.linear.z = 0
	    

            # Angular velocity in the z-axis.
            vel_msg_Turtle.angular.x = 0
            vel_msg_Turtle.angular.y = 0
            vel_msg_Turtle.angular.z = self.angular_vel(self.goal_pose)
	    #rospy.loginfo("angular speed:"+str(vel_msg_Turtle.angular.z)+"\n")
	    #rospy.loginfo("theta:"+str(self.pose.theta)+"\n")

            # Publishing our vel_msg_Turtle
            self.vel_pub.publish(vel_msg_Turtle)
	    """
	    self.pose_publisher_self.publish(self.pose)
	    self.pose_publisher_runner.publish(self.goal_pose)
	    """
	    
            # Publish at the desired rate.
            self.rate.sleep()
	    end=rospy.Time.now()
	    if end.secs-start.secs>=30:
		return False
		break
	#if not end.secs-start.secs>=30: 
	    
	# Waiting for 5s and the game restart 
	
	#    start=rospy.Time.now()
	
	# while end.secs-start.secs<5:
	#    end=rospy.Time.now()
	
        # Stopping our robot after the movement is over.
        vel_msg_Turtle.linear.x = 0
        vel_msg_Turtle.angular.z = 0
        self.vel_pub.publish(vel_msg_Turtle)
	return True
	



def handle_PID_Control(request):
    turtle_name=request.turtle_name
    control=Turtle_Controller(turtle_name,request.x,request.y,request.tolerance)
    ans=control.move2goal()
    return ServicePIDResponse(ans)

    
    
	

def PID_Control_server():
    rospy.init_node('PID_Server')
    try:
	PID = rospy.Service("PID_Server",ServicePID,handle_PID_Control)
    except:
	rospy.loginfo("Service call failed\n")
    rospy.spin()
    

if __name__=="__main__":
    PID_Control_server()

    
    
