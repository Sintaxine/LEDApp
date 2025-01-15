import time
import network
import socket
from machine import Pin
led_pin = Pin(1, Pin.OUT)
import time
from machine import Pin

led_pin = Pin(1, Pin.OUT)
led_pin.off()


morse_code = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.", "G": "--.", "H": "....",
    "I": "..", "J": ".---", "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---", "P": ".--.",
    "Q": "--.-", "R": ".-.", "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
    "Y": "-.--", "Z": "--..",
    "1": ".----", "2": "..---", "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...",
    "8": "---..", "9": "----.", "0": "-----"
}


def blink_morse(code):
    for symbol in code:
        if symbol == ".":
            led_pin.on()
            time.sleep(0.5)  #dot
            led_pin.off()
        elif symbol == "-":
            led_pin.on()
            time.sleep(1.5)  #dash
            led_pin.off()
        time.sleep(0.5) 
    time.sleep(1)

def blinkstring(string):
    for char in string:
        if char in morse_code:
            blink_morse(morse_code[char])
        
        else:
            pass

ssid = "yourssid"
password = "yourpassword"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    time.sleep(1)

ip_address = wlan.ifconfig()[0]

print("Connected to Wi-Fi network",ssid)
print("IP Address:", ip_address)

html = """
<!DOCTYPE html>
<html>
<head>
    <title>LED Control</title>
    <style>
        body { text-align: center; font-family: Arial, sans-serif; margin-top: 50px; }
        button { padding: 10px 20px; font-size: 20px; margin: 20px; cursor: pointer; }
        input { padding: 10px 20px; font-size: 20px; margin: 20px; }
    </style>
</head>
<body>
    <h1>Control LED</h1>
    <button onclick="location.href='/set_led/on'">Turn LED On</button>
    <button onclick="location.href='/set_led/off'">Turn LED Off</button>
    <p id="statusIndicator">LED Status: OFF</p>

    <!-- Form to get user input -->
    <form action="/submit_input" method="GET">
        <label for="userInput">Enter some text to be converted into morse code:</label>
        <input type="text" id="userInput" name="userInput" placeholder="Type something...">
        <button type="submit">Submit</button>
    </form>

    <script>
        var statusText = document.getElementById("statusIndicator");
        if(location.href.includes("set_led/on")) {
            statusText.textContent = "LED Status: ON";
        }
            
        if(location.href.includes("set_led/off")) {
            statusText.textContent = "LED Status: OFF";
        }
    </script>
</body>
</html>
"""

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print("Listening on", addr)

while True:
    cl, addr = s.accept()
    print('Client connected from', addr)
    request = cl.recv(1024)
    request = str(request)

 
    if '/set_led/on' in request:
        led_pin.on()  
    elif '/set_led/off' in request:
        led_pin.off()  
    elif '/submit_input' in request:
        start_index = request.find("?userinput=") + len("?userinput=")
        end_index = request.find("end")
        if start_index != -1 and end_index != -1:
            user_input = request[start_index:end_index].strip()
        try:
            user_input2 = user_input[user_input.find("=") + 1:]
            if len(user_input2) < 14:
                try:
                    print("User input received:", user_input2)
                    print("Blinking morse code.")
                    blinkstring(user_input2)
                    print("Done! No errors reported.")
                except Exception as e:
                    print("Failed! userinput probably invalid. Error code:",e)
        except Exception as e:
            print("Something went wrong.", e)
    cl.send('HTTP/1.1 200 OK\r\n')
    cl.send('Content-Type: text/html\r\n\r\n')
    cl.send(html)
    cl.close()

