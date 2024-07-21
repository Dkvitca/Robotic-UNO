import socket
import keyboard 

# UDP setup
server_ip = "192.168.1.132"  # Arduino IP address
server_port = 8888

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_data(message):
    sock.sendto(message.encode(), (server_ip, server_port))
    print(f"Sent message: {message}")

def on_key_event(key):
    if key.name == 'up':
        send_data("forward")  # Send command to rotate clockwise

    elif key.name == 'down':
        send_data("back")  # Send command to rotate counterclockwise

    elif key.name == 'left':
        send_data("left")  # Send command to stop

    elif key.name == 'right':
        send_data("right")  # Send command to stop

    elif key.name == 's':
        send_data("stop")  # Send command to stop

# Hook the keyboard events
keyboard.on_press(on_key_event)

print("Press the arrow keys to control the motors. Press 'esc' to exit.")

# Keep the script running
try:
    keyboard.wait('esc')
except KeyboardInterrupt:
    pass
finally:
    # Cleanup
    sock.close()


