import streamlit as st
import yaml
from utils import list_wifi_networks,connect_to_wifi
import subprocess
import time 
import os

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)

def get_active_connections():
    try:
        # Get the list of active connections
        result = subprocess.run("nmcli connection show --active", shell=True, check=True, stdout=subprocess.PIPE)
        active_connections = result.stdout.decode().splitlines()
        return active_connections
    except subprocess.CalledProcessError as e:
        print(f"Error fetching active connections: {e}")
        return []

def turn_off_hotspot(connection_name):
    try:
        # Command to disable the Wi-Fi hotspot
        command = f"nmcli connection down id '{connection_name}'"
        subprocess.run(command, shell=True, check=True)
        print(f"Wi-Fi hotspot '{connection_name}' has been turned off.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to turn off the hotspot: {e}")

def update_config(key,value):
    with open('../data/config.yaml', 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    config[key] = value
    with open('../data/config.yaml', 'w', encoding='utf-8') as file:
        yaml.safe_dump(config, file, allow_unicode=True)
    print("UNIT_NAME updated successfully!")


st.title('Wifi')

#save current wifi list
wifi_networks,current_wifi = list_wifi_networks()
if current_wifi != "MyHotspot" or not os.path.exists('wifi_list.txt'):
    with open('wifi_list.txt', 'w') as file:
        for item in wifi_networks:
            file.write(f"{item}\n")

with open('wifi_list.txt', 'r') as file:
    wifi_list = [line.strip() for line in file]
# st.write('wifi_list',wifi_list)

list_wifis,current_wifi  = list_wifi_networks()
st.subheader(f'current wifi : {current_wifi}')

# if st.button("setup Wifi"):
if current_wifi:
    if current_wifi == "MyHotspot" or current_wifi == "MyHotspot":
        wifi_ssid_selected = st.selectbox("wifi ssid",wifi_list)
    else:

        if current_wifi in set(list_wifis):
            list_wifis.remove(current_wifi)
            list_wifis.insert(0, current_wifi)
        wifi_ssid_selected = st.selectbox("wifi ssid",list_wifis)
else:
    wifi_ssid_selected = st.selectbox("wifi ssid",['select wifi ssid'] + list_wifis)

wifi_password_selected = st.text_input('wifi password')

if st.button("connect"):
    if current_wifi == "MyHotspot":
        # turn off wifi hotspot
        connections = get_active_connections()
        for connection in connections:
            if "Hotspot" in connection:
                connection_name = connection.split()[0]
                turn_off_hotspot(connection_name)
                break
        else:
            print("No active Wi-Fi hotspot found.")
        time.sleep(5)
            
    st.write("Please refresh setting page in kiosk for check connection")
    connect_to_wifi(wifi_ssid_selected,wifi_password_selected)

    list_wifis,current_wifi  = list_wifi_networks()
    if current_wifi == wifi_ssid_selected:
        st.write(f'success connect to {wifi_ssid_selected}')
    else:
        st.write('Fail')


st.title('Setting')

with open('../data/config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)


if config['CHECK_MATCH']:
    index = 0
else:
    index = 1
setting_match = st.radio(
    "ตั้งค่าชื่อผู้รับผิดชอบกับผู้เบิก",
    ["ต้องตรงกัน", "ไม่จำเป็นต้องต้องกัน"],
    index=index
)
unit_name = st.text_input('unit name',config['UNIT_NAME'])
line_token1 = st.text_input('line token1',config['LINE_TOKEN1'])
line_token2 = st.text_input('line token2',config['LINE_TOKEN2'])
line_token3 = st.text_input('line token3',config['LINE_TOKEN3'])

GOOGLE_SHEET_API = st.text_input('google sheet api',config['GOOGLE_SHEET_API'])
GOOGLE_SHEET_URL = st.text_input('google sheet url',config['GOOGLE_SHEET_URL'])

if st.button('update'):
    config['UNIT_NAME'] = unit_name
    config['LINE_TOKEN1'] = line_token1
    config['LINE_TOKEN2'] = line_token2
    config['LINE_TOKEN3'] = line_token3
    config['GOOGLE_SHEET_API'] = GOOGLE_SHEET_API
    config['GOOGLE_SHEET_URL'] = GOOGLE_SHEET_URL

    if setting_match == "ต้องตรงกัน":
        config['CHECK_MATCH'] = True
    else:
        config['CHECK_MATCH'] = False

    with open('../data/config.yaml', 'w', encoding='utf-8') as file:
        yaml.safe_dump(config, file, allow_unicode=True)
    st.write("updated successfully!")



# setting_match = st.radio(
#     "ตั้งค่าชื่อผู้รับผิดชอบกับผู้เบิก",
#     ["ต้องตรงกัน", "ไม่จำเป็นต้องต้องกัน"],
# )

# if setting_match == "ต้องตรงกัน":
#     st.write("You selected comedy.")
# else:
#     st.write("You didn't select comedy.")



# config[key] = value
#     with open('../data/config.yaml', 'w', encoding='utf-8') as file:
#         yaml.safe_dump(config, file, allow_unicode=True)
#     print("UNIT_NAME updated successfully!")


# st.write(unit_name)
# update_config('UNIT_NAME',unit_name)





