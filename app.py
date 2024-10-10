import csv
import streamlit as st
import pandas as pd
import os
from datetime import datetime
import cv2
import pygame
from utils import generate_link_qr,gen_wifi_qr,set_hotspot,get_wifi_interface,get_ip,list_wifi_networks,read_config_yaml,img_to_base64
import requests

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

config = read_config_yaml('config.yaml')
BARCODE_HISTORY = config['BARCODE_HISTORY']
BARCODE_STATUS = config['BARCODE_STATUS']
BARCODE_RESET = config['BARCODE_RESET']
BARCODE_CLEAR = config['BARCODE_CLEAR']
BARCODE_SETTING = config['BARCODE_SETTING']
WEAPON_DATA_PATH = config['WEAPON_DATA_PATH']
PERSON_DATA_PATH = config['PERSON_DATA_PATH']
HISTORY_DATA_PATH = config['HISTORY_DATA_PATH']
UNIT_NAME = config['UNIT_NAME']
LOGO_PATH = config['LOGO_PATH']
LINE_TOKENS = []
for i in range(1,4):
    if config[f'LINE_TOKEN{i}']:
        LINE_TOKENS.append(config[f'LINE_TOKEN{i}'])

if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "current_weapon" not in st.session_state:
    st.session_state.current_weapon = ""
if "current_person" not in st.session_state:
    st.session_state.current_person = ""


def is_online():
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False
    
def line_noti(line_token, message, image_path=None):
    headers = {
        'Authorization': f'Bearer {line_token}'
    }
    payload = {'message': message}
    files = None
    # Only open the file if an image_path is provided
    if image_path:
        with open(image_path, 'rb') as f:
            files = {'imageFile': f}
            response = requests.post('https://notify-api.line.me/api/notify', headers=headers, data=payload, files=files)
    else:
        response = requests.post('https://notify-api.line.me/api/notify', headers=headers, data=payload)

    return response

def example_header(content):
     st.markdown(f'<p style="font-size:80px;text-align: center;font-weight: bold;">{content}</p>', unsafe_allow_html=True)

def example(color1, color2, color3, content):
     st.markdown(f'<p style="text-align:center; height:60px; font-weight:bold; background-image:linear-gradient(to right,{color1}, {color2});color:{color3}; font-size:36px; border-radius:0%;">{content}</p>', unsafe_allow_html=True)

