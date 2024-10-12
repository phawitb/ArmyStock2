import subprocess
import re
import qrcode
import yaml
import base64

# generate_link_qr,gen_wifi_qr,set_hotspot,get_wifi_interface,get_ip,list_wifi_networks,connect_to_wifi,read_config_yaml,img_to_base64

def img_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    data_url = f"data:image/png;base64,{encoded_string}"
    return data_url

def read_config_yaml(file_path):
    with open(file_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config

def generate_link_qr(url, filename="qrcode_link.png"):
    qr = qrcode.QRCode(
        version=1,  # Controls the size of the QR code (1 is the smallest)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
        box_size=10,  # Size of the box where the QR code is displayed
        border=4,  # Size of the border (in boxes)
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(filename)
    # print(f"QR code generated and saved as {filename}")

def gen_wifi_qr(ssid,password):
    encryption = "WPA"  # Encryption type: WPA, WEP, or leave blank for no encryption

    wifi_format = f"WIFI:S:{ssid};T:{encryption};P:{password};;"

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(wifi_format)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.save("qrcode_wifi.png")

def set_hotspot(ssid, password, interfaces):
    try:
        # Turn on Wi-Fi (just in case it's off)
        subprocess.run(["nmcli", "radio", "wifi", "on"], check=True)
        
        # Set up the hotspot
        subprocess.run([
            "nmcli", "device", "wifi", "hotspot", 
            "ifname", interfaces,  # Replace 'wlan0' wlp4s0 with your Wi-Fi interface name
            "con-name", "MyHotspot", 
            "ssid", ssid, 
            "band", "bg",  # Use 'bg' for 2.4GHz band, 'a' for 5GHz if supported
            "password", password
        ], check=True)

        print(f"Hotspot '{ssid}' is set up successfully.")
        
    except subprocess.CalledProcessError as e:
        print(f"Failed to set up hotspot: {e}")

def get_wifi_interface():
    try:
        # Execute ifconfig command to get the network interfaces
        result = subprocess.run(['ifconfig'], capture_output=True, text=True)

        # Check if the command executed successfully
        if result.returncode != 0:
            return f"Error executing ifconfig: {result.stderr}"

        # Regex to find the wireless interface (interface name starts with 'wl')
        #ubuntu pc
        interfaces = re.findall(r'(^wlp\S+): flags', result.stdout, re.MULTILINE)
        if not interfaces:
            # rasberry pi
            interfaces = re.findall(r'(^wlan0): flags', result.stdout, re.MULTILINE)
        
        if interfaces:
            return interfaces[0]
        else:
            return None
    except Exception as e:
        return f"An error occurred: {str(e)}"

def get_ip(interface_name):
    ifconfig_output = subprocess.check_output("ifconfig", text=True)
    # interface_name = "wlp4s0"
    pattern = rf'{interface_name}.*?inet (\d+\.\d+\.\d+\.\d+)'

    match = re.search(pattern, ifconfig_output, re.DOTALL)

    ip_address = None
    if match:
        ip_address = match.group(1)
        print("IP Address for", interface_name, ":", ip_address)
    else:
        print(f"No IP address found for {interface_name}.")

    return ip_address

def list_wifi_networks():
    result = subprocess.run(['nmcli', '-t', '-f', 'SSID', 'dev', 'wifi'], capture_output=True, text=True)
    
    if result.returncode == 0:
        wifi_networks = result.stdout.strip().split('\n')
        wifi_networks = [ssid for ssid in wifi_networks if ssid]
    else:
        return "Error occurred: " + result.stderr
    
    current_connection = subprocess.run(['nmcli', '-t', '-f', 'NAME', 'connection', 'show', '--active'], capture_output=True, text=True)
    
    if current_connection.returncode == 0:
        #for ubuntupc
        active_ssid = current_connection.stdout.strip()
        active_ssid = active_ssid.split("\n")

        if len(active_ssid) < 3:
            active_ssid = None
        elif len(active_ssid) == 3:
            active_ssid = active_ssid[0]

        #for rasberry pi
        if not active_ssid:
            active_ssid = current_connection.stdout.strip()

    return wifi_networks,active_ssid

def connect_to_wifi(ssid, password):
    # Command to add the Wi-Fi connection
    command = ['nmcli', 'dev', 'wifi', 'connect', ssid, 'password', password]

    try:
        # Run the command
        result = subprocess.run(command, capture_output=True, text=True)

        # Check if the connection was successful
        if result.returncode == 0:
            return f"Successfully connected to {ssid}."
        else:
            return f"Failed to connect to {ssid}. Error: {result.stderr}"
    except Exception as e:
        return f"An error occurred: {str(e)}"
    

# connect_to_wifi("Botan_2.4GHz", "Abcd1234")