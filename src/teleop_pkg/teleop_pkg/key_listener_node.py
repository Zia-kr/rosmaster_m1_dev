import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from Rosmaster_Lib import Rosmaster
import time
import sys
import termios
import tty
import select


class CommandPublisher(Node):

    def __init__(self):
        super().__init__('keyboard_publisher')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.speed = 0.2
        timer_period = 0.05
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)
        tty.setcbreak(self.fd)

    def timer_callback(self):
        msg = Twist()
        key = self.get_key()

        if key == '\x1b[A':
            msg.linear.x = self.speed
            self.get_logger().info('Moving Forward')
        elif key == '\x1b[B':
            msg.linear.x = -self.speed
            self.get_logger().info('Moving Backward')
        elif key == '\x1b[C':
            msg.linear.y = self.speed
            self.get_logger().info('Moving Right')
        elif key == '\x1b[D':
            msg.linear.y = -self.speed
            self.get_logger().info('Moving Left')
        elif key == '+':
            self.speed += 0.1
            self.get_logger().info(f'Increasing speed to {self.speed}')
        elif key == '-':
            self.speed = max(0, self.speed - 0.1)
            self.get_logger().info(f'Decreasing speed to {self.speed}')
        elif key == 'r':
            msg.angular.z = self.speed
            self.get_logger().info('Rotating Right')
        elif key == 'l':
            msg.angular.z = -self.speed
            self.get_logger().info('Rotating Left')

        self.publisher_.publish(msg)

    def get_key(self):
        # Non-blocking check: is there data waiting on stdin right now?
        ready, _, _ = select.select([sys.stdin], [], [], 0)
        ready = [sys.stdin]
        if not ready:
            return ''  
            
        key = sys.stdin.read(1)
        if key == '\x1b':
            key += sys.stdin.read(2)
        return key

    def restore_terminal(self):
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)


def main(args=None):
    rclpy.init(args=args)
    command_publisher = CommandPublisher()
    try:
        rclpy.spin(command_publisher)
    finally:
        command_publisher.restore_terminal()
        command_publisher.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()