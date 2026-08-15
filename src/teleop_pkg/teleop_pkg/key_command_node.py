import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from Rosmaster_Lib import Rosmaster


class CommandSubscriber(Node):

    def __init__(self):
        super().__init__('command_subscriber')
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.listener_callback,
            10)
        self.subscription  
        #self.bot = Rosmaster(com="/dev/ttyUSB1")

    def listener_callback(self, msg):
        #self.bot.set_car_motion(msg.linear.x, msg.linear.y, msg.angular.z)
        self.get_logger().info(f'linear_x: {msg.linear.x}, linear_y: {msg.linear.y}, angular_z: {msg.angular.z}')


def main(args=None):
    rclpy.init(args=args)

    command_subscriber = CommandSubscriber()

    rclpy.spin(command_subscriber)

    command_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()