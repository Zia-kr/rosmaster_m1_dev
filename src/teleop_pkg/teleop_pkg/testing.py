import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from Rosmaster_Lib import Rosmaster
import time
import sys
import termios
import tty
import select

bot4 = Rosmaster(com="/dev/ttyUSB1")
bot4.create_receive_threading()
while True :
    print("Accelerometer Data:", bot4.get_accelerometer_data())
    print("Gyroscope Data:", bot4.get_gyroscope_data())