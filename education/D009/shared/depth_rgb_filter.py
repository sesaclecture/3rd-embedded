import cv2
import message_filters
import rclpy  # Load ROS2 Python client library
from cv_bridge import CvBridge  # ROS Image<->OpenCV Mat conversion utility
from rclpy.node import Node
from sensor_msgs.msg import Image


class DepthRgbFilter(Node): # Define a new ROS node by inheriting from Node
    def __init__(self):
        super().__init__('depth_rgb_filter')
        self.bridge = CvBridge()

        # Subscribe to RGB and depth topics with synchronization
        rgb_sub = message_filters.Subscriber(self, Image, '/ascamera/camera_publisher/rgb0/image')
        depth_sub = message_filters.Subscriber(self, Image, '/ascamera/camera_publisher/depth0/image_raw')

        ts = message_filters.ApproximateTimeSynchronizer([rgb_sub, depth_sub], queue_size=10, slop=0.05)
        ts.registerCallback(self.callback)

    # Callback where the actual image processing happens
    def callback(self, rgb_msg, depth_msg):
        # Convert ROS Image messages to OpenCV format
        rgb = self.bridge.imgmsg_to_cv2(rgb_msg, 'bgr8')
        depth = self.bridge.imgmsg_to_cv2(depth_msg, '16UC1')

        cv2.imshow('RGB Preview', rgb)
        cv2.imshow('Depth Preview', depth)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)   # Initialize ROS2 communication
    node = DepthRgbFilter() # Create the node instance
    rclpy.spin(node)        # Enter the callback waiting loop
    node.destroy_node()     # Clean up the node
    rclpy.shutdown()        # Shut down ROS2

if __name__ == '__main__':
    main()
