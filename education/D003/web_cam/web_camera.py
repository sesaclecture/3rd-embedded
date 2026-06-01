#!/usr/bin/python3

import atexit
import collections
import os.path
import threading
import time

import cv2
import flask

###############################################################################
# Camera part


class Camera(threading.Thread):
    def __init__(self, device):
        super(Camera, self).__init__()
        self.cv = threading.Condition()
        self.stop = False

        self.cap = cv2.VideoCapture(device)
        self.frame = None
        #self.setsize(800, 600)
        #self.setfps(10)

        self.start()

        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        print('size {}'.format(self.getsize()))

    def shot(self):
        with self.cv:
            self.cv.wait()

        return bytes(self.frame)

    def run(self):
        while self.stop is not True:
            _, raw = self.cap.read()
            _, self.frame = cv2.imencode(".jpg", raw)

            with self.cv:
                self.cv.notify_all()

    def __del__(self):
        with self.cv:
            self.cv.notify_all()

        self.cap.release()
        self.out.release()
        cv2.destroyAllWindows()

    def getdev():
        camdev_name = []
        camdev_path = [
            '/sys/class/video4linux/video0', '/sys/class/video4linux/video1',
            '/sys/class/video4linux/video2'
        ]
        camdev_idx_max = -1

        for i in camdev_path:
            if os.path.exists(i):
                file = open(i + '/name')
                camdev_idx_max += 1
                camdev_name.insert(camdev_idx_max, file.readline().rstrip())
            else:
                if camdev_idx_max == -1:
                    camdev_name.append('None')
                break

    def getsize(self):
        width = self.cap.get(3)  # 3: CV_CAP_PROP_FRAME_WIDTH
        height = self.cap.get(4)  # 4: CV_CAP_PROP_FRAME_HEIGHT
        return (int(width), int(height))

    def setsize(self, width, height):
        self.cap.set(3, width)
        self.cap.set(4, height)

    def getfps(self):
        return self.cap.get(5)  # 5: CV_CAP_PROP_FPS

    def setfps(self, fps):
        self.cap.set(5, fps)  # 5: CV_CAP_PROP_FPS


###############################################################################
# Camera instance

Camera.getdev()
camera = Camera(0)


def close_camera():
    camera.stop = True
    camera.join()


atexit.register(close_camera)

###############################################################################
# Web part

app = flask.Flask(__name__)


def jpeg():
    while True:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + camera.shot() + b'\r\n')


@app.route('/')
def route_index():
    return """\
<html>
    <head>
        <title>Camera streaming test</title>
    </head>
    <body>
        <h1>Live Camera Streaming</h1>
        <img src="/cam">
    </body>
</html>\
"""


@app.route('/cam')
def route_cam():
    return flask.Response(jpeg(),
                          mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8084, threaded=True)
