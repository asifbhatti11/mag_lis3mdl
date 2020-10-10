#!/usr/bin/env python
import rospy
from sensor_msgs.msg import MagneticField

import time
import board
import busio
import adafruit_lis3mdl

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_lis3mdl.LIS3MDL(i2c)

calibration=(0,0,0) # follow https://learn.adafruit.com/adafruit-sensorlab-magnetometer-calibration for calibration and replace calibration values with (0,0,0)
def mag():
    pub = rospy.Publisher('MagneticField', MagneticField, queue_size=10)
    rospy.init_node('MagneticField', anonymous=True)
    i=0
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        seq = i
        mag_msg = MagneticField()
        mag_msg.header.seq = seq
        mag_msg.header.frame_id = 'lis3mdl'
        mag_msg.header.stamp = rospy.Time.now()
        mag_msg.magnetic_field.x = sensor.magnetic[0]-calibration[0]
        mag_msg.magnetic_field.y = sensor.magnetic[1]-calibration[1]
        mag_msg.magnetic_field.z = sensor.magnetic[2]-calibration[2]
        pub.publish(mag_msg)
        i = i + 1
        rate.sleep()

if __name__ == '__main__':
    try:
        mag()
    except rospy.ROSInterruptException:
        pass
