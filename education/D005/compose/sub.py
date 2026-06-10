# sub.py
import sys

import zmq


def main():
    if len(sys.argv) < 2:
        print("사용법: python sub.py <토픽>")
        print("예:    python sub.py C   또는   python sub.py F")
        sys.exit(1)

    topic = sys.argv[1]

    ctx = zmq.Context()
    sub = ctx.socket(zmq.SUB)
    sub.connect("tcp://pubsub:5556")
    sub.setsockopt_string(zmq.SUBSCRIBE, topic)

    print(f"[SUB] Subscribed to topic '{topic}'")

    try:
        while True:
            t, msg = sub.recv_multipart()
            print(f"[{t.decode()}] {msg.decode()}")
    except KeyboardInterrupt:
        pass
    finally:
        sub.close()
        ctx.term()

if __name__ == "__main__":
    main()