def toggle_instock(weapon_barcode):
    data = []
    sta = []
    with open(WEAPON_DATA_PATH, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  
        data = [header]  
        for row in reader:
            if row[0] == weapon_barcode:
                if row[4] == 'True':
                    row[4] = 'False'
                elif row[4] == 'False':
                    row[4] = 'True'
                sta = row[4]
            data.append(row)
    
    with open(WEAPON_DATA_PATH, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    return sta

def submit():
    st.session_state.input_text = st.session_state.widget
    st.session_state.widget = ""

#read data
df_weapon = pd.read_csv(WEAPON_DATA_PATH)
df_person = pd.read_csv(PERSON_DATA_PATH)
df_weapon = df_weapon.astype(str)
df_person = df_person.astype(str)

try:
    df_history = pd.read_csv(HISTORY_DATA_PATH)
    df_history = df_history.astype(str)
except:
    df_history = pd.DataFrame(columns=[
        'weapon_barcode', 
        'weapon_id', 
        'weapon_type', 
        'weapon_respon_name', 
        'weapon_respon_id', 
        'person_id', 
        'person_barcode', 
        'person_name', 
        'timestamp', 
        'action'
    ])
    
df_history = df_history.sort_values(by='timestamp',ascending=False)

unique_types = list(df_weapon['type'].unique())

weapons_ins = {}
weapons_outs = {}
for t in unique_types:
    weapons_ins[t] = df_weapon[(df_weapon['instock'] == 'True') & (df_weapon['type'] == t)]['weapon_barcode'].tolist()
    weapons_outs[t] = df_weapon[(df_weapon['instock'] == 'False') & (df_weapon['type'] == t)]['weapon_barcode'].tolist()

# input text
st.sidebar.text_input("scan barcode", key="widget", on_change=submit)
input_text = st.session_state.input_text
st.components.v1.html(
    f"""
    <script>
        // Wait until the DOM is fully loaded
        document.addEventListener('DOMContentLoaded', function() {{
            // Focus on the input field when the page loads
            var inputField = window.parent.document.querySelector('input[type="text"]');
            if(inputField) {{
                inputField.focus();
            }}
        }});
    </script>
    """,
    height=0,
)

## check text input
current_weapon = df_weapon[df_weapon['weapon_barcode']==input_text]
try:
    df_history_current_weapon_barcode = df_history[df_history['weapon_barcode']==st.session_state.current_weapon['weapon_barcode']]
except:
    df_history_current_weapon_barcode = df_history[df_history['weapon_barcode']=='']
current_person = df_person[df_person['person_barcode']==input_text]
if current_weapon.shape[0]==1:
    st.session_state.current_weapon = dict(current_weapon.iloc[0])
if current_person.shape[0]==1:
    st.session_state.current_person = dict(current_person.iloc[0])

# history
if input_text == BARCODE_HISTORY or input_text == '1':
    st.title('ประวัติการเบิกจ่ายอาวุธ')
    if st.session_state.current_weapon:

        ims = []
        for i in df_history_current_weapon_barcode['timestamp']:
            image_path = 'data/images/' + i + '.jpg'
            try:
                im = img_to_base64(image_path)
                ims.append(im)
            except:
                ims.append(image_path)
        df_history_current_weapon_barcode['image'] = ims
        cols = ['timestamp'] + [col for col in df_history_current_weapon_barcode.columns if col != 'timestamp']
        df_history_current_weapon_barcode = df_history_current_weapon_barcode[cols]
        st.data_editor(
            df_history_current_weapon_barcode,
            column_config={
                "image": st.column_config.ImageColumn(
                    "Preview Image", help="Streamlit app preview screenshots"
                )
            },
            hide_index=True,
        )
    else:
        ims = []
        for i in df_history['timestamp']:
            image_path = 'data/images/' + i + '.jpg'
            try:
                im = img_to_base64(image_path)
                ims.append(im)
            except:
                ims.append(image_path)
        df_history['image'] = ims
        cols = ['timestamp'] + [col for col in df_history.columns if col != 'timestamp']
        df_history = df_history[cols]
        st.data_editor(
            df_history,
            column_config={
                "image": st.column_config.ImageColumn(
                    "Preview Image", help="Streamlit app preview screenshots"
                )
            },
            hide_index=True,
        )

# status
elif input_text == BARCODE_STATUS or input_text == '2':
    st.title('สถานภาพปัจจุบัน')
    cols = st.columns(len(unique_types))

    for i,col in enumerate(cols):
        with col:
            st.header(unique_types[i])
            st.subheader(f'อาวุธในคลัง {len(weapons_ins[unique_types[i]])} กระบอก')

            df_in = df_weapon[(df_weapon['instock'] == 'True') & (df_weapon['type'] == unique_types[i])]

            person_respon_names = []
            for id in df_in['person_respon_id']:
                prn = df_person[df_person['person_id']==id].iloc[0]['name']
                person_respon_names.append(prn)
            df_in['person_respon_name'] = person_respon_names

            df_in.reset_index(drop=True, inplace=True)  # Reset the index
            df_in.index = df_in.index + 1  # Adjust index to start from 1

            df_in = df_in[['weapon_id','person_respon_name']]
            st.write(df_in)

            st.subheader(f'อาวุธนอกคลัง {len(weapons_outs[unique_types[i]])} กระบอก')
            df_out = df_weapon[(df_weapon['instock'] == 'False') & (df_weapon['type'] == unique_types[i])]
            person_respon_names = []
            for id in df_out['person_respon_id']:
                prn = df_person[df_person['person_id']==id].iloc[0]['name']
                person_respon_names.append(prn)
            df_out['person_respon_name'] = person_respon_names
            df_out.reset_index(drop=True, inplace=True)  # Reset the index
            df_out.index = df_out.index + 1  # Adjust index to start from 1

            try:
                ts = []
                pn = []
                for wid in df_out['weapon_id']:
                    filtered_data = df_history[df_history['weapon_id'] == wid]
                    last_transaction = filtered_data.sort_values(by='timestamp', ascending=False)
                    ts.append(last_transaction.iloc[0]['timestamp'])
                    pn.append(last_transaction.iloc[0]['person_name'])
                df_out['timestamp'] = ts
                df_out['person_name'] = pn
                df_out = df_out[['weapon_id','person_respon_name','person_name','timestamp']]

            except:
                df_out = df_out[['weapon_id','person_respon_name']]

            st.write(df_out)

# reset 
elif input_text == BARCODE_RESET or input_text == 'r':
    df_weapon['instock'] = 'True'
    df_weapon.to_csv(WEAPON_DATA_PATH, index=False)
    st.title('reset complete!!')

# setting
elif input_text == BARCODE_SETTING or input_text == 's':
    st.title('Setting & History')
    wifi_networks,active_ssid = list_wifi_networks() 

    with open('wifi_list.txt', 'w') as file:
        for item in wifi_networks:
            file.write(f"{item}\n")

    interface_name = get_wifi_interface()
    current_ip = get_ip(interface_name)

    st.subheader(f'current_ip {current_ip}')
    if not current_ip:
        set_hotspot("MyHotspot", "abcd1234")
        gen_wifi_qr("MyHotspot", "abcd1234")

        current_ip = get_ip(interface_name)

    cols = st.columns(2)

    if active_ssid == "MyHotspot" or not active_ssid:
        cols[0].subheader('STEP1 : Connect to MyHotspot')
        cols[0].write('ssid: MyHotspot')
        cols[0].write('password: abcd1234')
     
        cols[0].image('qrcode_wifi.png',caption="qrcode_wifi")

    else:
        cols[0].subheader(f'STEP1 : Connect to ssid: {active_ssid}')

    url = f"http://{current_ip}:8509/setting"
    generate_link_qr(url)
    cols[1].subheader(f'STEP2 : Connect to {url}')
    cols[1].image('qrcode_link.png')

# main
else:
    #clear current weapon and person
    if input_text == BARCODE_CLEAR or input_text == 'c':
        st.session_state.current_weapon = ''
        st.session_state.current_person = ''

    # head status
    col1, col2, col3 = st.columns([1,8,1])
    with col1:
        st.image(LOGO_PATH, use_column_width=True)
    with col2:
        example_header(UNIT_NAME)
    with col3:
        pass

    st.markdown("""---""")
    if len(unique_types)==1:
        col1, col2, col3, col4 = st.columns([5,4,3,4])
        col1.title(f':blue[{unique_types[0]}]')
        col2.title(f':blue[ยอดเดิม]')
        col2.title(f':blue[{len(weapons_ins[unique_types[0]]) + len(weapons_outs[unique_types[0]])} กระบอก]')
        col3.title(f':red[เบิก]')
        col3.title(f':red[{len(weapons_outs[unique_types[0]])} กระบอก]')
        col4.title(f'คงเหลือ')
        col4.title(f'{len(weapons_ins[unique_types[0]])} กระบอก')

    else:
        for t in unique_types:

            col1, col2, col3, col4 = st.columns([5,4,3,4])
            col1.title(f':blue[{t}]')
            col2.title(f':blue[ยอดเดิม {len(weapons_ins[t]) + len(weapons_outs[t])}]')
            col3.title(f':red[เบิก {len(weapons_outs[t])}]')
            col4.title(f'คงเหลือ {len(weapons_ins[t])}')

    st.markdown("""---""")

    # current weapon person id
    col11, col22 = st.columns(2)
    with col11:
        st.subheader(':green[อาวุธ]')
        if st.session_state.current_weapon:
            st.title(f":red[{st.session_state.current_weapon['weapon_id']}]")
            weapon_respon_id = st.session_state.current_weapon['person_respon_id']
            try:
                weapon_respon_name = df_person[df_person['person_id']==weapon_respon_id].iloc[0]['name']
            except:
                weapon_respon_name = 'ไม่ปรากฎชื่อผู้รับผิดชอบ'
            st.write(f"{weapon_respon_name} ({weapon_respon_id})")

        else:
            st.write('--')
    with col22:
        st.subheader(':green[ผู้เบิก]')
        if st.session_state.current_person:
            st.title(f":red[{st.session_state.current_person['name']}]")
    
        else:
            st.write('--')

    st.markdown("""---""")

    #show current status text
    sta = 'โปรดสแกนอาวุธ และบัตรประจำตัว'
    if st.session_state.current_weapon and st.session_state.current_person:
        sta = 'บันทึกสำเร็จ!!'
    elif st.session_state.current_weapon:
        sta = 'โปรดสแกนบัตรประจำตัว'
    elif st.session_state.current_person:
        sta = 'โปรดสแกนอาวุธ'

    example('#ff6320','#eaff2f','#000000',sta)

    # complete state
    if st.session_state.current_weapon and st.session_state.current_person:
        isin = toggle_instock(st.session_state.current_weapon['weapon_barcode'])
        if isin == 'True':
            action = 'in'
        else:
            action = 'out'

        #save data to csv
        data = {
            'weapon_barcode' : st.session_state.current_weapon['weapon_barcode'],
            'weapon_id' : st.session_state.current_weapon['weapon_id'],
            'weapon_type' : st.session_state.current_weapon['type'],
            'weapon_respon_name' : weapon_respon_name,
            'weapon_respon_id' : weapon_respon_id,
            'person_id' : st.session_state.current_person['person_id'],
            'person_barcode' : st.session_state.current_person['person_barcode'],
            'person_name' : st.session_state.current_person['name'],
            'timestamp' : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'action' : action
        }

        file_path = HISTORY_DATA_PATH
        file_exists = os.path.isfile(file_path)
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(data.keys())  # Write the header row
            writer.writerow(data.values())

        # if st.button("Foo"):
        st.session_state.current_weapon = ''
        st.session_state.current_person = ''
        st.session_state.history_current_weapon_barcode = ''
        st.session_state.input_text = ''

        #capture image
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open camera.")
            exit()
        ret, frame = cap.read()
        image_path = None
        if ret:
            directory = 'data/images'
            if not os.path.exists(directory):
                os.makedirs(directory)
            image_path = f"{directory}/{data['timestamp']}.jpg"
            cv2.imwrite(image_path, frame)
        cap.release()

        #line noti
        if is_online():
            for line_token in LINE_TOKENS:
                message = f"\nหมายเลขปืน: {data['weapon_id']}\n"
                message += f"ชนิด: {data['weapon_type']}\n"
                message += f"ผู้รับผิดชอบปืน: {data['weapon_respon_name']}\n"
                message += f"ผู้เบิก : {data['person_name']}\n"
                line_noti(line_token,message,image_path)
            

        #voice
        pygame.mixer.init()
        if action == 'in':
            pygame.mixer.music.load("data/voices/in.mp3")
        else:
            pygame.mixer.music.load("data/voices/out.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)              

        st.rerun()






