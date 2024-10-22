# ArmyStock2
## Step1 : set up google sheet
```
setup_tutorial :: https://www.youtube.com/watch?v=r817RLqmLac
sheet url :: https://docs.google.com/spreadsheets/d/1qjwfbjsITCQXcdYV88soR3xk-NBUKpjGTuQ57IWG2Dc/edit?usp=sharing
```
```
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
```
```
# copy google_sheet_url to config.yaml
# copy google_sheet_api to config.yaml
```
## Step2 : set up ubuntu environments
```
#0 install chromium from ubuntu-store
#1 sudo api install git
#2 sudo apt install chromium-browser
#3 sudo api install unclutter

** if can't use streamlit run app.py >> python3 -m streamlit run app.py
```
```
cd /home/phawit/Documents
git https://github.com/phawitb/ArmyStock2.com](https://github.com/phawitb/ArmyStock2.git
cd /home/phawit/Documents/ArmyStock2
pip install -r equirements.txt

copy run_streamlit_pi.sh to outside ArmyStock2
cd /home/phawit/Documents/
chmod +x run_streamlit.sh
```
## Step3 : Setup Ngrok
```
# https://dashboard.ngrok.com/get-started/setup/linux
curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
	| sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
	&& echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
	| sudo tee /etc/apt/sources.list.d/ngrok.list \
	&& sudo apt update \
	&& sudo apt install ngrok
 ```
```
ngrok config add-authtoken 2nLJwN5SqkrtH9bxLeirZByTgWR_6G3wNZZbWEepxGxtiUZZY
ngrok http http://localhost:8509
```
## Step4 : In Startup Applications
```
# copy run_streamlit.sh to 
/home/phawit/Documents/run_streamlit.sh
```



