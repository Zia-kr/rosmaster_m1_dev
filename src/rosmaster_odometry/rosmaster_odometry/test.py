from Rosmaster_Lib import Rosmaster
bot2 = Rosmaster(com="/dev/ttyUSB1") 
bot2.create_receive_threading()

vx, vy, vz = bot2.get_motion_data()
print("vx: ", vx, "vy: ", vy, "vz: ", vz)
print(bot2.get_battery_voltage())

