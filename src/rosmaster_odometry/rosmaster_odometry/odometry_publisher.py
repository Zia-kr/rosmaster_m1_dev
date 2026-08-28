import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from Rosmaster_Lib import Rosmaster
import time
import math


class OdometryPublisher(Node):

    def __init__(self):
        super().__init__('odometry_publisher')
        self.publisher_ = self.create_publisher(Odometry, 'odom', 10)
        timer_period = 0.05
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.bot2 = Rosmaster(com="/dev/ttyUSB1") 
        self.bot2.create_receive_threading()
        self.current_time = time.monotonic()
        self.past_time = time.monotonic()
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

    def timer_callback(self):
        self.current_time = time.monotonic()
        vx, vy, vz = self.bot2.get_motion_data()
        dt = self.current_time - self.past_time

        msg = Odometry()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "odom"
        msg.child_frame_id = "base_link"

        self.theta += vz * dt
        self.x += (vx * math.cos(self.theta) - vy * math.sin(self.theta)) * dt
        self.y += (vy * math.cos(self.theta) + vx * math.sin(self.theta)) * dt

        msg.pose.pose.position.x = self.x
        msg.pose.pose.position.y = self.y
        msg.pose.pose.position.z = 0.0

        msg.pose.pose.orientation.x = 0.0
        msg.pose.pose.orientation.y = 0.0
        msg.pose.pose.orientation.z = math.sin(self.theta/2)
        msg.pose.pose.orientation.w = math.cos(self.theta/2)

        msg.twist.twist.linear.x = vx
        msg.twist.twist.linear.y = vy
        msg.twist.twist.linear.z = 0.0

        msg.twist.twist.angular.x = 0.0
        msg.twist.twist.angular.y = 0.0
        msg.twist.twist.angular.z = vz

        print("x: ", self.x, "y: ", self.y, "theta: ", self.theta)

        self.past_time = self.current_time
        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    odometry_publisher = OdometryPublisher()
    rclpy.spin(odometry_publisher)

    odometry_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()