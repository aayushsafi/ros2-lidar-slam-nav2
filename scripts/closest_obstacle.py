import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

class ClosestObstacle(Node):
    def __init__(self):
        super().__init__('closest_obstacle')
        self.create_subscription(LaserScan, '/scan', self.callback, 10)

    def callback(self, msg):
        closest_r, closest_a = float('inf'), None
        front_r, front_a = float('inf'), None
        for i, r in enumerate(msg.ranges):
            if not (math.isfinite(r) and msg.range_min <= r <= msg.range_max):
                continue
            angle = msg.angle_min + i * msg.angle_increment
            if r < closest_r:
                closest_r, closest_a = r, angle
            if abs(angle) <= math.radians(30) and r < front_r:
                front_r, front_a = r, angle

        overall = (f'{closest_r:.2f} m at {math.degrees(closest_a):.0f}°'
                   if closest_a is not None else 'none')
        front = (f'{front_r:.2f} m at {math.degrees(front_a):.0f}°'
                 if front_a is not None else 'CLEAR')
        self.get_logger().info(f'Overall: {overall} | Front 60°: {front}')

def main():
    rclpy.init()
    rclpy.spin(ClosestObstacle())

if __name__ == '__main__':
    main()
