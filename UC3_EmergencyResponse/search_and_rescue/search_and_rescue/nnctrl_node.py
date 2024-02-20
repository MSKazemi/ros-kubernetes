
from px4_msgs.msg import VehicleRatesSetpoint, VehicleLocalPosition, VehicleAttitude, VehicleOdometry
from pathlib import Path
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy

from message_filters import Subscriber, ApproximateTimeSynchronizer

import numpy as np

import torch
import torch.nn as nn


class NNCtrl(Node):

    def __init__(self, path):
        super().__init__('nnctrl')

        # Configure QoS profile for publishing and subscribing
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )
        
        # # Create Subscribers to sensor topics
        self.vehicle_local_position_subscriber = self.create_subscription(
            VehicleLocalPosition, '/fmu/out/vehicle_local_position', self.vehicle_local_position_callback, qos_profile=qos_profile)
        self.vehicle_attitude_subscriber = self.create_subscription(
            VehicleAttitude, '/fmu/out/vehicle_attitude', self.vehicle_attitude_callback, qos_profile=qos_profile)
        self.vehicle_angvel_subscriber = self.create_subscription(
            VehicleOdometry, '/fmu/out/vehicle_odometry', self.vehicle_odom_callback, qos_profile=qos_profile)
        
        # self.vehicle_local_position_subscriber = Subscriber(self, VehicleLocalPosition, '/fmu/out/vehicle_local_position', qos_profile=qos_profile)
        # self.vehicle_attitude_subscriber = Subscriber(self, VehicleAttitude, '/fmu/out/vehicle_attitude', qos_profile=qos_profile)
        # self.vehicle_angvel_subscriber = Subscriber(self, VehicleAngularVelocity, '/fmu/out/vehicle_attitude', qos_profile=qos_profile)

        #  Synchronize data
        # self.ts = ApproximateTimeSynchronizer([self.vehicle_local_position_subscriber, self.vehicle_attitude_subscriber, \
        #                                                        self.vehicle_angvel_subscriber], 10, 0.01, allow_headerless=True)

        # Create Publishers
        self.ctbr_publisher = self.create_publisher(VehicleRatesSetpoint, '/ctbr_nn', 30)
        
        # Create variables
        self.device = 'cpu'
        self.vehicle_local_position = VehicleLocalPosition()
        self.vehicle_attitude = VehicleAttitude()
        self.vehicle_odm = VehicleOdometry()
        self.obs = torch.zeros(19, dtype=torch.float32, device=self.device)
        self.tgt_pos = torch.tensor([0,0,3], dtype=torch.float32, device=self.device)
        self.gate_pos = torch.tensor([0,0,3], dtype=torch.float32, device=self.device)
        self.gate_vel = torch.tensor([0,0,0], dtype=torch.float32, device=self.device)
        self.max_body_rate = 0.1

        # Create Neural Netwwork
        self.model = NNModel(path)
        self.model.eval()

        # Create a timer to publish control commands
        self.timer = self.create_timer(0.02, self.timer_callback)

    def vehicle_local_position_callback(self, vehicle_local_position):
        """Callback function for vehicle_local_position topic subscriber."""
        self.vehicle_local_position = vehicle_local_position
        self.get_logger().info(f'HEARD LOCALPOS:{vehicle_local_position.x, vehicle_local_position.y, vehicle_local_position.z}')

    def vehicle_attitude_callback(self, vehicle_attitude):
        """Callback function for vehicle_goal_position topic subscriber."""
        self.vehicle_attitude = vehicle_attitude

    def vehicle_odom_callback(self, vehicle_odm):
        """Callback function for vehicle_goal_position topic subscriber."""
        self.vehicle_odm = vehicle_odm

    def timer_callback(self):
        
        # Convertion from NED to ENU
        torch_vehicle_pos = torch.tensor([-self.vehicle_local_position.y, -self.vehicle_local_position.x, -self.vehicle_local_position.z], dtype=torch.float32, device=self.device)
        # Orientation of the FRD body frame wrt the NED
        torch_vehicle_att = torch.tensor([self.vehicle_attitude.q], dtype=torch.float32, device=self.device)
        # Convertion from NED to ENU
        torch_vehicle_linvel = torch.tensor([ -self.vehicle_local_position.vy, -self.vehicle_local_position.vx, -self.vehicle_local_position.vz], dtype=torch.float32, device=self.device)
        # angvel in body fixed frame from FRD to FLU
        torch_vehicle_angvel = torch.tensor([self.vehicle_odm.angular_velocity[0],-self.vehicle_odm.angular_velocity[1], -self.vehicle_odm.angular_velocity[2]], dtype=torch.float32, device=self.device)
        

        # TODO CHECK reference frames of stuf and coherence!!
        self.obs[0:3] = (torch_vehicle_pos - self.tgt_pos)
        self.obs[3:7] = torch_vehicle_att
        self.obs[7:10] = torch_vehicle_linvel
        self.obs[10:13] = torch_vehicle_angvel
        self.obs[13:16] = (torch_vehicle_pos - self.gate_pos)
        self.obs[16:19] = self.gate_vel

        action = self.model(self.obs[None, ...])
        action = action.squeeze().detach()

        action_msg = VehicleRatesSetpoint()
        action_msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        # from FLU to FRD
        action_msg.roll = action[0].item() * self.max_body_rate
        action_msg.pitch = -action[1].item() * self.max_body_rate
        action_msg.yaw = -action[2].item() * self.max_body_rate
        action_msg.thrust_body[2] = -(1+action[3].item())/2 #action[3].item() -(1+action[3].item())/2
        
        self.ctbr_publisher.publish(action_msg)
        # self.get_logger().info(f'-----NN output\n{action}')


def main(args=None):
    rclpy.init(args=args)

    nn_ctrl = NNCtrl(Path("src/search_and_rescue/search_and_rescue/nn_models/11V2CorrectFriction02.pth"))

    rclpy.spin(nn_ctrl)
    rclpy.shutdown()

if __name__ == '__main__':
    main()


## Neural Network model

class NNModel(nn.Module):
    def __init__(self, path, device = 'cpu'):
        super().__init__()

        self.device = device
        self.path = path
        self.model = nn.Sequential(
            nn.Linear(19, 256), 
            nn.ELU(),
            nn.Linear(256, 256), 
            nn.ELU(), 
            nn.Linear(256, 128), 
            nn.ELU(), 
            nn.Linear(128, 4),
        )

        self._load_net()
    
    def _load_net(self):
        dict_net = torch.load(self.path, map_location=torch.device(self.device))
        cntr = 0
        
        for key, value in dict_net["model"].items():
            if ("actor_mlp" in key) or ("mu" in key):
                if "weight" in key:
                    self.model[cntr].weight.data = value
                elif "bias" in key:
                    self.model[cntr].bias.data = value
                    cntr += 2
        
        self.running_mean = dict_net["model"]["running_mean_std.running_mean"]
        self.running_var = dict_net["model"]["running_mean_std.running_var"]


    def forward(self, x):

        # TODO Why -5,5 as max range ????????
        x = torch.clamp((x - self.running_mean.float()) / torch.sqrt(self.running_var.float() + 1e-5), -5, 5)
        return torch.clip(self.model(x), -1, 1)