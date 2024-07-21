import socket
import matplotlib.pyplot as plt
import numpy as np

# UDP setup
local_ip = "0.0.0.0"  # Listen on all interfaces
local_port = 8888

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((local_ip, local_port))

num = [0] * 181  # Initialize with 181 zeros (0 to 180 degrees)
inc = 1

plt.ion()  # Enable interactive mode
fig, ax = plt.subplots(figsize=(12, 8))
lines = [ax.plot([], [], 'b-')[0] for _ in range(181)]  # Create a line for each angle
scatter = ax.scatter([], [], c='r', s=20)  # Empty scatter plot for points
ax.set_aspect('equal')
ax.set_xlabel('X (cm)')
ax.set_ylabel('Y (cm)')
ax.set_title('Ultrasonic Sensor Mapping')

# Set initial plot limits
ax.set_xlim(-300, 300)
ax.set_ylim(0, 300)
ax.grid(True)

# Show the plot
plt.show(block=False)
plt.pause(0.1)  # Pause to render the plot

print("Waiting for data from Arduino...")

try:
    while True:
        data, _ = sock.recvfrom(1024)  # Buffer size is 1024 bytes
        message = data.decode().strip()
        print(f"Received message: {message}")
        
        angle, distance = map(int, message.split(","))
        num[angle] = distance  # Update the distance at the specific angle
        
        # Update the plot
        for i, line in enumerate(lines):
            if num[i] > 0:  # Only plot if we have a non-zero distance
                x = [0, num[i] * np.cos(np.radians(i))]
                y = [0, num[i] * np.sin(np.radians(i))]
                line.set_data(x, y)
            else:
                line.set_data([], [])
        
        # Update the scatter plot
        x_scatter = [num[i] * np.cos(np.radians(i)) for i in range(181) if num[i] > 0]
        y_scatter = [num[i] * np.sin(np.radians(i)) for i in range(181) if num[i] > 0]
        scatter.set_offsets(np.column_stack((x_scatter, y_scatter)))
        
        # Adjust plot limits if necessary
        max_distance = max(num) if max(num) > 0 else 300
        ax.set_xlim(-max_distance, max_distance)
        ax.set_ylim(0, max_distance)
        
        plt.draw()
        plt.pause(0.01)

except KeyboardInterrupt:
    print("Script terminated by user")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    sock.close()
    plt.ioff()
    plt.show()