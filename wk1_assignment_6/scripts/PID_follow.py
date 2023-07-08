#!/usr/bin/env python
# coding=utf-8

import rospy
from wk1_assignment_6.srv import *
from wk1_assignment_6.msg import *
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import *
from math import pow, atan2, sqrt, pi
import random



class Turtle_Controller:

    def __init__(self,leader,follower,tolerance):
        # Creates a node with name 'turtlebot_controller' and make sure it is a
        # unique node (using anonymous=True).
        

        # Publisher which will publish to the topic '/hunter/cmd_vel'.
        self.velocity_publisher_self = rospy.Publisher('/'+follower+'/cmd_vel',
                                                  Twist, queue_size=10)
	"""
	self.pose_publisher_self = rospy.Publisher('/hunter/pose',
                                                  Pose, queue_size=10)
	self.pose_publisher_runner = rospy.Publisher('/runner/pose',
                                                  Pose, queue_size=10)
	"""

        # A subscriber to the topic '/hunter/pose'. self.update_pose is called
        # when a message of type Pose is received.
        self.pose_subscriber_self = rospy.Subscriber('/'+follower+'/pose',
                                                Pose, self.update_pose_self)
	self.pose_subscriber_runner = rospy.Subscriber('/'+leader+'/pose',Pose,self.update_pose_runner)

	self.end_pub=rospy.Publisher('/'+follower+'/end',
                                                  End, queue_size=1)
	self.end_sub=rospy.Subscriber('/'+leader+'/end',End,self.update_end)
        self.pose = Pose()
        self.rate = rospy.Rate(10)
	self.end=End(True)
	self.goal_pose=Pose()

    def update_pose_self(self, data):
        """Callback function which is called when a new message of type Pose is
        received by the subscriber."""
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)

    def update_pose_runner(self,data):
	self.goal_pose = data
	self.goal_pose.x = round(self.goal_pose.x, 4)
        self.goal_pose.y = round(self.goal_pose.y, 4)
    def update_end(self,data):
	self.end=data
	
	self.end_pub.publish(data)
    def euclidean_distance(self, goal_pose):
        """Euclidean distance between current pose and the goal."""
        return sqrt(pow((goal_pose.x - self.pose.x), 2) +
                    pow((goal_pose.y - self.pose.y), 2))

    def linear_vel(self, goal_pose, constant=1):
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

    def move2goal(self):
        """Moves the turtle to the goal."""
        
        # Please, insert a number slightly greater than 0 (e.g. 0.01).
        distance_tolerance = 0.5

        vel_msg_Turtle = Twist()

	start=rospy.Time.now()
	end=rospy.Time.now()
	self.goal_pose.x=random.uniform(0,11)
	self.goal_pose.y=random.uniform(0,11)
	print("follow to leader")
	
	
	while self.end.end==True:
	    continue
	while self.end.end==False:
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
                self.velocity_publisher_self.publish(vel_msg_Turtle)
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
		if self.end.end==True:
		    break
	
	
	print("follow end")
	
        # Stopping our robot after the movement is over.
        vel_msg_Turtle.linear.x = 0
        vel_msg_Turtle.angular.z = 0
        self.velocity_publisher_self.publish(vel_msg_Turtle)
	self.end_pub.publish(End(True))
	return True

	



def handle_PID_Control(request):
    
    control=Turtle_Controller(request.leader,request.follower,request.tolerance)
    ans=control.move2goal()
    return FollowPIDResponse(ans)

    
    
	

def PID_Control_server():
    rospy.init_node('PID_follow',anonymous=True)
    try:
	PID = rospy.Service("PID_follow",FollowPID,handle_PID_Control)
    except:
	rospy.loginfo("Service call failed\n")
    rospy.spin()
    

if __name__=="__main__":
    PID_Control_server()

    
