import cv2

# v4l2-ctl -d /dev/video0 --list-formats-ext

# Read from the first camera device
cap = cv2.VideoCapture(4)

w = 640#1280
h = 480#720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)

# 성공적으로 video device 가 열렸으면 while 문 반복
while(cap.isOpened()):
    # 한 프레임을 읽어옴
    ret, frame = cap.read()
    if ret is False:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Display
    cv2.imshow("Camera", frame)

    # 1 ms 동안 대기하며 키 입력을 받고 'q' 입력 시 종료
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break

#import cv2

## 0번 카메라 열기
#cap = cv2.VideoCapture(0)
#
## 해상도 고정
#cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
#
## VideoWriter 준비 (640x480, 30fps, mp4 코덱)
#fourcc = cv2.VideoWriter_fourcc(*"mp4v")
#writer = cv2.VideoWriter("output.mp4", fourcc, 30.0, (640, 480))
#
#while True:
#    ret, frame = cap.read()
#    if not ret:
#        break
#
#    # 화면 출력
#    cv2.imshow("Camera", frame)
#
#    # 프레임 저장
#    writer.write(frame)
#
#    # 'q' 입력 시 종료
#    if cv2.waitKey(1) & 0xFF == ord('q'):
#        break
#
#cap.release()
#writer.release()
#cv2.destroyAllWindows()
#
