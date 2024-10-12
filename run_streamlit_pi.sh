#!/bin/bash

sleep 5

#source /home/phawit/anaconda3/etc/profile.d/conda.sh  # Adjust this path if necessary
#conda activate rifle  # Replace 'your_env_name' with your actual environment name

cd /home/phawit/Documents

URL="8.8.8.8"  # Google Public DNS
if ping -c 1 "$URL" &> /dev/null; then
    echo "online"
    rm -r ArmyStock2
    sleep 1
    git clone https://github.com/phawitb/ArmyStock2.git
    sleep 3
fi

cd /home/phawit/Documents/ArmyStock2
python3 load_data_from_googlesheet.py

sleep 3

python3 -m streamlit run app.py --server.headless true --server.port 8509 &

sleep 5

chromium-browser --start-fullscreen http://localhost:8509
