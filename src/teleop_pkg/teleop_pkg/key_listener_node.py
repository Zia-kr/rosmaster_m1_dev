import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from Rosmaster_Lib import Rosmaster
from pynput.keyboard import Key, Listener, KeyCode
import time


class CommandPublisher(Node):

    def __init__(self):
        super().__init__('keyboard_publisher')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.speed = 0.2  
        self.plus = KeyCode.from_char('p')
        self.minus = KeyCode.from_char('m')
        self.R = KeyCode.from_char('r')
        self.L = KeyCode.from_char('l')
        self.press_period = 0.2
        self.last_press_time = {}
        self.listener = Listener(on_press=self.on_press)
        self.listener.start()
        timer_period = 0.05
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = Twist()

        if self.is_held_down(self.plus):
            self.speed += 0.1
        elif self.is_held_down(self.minus):
            self.speed = max(0.0, self.speed - 0.1)

        if self.is_held_down(Key.up):
            msg.linear.x = self.speed
        elif self.is_held_down(Key.down):
            msg.linear.x = -self.speed

        if self.is_held_down(Key.left):
            msg.linear.y = -self.speed
        elif self.is_held_down(Key.right):
            msg.linear.y = self.speed

        if self.is_held_down(self.R):
            msg.angular.z = self.speed
        elif self.is_held_down(self.L):
            msg.angular.z = -self.speed

        self.publisher_.publish(msg)
        #self.get_logger().info(f'Publishing: {msg}')

    def on_press(self, key):
        self.last_press_time[key] = time.monotonic()

    def is_held_down(self, key):
        last = self.last_press_time.get(key)
        t = time.monotonic()
        return last is not None and (t-self.last_press_time[key]) < self.press_period


def main(args=None):
    rclpy.init(args=args)
    command_publisher = CommandPublisher()
    rclpy.spin(command_publisher)
    command_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()