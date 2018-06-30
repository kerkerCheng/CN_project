import cv2
import socket
import threading
import numpy as np

HOST, PORT = "127.0.0.1", 666
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = (HOST, PORT)

recv_HOST, recv_PORT = "127.0.0.1", 667
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((recv_HOST, recv_PORT))
server.listen(5)

print("listening on %s : %d" % (recv_HOST, recv_PORT))


def handle_client(client_socket):
    request = client_socket.recv(1024)
    print("Received: %s" % request)
    client_socket.send("ACK!")
    client_socket.close()


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

spilit = 1
img_size = 360*640*3
jpg_size = 15600
packet_size = int(jpg_size / spilit)


state = 0

def main():
    


while True:

    ret, frame = cap.read()
    ret, jpg = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 40])
    print(jpg.shape)
    d = jpg.flatten()
    frame_byte = d.tostring()
    # jpg_recover = np.fromstring(frame_byte, dtype=np.uint8)
    # frame_recover = cv2.imdecode(jpg_recover, cv2.IMREAD_COLOR)

    for i in range(spilit):
        s.sendto(frame_byte[i*packet_size:(i+1)*packet_size], addr)

    # cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('frame', 1280, 720)
    # cv2.imshow('frame', frame)

    recv_cli, recv_addr = server.accept()
    print("Accept %s %d" % (addr[0], addr[1]))
    client_handler = threading.Thread(target=handle_client, args=(recv_cli))
    client_handler.start()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()

cv2.destroyAllWindows()
