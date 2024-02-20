#! /usr/bin/env python3

import csv
import numpy as np
import os
import rclpy
from rclpy.node import Node
from scipy.optimize import linear_sum_assignment

from geometry_msgs.msg import PoseStamped
from rosgraph_msgs.msg import Clock as ClockMsg
from std_msgs.msg import String
from search_and_rescue_interfaces.msg import GoalsList

class Edge(Node):

    def __init__(self):
        super().__init__('edge')

        self.goals_list_msg_old = GoalsList()
        self.drones_pos = [[0,0,0],[0,2,0],[2,2,0]]

        self.coords_sub = self.create_subscription(
            GoalsList,
            'roi',
            self.coords_callback,
            10)
        self.coords_sub

        self.goal_pub1 = self.create_publisher(PoseStamped, 'goal1', 10)
        self.goal_pub2 = self.create_publisher(PoseStamped, 'goal2', 10)
        self.goal_pub3 = self.create_publisher(PoseStamped, 'goal3', 10)

    def coords_callback(self, coords_msg):
        grouped_data_list = []
        distance_matrix = np.zeros((3,3))

        # if self.goals_list_msg_old.data != coords_msg.data:
        # self.get_logger().info(f"I heard: {coords_msg.data}")

        # - unpack coords (sequence of coords)
        for i in range(0, len(coords_msg.data), 3):
            group = coords_msg.data[i:i+3]  # Get a group of three elements
            grouped_data_list.append(group)  # Append the group to the list of grouped data

        group1 = np.array(grouped_data_list[0])
        group2 = np.array(grouped_data_list[1])
        group3 = np.array(grouped_data_list[2])

        # - compute distacence drone-ROI
        for i, pos in enumerate(self.drones_pos):
            for j, coords in enumerate(grouped_data_list):
                pos = np.array(pos)
                coords = np.array(coords)
                dist = np.linalg.norm(pos-coords)
                distance_matrix[i][j] = dist
        
        # - send position to the drone that is the nearest
        row_indices, col_indices = linear_sum_assignment(distance_matrix)
        # col_indices: 
        # - col_indices[0] is the index of the target associated to the 1st drone 
        # - col_indices[1] is the index of the target associated to the 2nd drone
        # ...

        self.send_assignemnt(col_indices, grouped_data_list)

        self.goals_list_msg_old.data = coords_msg.data
        
    def send_assignemnt(self, col_indices, grouped_data_list):
        # goal to drone 1
        goal1 = PoseStamped()
        goal1.header.frame_id = 'map'
        goal1.header.stamp = self.get_clock().now().to_msg() # int(self.get_clock().now().nanoseconds / 1000)
        goal1.pose.position.x =  float(grouped_data_list[col_indices[0]][0])
        goal1.pose.position.y =  float(grouped_data_list[col_indices[0]][1])
        goal1.pose.position.z =  float(grouped_data_list[col_indices[0]][2])
        goal1.pose.orientation.w =  0.0
        self.goal_pub1.publish(goal1)
        # self.get_logger().info(f"Sent goal to drone 1: {goal1}")

        # goal to drone 2
        goal2 = PoseStamped()
        goal2.header.frame_id = 'map'
        goal2.header.stamp = self.get_clock().now().to_msg()
        goal2.pose.position.x =  float(grouped_data_list[col_indices[1]][0])
        goal2.pose.position.y =  float(grouped_data_list[col_indices[1]][1])
        goal2.pose.position.z =  float(grouped_data_list[col_indices[1]][2])
        goal2.pose.orientation.w =  0.0
        self.goal_pub2.publish(goal2)
        # self.get_logger().info(f"Sent goal to drone 2: {goal2}")

        # goal to drone 3
        goal3 = PoseStamped()
        goal3.header.frame_id = 'map'
        goal3.header.stamp = self.get_clock().now().to_msg()
        goal3.pose.position.x =  float(grouped_data_list[col_indices[2]][0])
        goal3.pose.position.y =  float(grouped_data_list[col_indices[2]][1])
        goal3.pose.position.z =  float(grouped_data_list[col_indices[2]][2])
        goal3.pose.orientation.w =  0.0        
        self.goal_pub3.publish(goal3)
        # self.get_logger().info(f"Sent goal to drone 3: {goal3}")

def main(args=None):
    rclpy.init(args=args)

    minimal_edge = Edge()

    rclpy.spin(minimal_edge)

    minimal_edge.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()