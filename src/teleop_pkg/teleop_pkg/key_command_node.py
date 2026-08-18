import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from Rosmaster_Lib import Rosmaster
import time



class CommandSubscriber(Node):

    def __init__(self):
        super().__init__('command_subscriber')
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.listener_callback,
            10)
        self.subscription  
        self.bot = Rosmaster(com="/dev/ttyUSB1")
        self.bot.create_receive_threading()
        watchdog_timer_period = 0.1
        self.timer = self.create_timer(watchdog_timer_period, self.watchdog_timer_callback)
        self.last_command_time = time.monotonic()
        self.should_stop = False



    def listener_callback(self, msg):
        self.last_command_time = time.monotonic()
        self.bot.set_car_motion(msg.linear.x, msg.linear.y, msg.angular.z)
        self.bot.get_motion_data()
    
    def watchdog_timer_callback(self):
        current_time = time.monotonic()
        if current_time - self.last_command_time > 0.8:
            self.bot.set_car_motion(0.0, 0.0, 0.0)
            self.get_logger().info('No command received for 0.1 seconds, stopping the robot.')
            if current_time - self.last_command_time > 1.5:
                self.get_logger().info('No command received for 1.5 seconds, stopping the robot and exiting.')
                self.should_stop = True
        else:
            self.get_logger().info('Command received, robot is moving.')


def main(args=None):
    rclpy.init(args=args)

    command_subscriber = CommandSubscriber()
    while rclpy.ok() and not command_subscriber.should_stop:
        rclpy.spin_once(command_subscriber)

    command_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()