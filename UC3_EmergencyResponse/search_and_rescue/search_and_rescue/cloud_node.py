#! /usr/bin/env python3

import csv
import os
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped
from rosgraph_msgs.msg import Clock as ClockMsg
from std_msgs.msg import String
from search_and_rescue_interfaces.msg import GoalsList



class Cloud(Node):

    def __init__(self):
        super().__init__('cloud')
    
        self.coord_publisher = self.create_publisher(GoalsList, 'roi', 10)
        timer_period = 0.5  # 2Hz

        self.map_file_path = os.path.abspath('src/search_and_rescue/search_and_rescue/maps/map1.csv')

        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        goals_list_msg = GoalsList()
        goals_list_msg.data = self.coords_from_map(self.map_file_path)

        self.coord_publisher.publish(goals_list_msg)
        # self.get_logger().info(f"Received Int32MultiArray message: {goals_list_msg.data}")

    def coords_from_map(self, map_file_path):
        roi_coords_list = []
        
        with open(map_file_path, newline='') as map_file:
            reader = csv.reader(map_file)

            for row in reader:
                x, y, z = [int(value) for value in row]
                roi_coords_list.append(x)
                roi_coords_list.append(y)
                roi_coords_list.append(z)

                #TODO: now generate coords from a satellite imag

        return roi_coords_list
    
def main(args=None):
    rclpy.init(args=args)

    cloud_dev = Cloud()

    rclpy.spin(cloud_dev)

    cloud_dev.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()