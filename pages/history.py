import streamlit as st
import pandas as pd
from utils import read_config_yaml,img_to_base64

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
HISTORY_DATA_PATH = config['HISTORY_DATA_PATH']
WEAPON_DATA_PATH = config['WEAPON_DATA_PATH']

st.title('ประวัติการเบิกจ่ายอาวุธ')

current_weapon_id = st.text_input("weapon id or weapon barcode")

#read data
df_weapon = pd.read_csv(WEAPON_DATA_PATH)
df_weapon = df_weapon.astype(str)

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

if current_weapon_id:
    try:
        x = df_weapon[df_weapon['weapon_id']==current_weapon_id]
        current_weapon_barcode = x.iloc[0]['weapon_barcode']

        df_history_current_weapon_barcode = df_history[df_history['weapon_barcode']==current_weapon_barcode]
    except:
        try:
            df_history_current_weapon_barcode = df_history[df_history['weapon_barcode']==current_weapon_id]
        except:
            df_history_current_weapon_barcode = df_history[df_history['weapon_barcode']=='']

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


