import socket
import cv2
import time
import numpy as np

HOST, PORT = "127.0.0.1", 666
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))

TCP_HOST, TCP_PORT = "127.0.0.1", 667
client_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_TCP.connect((TCP_HOST, TCP_PORT))

spilit = 1
img_size = 640*360*3
jpg_size = 20000
packet_size = int(jpg_size/spilit)

clock = time.time()
packet_num = 1
fps = 0

print("Wait for image....")

while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif cv2.waitKey(1) & 0xFF == ord('z'):
        client_TCP.send('mid\n'.encode('utf-8'))
    elif cv2.waitKey(1) & 0xFF == ord('x'):
        client_TCP.send('mid-low\n'.encode('utf-8'))
    elif cv2.waitKey(1) & 0xFF == ord('c'):
        client_TCP.send('low\n'.encode('utf-8'))
    elif cv2.waitKey(1) & 0xFF == ord('v'):
        client_TCP.send('lowlow\n'.encode('utf-8'))

    frame_byte, address = s.recvfrom(packet_size)

    jpg_recover = np.frombuffer(frame_byte, np.uint8)
    frame_recover = cv2.imdecode(jpg_recover, cv2.IMREAD_COLOR)
    if frame_recover is None:
        continue
    cv2.putText(frame_recover, str(len(frame_byte)), (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(frame_recover, str(fps), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('frame', 1280, 720)
    cv2.imshow('frame', frame_recover)

    packet_num += 1
    if (time.time() - clock) > 1:
        fps = packet_num
        packet_num = 0
        clock = time.time()

cv2.destroyAllWindows()
client_TCP.close()
