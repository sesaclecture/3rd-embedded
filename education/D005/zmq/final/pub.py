# pub.py
import time
import random
import zmq

def main():
    ctx = zmq.Context.instance()
    pub = ctx.socket(zmq.PUB)
    pub.bind("tcp://*:5555")
    print("[PUB] bind tcp://*:5555 (topicless, Celsius only)")
    time.sleep(0.3)  # slow-joiner 완화

    try:
        while True:
            temp_c = round(random.uniform(20.0, 30.0), 2)
            pub.send_string(str(temp_c))  # 토픽 없이 값만
            print(f"[PUB] {temp_c}C")
            time.sleep(1.0)
    except KeyboardInterrupt:
        pass
    finally:
        pub.close(0)
        ctx.term()

if __name__ == "__main__":
    main()

