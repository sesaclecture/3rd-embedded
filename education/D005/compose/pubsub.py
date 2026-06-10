# pubsub.py
import time

import zmq


def c_to_f(c: float) -> float:
    return c * 9 / 5 + 32

def main():
    ctx = zmq.Context.instance()

    # 입력(섭씨) 구독
    sub = ctx.socket(zmq.SUB)
    sub.connect("tcp://pub:5555")
    sub.setsockopt_string(zmq.SUBSCRIBE, "")  # 모든 메시지
    print("[PUBSUB] sub tcp://pub:5555 (Celsius in)")

    # 출력(토픽별) 발행
    pub = ctx.socket(zmq.PUB)
    pub.bind("tcp://*:5556")
    print("[PUBSUB] pub tcp://*:5556 (topics: C, F)")

    time.sleep(0.3)  # 연결 안정화

    try:
        while True:
            msg = sub.recv_string()          # "25.37"
            c = float(msg)
            f = c_to_f(c)

            # 토픽별 멀티프레임 발행
            pub.send_multipart([b"C", f"{c:.2f}".encode()])
            pub.send_multipart([b"F", f"{f:.2f}".encode()])

            print(f"[PUBSUB] C:{c:.2f} -> F:{f:.2f}")
    except KeyboardInterrupt:
        pass
    finally:
        sub.close(0)
        pub.close(0)
        ctx.term()

if __name__ == "__main__":
    main()
