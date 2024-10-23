import streamlit as st
import pandas as pd
from utils import read_config_yaml

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

config = read_config_yaml('../data/config.yaml')

PERSON_DATA_PATH = config['PERSON_DATA_PATH']
HISTORY_DATA_PATH = config['HISTORY_DATA_PATH']

WEAPON_DATA_PATH = config['WEAPON_DATA_PATH']

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
            #append timestamp and person data from history.csv
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