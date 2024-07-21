import socket
import keyboard
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import threading

# UDP setup
server_ip = ""  # Arduino IP address
server_port = 8888
local_ip = "0.0.0.0"  # Listen on all interfaces
local_port = 8888

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((local_ip, local_port))

# Variables for plotting
num = [0] * 181

fig, ax = plt.subplots(figsize=(12, 8))
lines = [ax.plot([], [], 'b-')[0] for _ in range(181)]
scatter = ax.scatter([], [], c='r', s=20)
ax.set_aspect('equal')
ax.set_xlabel('X (cm)')
ax.set_ylabel('Y (cm)')
ax.set_title('Ultrasonic Sensor Mapping')
ax.set_xlim(-300, 300)
ax.set_ylim(0, 300)
ax.grid(True)

def send_data(message):
    sock.sendto(message.encode(), (server_ip, server_port))
    print(f"Sent message: {message}")

def on_key_event(key):
    if key.name == 'up':
        send_data("forward")
    elif key.name == 'down':
        send_data("back")
    elif key.name == 'left':
        send_data("left")
    elif key.name == 'right':
        send_data("right")
    elif key.name == 's':
        send_data("stop")
        

def listen_for_data():
    while True:
        data, _ = sock.recvfrom(1024)
        message = data.decode().strip()
        print(f"Received message: {message}")
        
        angle, distance = map(int, message.split(","))
        num[angle] = distance

def update_plot(frame):
    for i, line in enumerate(lines):
        if num[i] > 0:
            x = [0, num[i] * np.cos(np.radians(i))]
            y = [0, num[i] * np.sin(np.radians(i))]
            line.set_data(x, y)
        else:
            line.set_data([], [])
    
    x_scatter = [num[i] * np.cos(np.radians(i)) for i in range(181) if num[i] > 0]
    y_scatter = [num[i] * np.sin(np.radians(i)) for i in range(181) if num[i] > 0]
    scatter.set_offsets(np.column_stack((x_scatter, y_scatter)))
    
    max_distance = max(num) if max(num) > 0 else 300
    ax.set_xlim(-max_distance, max_distance)
    ax.set_ylim(0, max_distance)

# Start the data listener in a separate thread
data_thread = threading.Thread(target=listen_for_data)
data_thread.daemon = True
data_thread.start()

keyboard.on_press(on_key_event)
print("Press the arrow keys to control the motors. Press 'esc' to exit.")

# Start the animation
ani = FuncAnimation(fig, update_plot, interval=100)

# Show the plot window
plt.show(block=True)

# Keep the script running
try:
    keyboard.wait('esc')
except KeyboardInterrupt:
    pass
finally:
    sock.close()
