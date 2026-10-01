import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

def wrap_to_pi(a: float) -> float:
    while a > math.pi:
        a -= 2.0 * math.pi
    while a < -math.pi:
        a += 2.0 * math.pi
    return a
    
class Turtle06(Node):
    def __init__(self):
        super().__init__('cherepaxa06')

        self.declare_parameter('digit', 67)
        self.declare_parameter('rate_hz', 30.0)
        self.declare_parameter('linear_v', 1.0)
        
        rate_hz = float(self.get_parameter('rate_hz').value)
        
        self.digit = int(self.get_parameter('digit').value)
        self.v = float(self.get_parameter('linear_v').value)
        
        name = f'cherepaxa06_{self.digit}'
        
        self.waypoints = []
        if self.digit == 0:
            self.waypoints = [
            (2.0, 8.0),
            (5.0, 8.0),
            (5.0, 2.0),
            (2.0, 2.0)]
        if self.digit == 6:
            self.waypoints = [
            (9.0, 5.0),
            (9.0, 2.0),
            (6.0, 2.0),
            (6.0, 8.0),
            (9.0, 8.0)]

        self.publisher = self.create_publisher(Twist, f'/{name}/cmd_vel', 10)
        self.create_subscription(Pose, f'/{name}/pose', self.on_pose, 10)
        self.t0 = self.get_clock().now()
        

        self.timer = self.create_timer(1.0 / rate_hz, self.on_timer)
        
    def on_pose(self, msg):
        self.pose = msg
        self.pose_done = True

    def on_timer(self):
        now = self.get_clock().now()
        t = (now - self.t0).nanoseconds * 1e-9
        angle_err = 0.0
        vel = self.v
        
        if len(self.waypoints) > 0 and self.pose_done:
            p1 = (self.pose.x, self.pose.y)
            p2 = self.waypoints[0]
            d = (p2[0]-p1[0], p2[1]-p1[1])
            
            if (d[0]*d[0] + d[1]*d[1])**0.5 < 0.01:
                self.waypoints.pop(0)
                vel = 0.0
            else:
                phi = math.atan2(d[1], d[0])
                theta = self.pose.theta
                angle_err = wrap_to_pi(phi - theta)
                
                if math.fabs(angle_err) > 0.05:
                    vel = 0.0
        else:
            vel = 0.0
        
    
        msg = Twist()
        msg.linear.x = vel
        msg.angular.z = angle_err * 10
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = Turtle06()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
