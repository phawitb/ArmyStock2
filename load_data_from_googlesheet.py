""" 
setup_tutorial :: https://www.youtube.com/watch?v=r817RLqmLac
sheet url :: https://docs.google.com/spreadsheets/d/1qjwfbjsITCQXcdYV88soR3xk-NBUKpjGTuQ57IWG2Dc/edit?usp=sharing
code.gs :: 
function doGet(e) {
  var action = e.parameter.action;

  if (action == 'getAllWeaponData') {
    return getAllWeaponData();  // Return all weapon data
  }
  
  if (action == 'getAllPersonData') {
    return getAllPersonData();  // Return all person data
  }
}

// Function to retrieve all weapon data
function getAllWeaponData() {
  var sheet_weapon = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('weapon_data');
  var rows = sheet_weapon.getRange(2, 1, sheet_weapon.getLastRow() - 1, sheet_weapon.getLastColumn()).getValues();
  var data = [];

  // Loop through rows and build JSON object for each
  for (var i = 0; i < rows.length; i++) {
    var row = rows[i];
    var record = {
      "weapon_barcode": row[0],
      "weapon_id": row[1],
      "type": row[2],
      "person_respon_id": row[3],
      "instock": row[4]
    };
    data.push(record);
  }

  var result = JSON.stringify(data);
  return ContentService.createTextOutput(result).setMimeType(ContentService.MimeType.JSON);
}

// Function to retrieve all person data
function getAllPersonData() {
  var sheet_person = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('person_data');
  var rows = sheet_person.getRange(2, 1, sheet_person.getLastRow() - 1, sheet_person.getLastColumn()).getValues();
  var data = [];

  // Loop through rows and build JSON object for each
  for (var i = 0; i < rows.length; i++) {
    var row = rows[i];
    var record = {
      "person_barcode": row[0],
      "person_id": row[1],
      "name": row[2]
    };
    data.push(record);
  }

  var result = JSON.stringify(data);
  return ContentService.createTextOutput(result).setMimeType(ContentService.MimeType.JSON);
}


"""

import os
import requests
import pandas as pd
import yaml

def read_config_yaml(file_path):
    with open(file_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config

config = read_config_yaml('config.yaml')
WEAPON_DATA_PATH = config['WEAPON_DATA_PATH']
PERSON_DATA_PATH = config['PERSON_DATA_PATH']

url = 'https://script.google.com/macros/s/AKfycbytyWzAyEr5SGa6I8qqUgErLiFW6bMQcSloBNy-TgpboYmRuG5ToksfmQ7dsx4uHVqk4w/exec'

def fetch_data(action):
    
    params = {
        'action': action 
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return pd.DataFrame(data)
    else:
        print(f"Error fetching {action}: {response.status_code}")
        return None

def update_weapon_data():
    df_new_weapon = fetch_data('getAllWeaponData')
    print('df_new_weapon',df_new_weapon)

    if df_new_weapon is not None:
        if os.path.exists(WEAPON_DATA_PATH):
            df_new_weapon.to_csv(WEAPON_DATA_PATH, index=False)
            print("weapon_data.csv updated successfully!")
        else:
            df_new_weapon.to_csv(WEAPON_DATA_PATH, index=False)
            print("weapon_data.csv created successfully!")

def update_person_data():
    df_new_person = fetch_data('getAllPersonData')
    print('df_new_person',df_new_person)

    if df_new_person is not None:
        if os.path.exists(PERSON_DATA_PATH):
            df_new_person.to_csv(PERSON_DATA_PATH, index=False)
            print("person_data.csv updated successfully!")
        else:
            df_new_person.to_csv(PERSON_DATA_PATH, index=False)
            print("person_data.csv created successfully!")

def main():
    update_weapon_data()
    update_person_data()

if __name__ == '__main__':
    main()



