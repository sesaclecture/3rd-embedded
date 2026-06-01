import json
import os
from datetime import datetime

import cv2
import numpy as np
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image


def nothing(x):
    pass


class LabCalibrationNode(Node):
    def __init__(self):
        super().__init__('lab_calibration_node')

        self.bridge = CvBridge()
        self.json_name = 'LAB-cal.json'

        self.keys = [
            ("l_min", 0),
            ("l_max", 255),
            ("a_min", 0),
            ("a_max", 255),
            ("b_min", 0),
            ("b_max", 255),
        ]

        self.cfg = {k: v for k, v in self.keys}

        if os.path.exists(self.json_name):
            with open(self.json_name, "r") as f:
                loaded_cfg = json.load(f)
                self.cfg.update(loaded_cfg)
            self.get_logger().info(f"Loaded {self.json_name}")
        else:
            self.get_logger().info(f"{self.json_name} not found. Use default values.")

        cv2.namedWindow("Trackbars")

        for k, v in self.keys:
            cv2.createTrackbar(k, "Trackbars", int(self.cfg.get(k, v)), 255, nothing)

        self.sub = self.create_subscription(
            Image,
            '/ascamera/camera_publisher/rgb0/image',
            self.callback,
            10
        )

        self.get_logger().info("LAB calibration node started")
        self.get_logger().info("Press s to save, ESC to quit")

    def save_config(self, vals):
        out = dict(zip([k for k, _ in self.keys], vals))

        now = datetime.now().strftime("%y%m%d-%H%M%S")

        with open(f"LAB-cal-{now}.json", "w") as f:
            json.dump(out, f, indent=4)

        with open(self.json_name, "w") as f:
            json.dump(out, f, indent=4)

        print(f"Saved LAB-cal-{now}.json & {self.json_name}")
        print(out)

    def callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

        vals = [cv2.getTrackbarPos(k, "Trackbars") for k, _ in self.keys]

        lower, upper = np.array(vals[::2]), np.array(vals[1::2])
        mask = cv2.inRange(lab, lower, upper)
        res = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.imshow("Original", cv2.resize(frame, (640, 480)))
        cv2.imshow("LAB Mask", cv2.resize(mask, (640, 480)))
        cv2.imshow("LAB Filter", cv2.resize(res, (640, 480)))

        key = cv2.waitKey(1) & 0xFF

        if key == ord("s"):
            self.save_config(vals)

        elif key == 27:
            rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)

    node = LabCalibrationNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    cv2.destroyAllWindows()

    if rclpy.ok():
        rclpy.shutdown()


if __name__ == '__main__':
    main()
