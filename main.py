import cv2
import socket
import threading
import numpy as np
import time

HOST, PORT = "127.0.0.1", 666
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = (HOST, PORT)

recv_HOST, recv_PORT = "127.0.0.1", 667
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((recv_HOST, recv_PORT))
server.listen(5)

print("listening on %s : %d" % (recv_HOST, recv_PORT))

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 360)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)


def main():
    t = threading.Thread(target=do_stream, args=((40, 20000),))
    t.start()
    client, addr = server.accept()
    print("Acepted connection from : %s:%d" % (addr[0], addr[1]))
    while True:
        recv_byte = client.recv(1024)
        request = recv_byte.decode('utf-8').split('\n')[0]

        if request == 'mid':
            print('mid----')
            parameter = (40, 20000)
            t.do_run = False
            t.join()
            t = threading.Thread(target=do_stream, args=(parameter,))
            t.start()
        elif request == 'mid-low':
            print('mid-low----')
            parameter = (30, 15000)
            t.do_run = False
            t.join()
            t = threading.Thread(target=do_stream, args=(parameter,))
            t.start()
        elif request == 'low':
            print('low----')
            parameter = (20, 12000)
            t.do_run = False
            t.join()
            t = threading.Thread(target=do_stream, args=(parameter,))
            t.start()
        elif request == 'lowlow':
            print('lowlow----')
            parameter = (10, 8000)
            t.do_run = False
            t.join()
            t = threading.Thread(target=do_stream, args=(parameter,))
            t.start()


def do_stream(parameter):
    print('start thread')
    quality, packet_size = parameter
    t = threading.current_thread()
    while getattr(t, "do_run", True):
        video_streaming(quality, packet_size)
    print("stop thread")


def video_streaming(quality, packet_size):
    spilit = 1
    img_size = 360 * 640 * 3
    jpg_size = packet_size
    packet_size = int(jpg_size / spilit)

    ret, frame = cap.read()
    if frame is not None:
        ret, jpg = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
        # print(jpg.shape)
        d = jpg.flatten()
        frame_byte = d.tostring()
        # jpg_recover = np.fromstring(frame_byte, dtype=np.uint8)
        # frame_recover = cv2.imdecode(jpg_recover, cv2.IMREAD_COLOR)

        for i in range(spilit):
            s.sendto(frame_byte[i*packet_size:(i+1)*packet_size], addr)

    # cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('frame', 1280, 720)
    # cv2.imshow('frame', frame)

    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
    #
    # cap.release()
    #
    # cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
