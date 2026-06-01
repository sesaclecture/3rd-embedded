import json
import os

import cv2
import message_filters
import numpy as np
import rclpy
from cv_bridge import CvBridge
from geometry_msgs.msg import Twist
from rclpy.node import Node
from sensor_msgs.msg import Image


class ObjectTrackerNode(Node):
    def __init__(self):
        super().__init__('obj_tracker_node')

        self.bridge = CvBridge()

        self.cmd_topic = '/controller/cmd_vel'

        self.target_depth = 350
        self.margin = 50

        self.turn_gain = 0.003

        self.lab_cfg = self.load_lab_config('LAB-cal.json')

        rgb_sub = message_filters.Subscriber(
            self,
            Image,
            '/ascamera/camera_publisher/rgb0/image'
        )

        depth_sub = message_filters.Subscriber(
            self,
            Image,
            '/ascamera/camera_publisher/depth0/image_raw'
        )

        ts = message_filters.ApproximateTimeSynchronizer(
            [rgb_sub, depth_sub],
            queue_size=10,
            slop=0.05
        )

        ts.registerCallback(self.callback)

        self.mecanum_pub = self.create_publisher(
            Twist,
            self.cmd_topic,
            1
        )

        self.get_logger().info('obj_tracker_node started')
        self.get_logger().info(f'cmd topic: {self.cmd_topic}')
        self.get_logger().info(f'LAB config: {self.lab_cfg}')

    def load_lab_config(self, json_name):
        cfg = {
            "l_min": 0,
            "l_max": 255,
            "a_min": 0,
            "a_max": 255,
            "b_min": 0,
            "b_max": 255,
        }

        if not os.path.exists(json_name):
            self.get_logger().warn(f'{json_name} not found. Use default LAB values.')
            return cfg

        with open(json_name, 'r') as f:
            loaded_cfg = json.load(f)

        cfg.update(loaded_cfg)
        return cfg

    def go_straight(self, speed=0.1):
        self.get_logger().info(f'Moving straight: {speed}')

        twist = Twist()

        if speed >= -1.0 and speed <= 1.0:
            twist.linear.x = speed
        else:
            twist.linear.x = 0.1

        twist.linear.y = 0.0
        twist.linear.z = 0.0

        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = 0.0

        self.mecanum_pub.publish(twist)

    def stop(self):
        self.get_logger().info('Stopping')

        twist = Twist()

        twist.linear.x = 0.0
        twist.linear.y = 0.0
        twist.linear.z = 0.0

        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = 0.0

        self.mecanum_pub.publish(twist)

    def turn_left(self, angle):
        self.get_logger().info(f'Turning: {angle}')

        twist = Twist()

        twist.linear.x = 0.0
        twist.linear.y = 0.0
        twist.linear.z = 0.0

        twist.angular.x = 0.0
        twist.angular.y = 0.0

        twist.angular.z = angle * self.turn_gain

        self.mecanum_pub.publish(twist)

    def turn_angle(self, screen_width, object_x):
        screen_cx = screen_width // 2
        error_x = object_x - screen_cx

        if abs(error_x) < 40:
            return 0.0

        angle = -error_x
        return angle

    def get_depth_at_center(self, depth, cx, cy):
        h, w = depth.shape

        x1 = max(cx - 5, 0)
        x2 = min(cx + 5, w)
        y1 = max(cy - 5, 0)
        y2 = min(cy + 5, h)

        roi = depth[y1:y2, x1:x2]
        valid = roi[roi > 0]

        if len(valid) == 0:
            return 0

        return int(np.median(valid))

    def callback(self, rgb_msg, depth_msg):
        frame = self.bridge.imgmsg_to_cv2(rgb_msg, 'bgr8')
        depth = self.bridge.imgmsg_to_cv2(depth_msg, '16UC1')

        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

        vals = [
            self.lab_cfg["l_min"],
            self.lab_cfg["l_max"],
            self.lab_cfg["a_min"],
            self.lab_cfg["a_max"],
            self.lab_cfg["b_min"],
            self.lab_cfg["b_max"],
        ]

        lower, upper = np.array(vals[::2]), np.array(vals[1::2])
        mask = cv2.inRange(lab, lower, upper)
        res = cv2.bitwise_and(frame, frame, mask=mask)

        # 컨투어(윤곽선)들을 찾아서 contours 에 저장
        # OpenCV에서 객체 검출, 분할, 모양 분석, 측정 등에 가장 널리 사용됨
        # contours, hierarchy = cv2.findContours(image, mode, method[, contours[, hierarchy[, offset]]])
        # method: 윤곽선 근사화(압축) 방법
        #   - cv2.CHAIN_APPROX_SIMPLE: 꼭짓점만 반환(메모리 절약)
        #   - cv2.CHAIN_APPROX_NONE: 모든 경계점 반환
        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        if contours:
            # 각 컨투어의 면적 계산 후, 가장 큰 것 선택
            biggest = max(contours, key=cv2.contourArea)

            area = cv2.contourArea(biggest)

            if area < 500:
                self.stop()
                cv2.imshow("LAB Object Tracking", cv2.resize(res, (640, 480)))
                cv2.waitKey(1)
                return

            x, y, w, h = cv2.boundingRect(biggest)

            cx = x + w // 2
            cy = y + h // 2

            depth_mm = self.get_depth_at_center(depth, cx, cy)

            cv2.rectangle(res, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(res, (cx, cy), 5, (0, 0, 255), -1)

            cv2.putText(
                res,
                f"Rect: ({x},{y},{w},{h})",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            cv2.putText(
                res,
                f"Depth: {depth_mm} mm",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2
            )

            screen_width = frame.shape[1]
            angle = self.turn_angle(screen_width, cx)

            if angle != 0.0:
                self.turn_left(angle)

            elif depth_mm == 0:
                self.stop()

            elif depth_mm > self.target_depth + self.margin:
                self.go_straight(0.08)

            elif depth_mm < self.target_depth - self.margin:
                self.go_straight(-0.05)

            else:
                self.stop()

        else:
            self.stop()

            cv2.putText(
                res,
                "Object not found",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

        cv2.imshow("LAB Object Tracking", cv2.resize(res, (640, 480)))
        cv2.imshow("LAB Mask", cv2.resize(mask, (640, 480)))
        cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)

    node = ObjectTrackerNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.stop()
    node.destroy_node()
    cv2.destroyAllWindows()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
