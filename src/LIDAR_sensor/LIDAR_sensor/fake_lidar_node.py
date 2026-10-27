#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import math


class FakeLidar(Node):
    def __init__(self):
        super().__init__("fake_lidar")
        self.lidar = self.create_publisher(LaserScan, "/scan", 10)
        self.timer_period = 0.1
        self.timer = self.create_timer(self.timer_period, self.publish_scan)
        self.angle_offset = 0.0

    def publish_scan(self):
        self.sensor = LaserScan()
        self.sensor.angle_min = -math.pi
        self.sensor.angle_max = math.pi
        self.sensor.angle_increment = math.pi / 180
        self.sensor.scan_time = 0.1
        self.sensor.range_min = 0.1
        self.sensor.range_max = 10.0
        self.sensor.header.stamp = self.get_clock().now().to_msg()
        self.sensor.header.frame_id = "laser_frame"

        total_readings = int(
            (self.sensor.angle_max - self.sensor.angle_min)
            / self.sensor.angle_increment
        )
        obstacles_list = []
        self.angle_offset += 0.1
        for i in range(total_readings):
            theta = self.sensor.angle_min + (i * self.sensor.angle_increment)
            if (
                (-15 + self.angle_offset)
                >= math.degrees(theta)
                >= (-45 + self.angle_offset)
            ):
                obstacles_list.append(1.2)
            elif 20 <= math.degrees(theta) <= 60:
                obstacles_list.append(1.8)
            else:
                obstacles_list.append(5.0)
        self.sensor.ranges = obstacles_list
        self.lidar.publish(self.sensor)


def main(args=None):
    rclpy.init(args=args)
    node = FakeLidar()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
