# ArmyStock2
## Step0 : setup google sheet All
```
setup_tutorial :: https://www.youtube.com/watch?v=r817RLqmLac
```
```
#https://docs.google.com/spreadsheets/d/1kAkUNRKKrgq1DXgAogc5nz43pcYL95n6DwQIqL8x4Es/edit?usp=sharing
https://script.google.com/macros/s/AKfycbwCwmDCVZto2usXx4SR0nYvCPqaLRJWfTxXDEQmNFkIgFgyO1eOLvEsglYhGzbnSi3m/exec
{
    "unit": "Unit1",
    "type": "TypeA",
    "in": 101,
    "out": 50,
    "total": 150,
    "url": "https://example.com",
    "sheet_url": "https://example.com2"
}
```
```
code.gs
function doGet() {
  return getAllData();
}

function getAllData() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
  var dataRange = sheet.getDataRange();
  var data = dataRange.getValues();
  
  // Get headers from the first row
  var headers = data[0];
  
  // Create array of objects where keys are the headers and values are the row data
  var jsonData = [];
  for (var i = 1; i < data.length; i++) {
    var rowData = {};
    for (var j = 0; j < headers.length; j++) {
      rowData[headers[j]] = data[i][j];
    }
    jsonData.push(rowData);
  }
  
  // Return the JSON response
  return ContentService.createTextOutput(JSON.stringify(jsonData))
                       .setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  try {
    // Parse the incoming POST data as JSON
    var data = JSON.parse(e.postData.contents);
    
    var unit = data.unit;
    var type = data.type;
    
    // Use the current time for the timestamp
    var currentTimestamp = new Date().toLocaleString(); 
    
    // Call the function to update or append data
    updateOrAppendData(unit, type, {
      in: data.in || null,   // If data.in is not provided, use null
      out: data.out || null, // If data.out is not provided, use null
      total: data.total || null, // If data.total is not provided, use null
      timestamp: currentTimestamp, // Always update timestamp
      url: data.url || null, // If data.url is not provided, use null
      sheet_url: data.sheet_url || null // If sheet_url is not provided, use null
    });
    
    // Return success message
    return ContentService.createTextOutput("Data has been updated or added.").setMimeType(ContentService.MimeType.TEXT);
  } catch (error) {
    // Return error message if something goes wrong
    return ContentService.createTextOutput("Error: " + error.message).setMimeType(ContentService.MimeType.TEXT);
  }
}

function updateOrAppendData(unit, type, inputData) {
  // Define the sheet and range
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
  var dataRange = sheet.getDataRange();
  var dataValues = dataRange.getValues();
  
  var headers = dataValues[0]; // Assume the first row is the header
  var unitCol = headers.indexOf('unit');
  var typeCol = headers.indexOf('type');
  var inCol = headers.indexOf('in');
  var outCol = headers.indexOf('out');
  var totalCol = headers.indexOf('total');
  var timestampCol = headers.indexOf('timestamp');
  var urlCol = headers.indexOf('url');
  var sheetUrlCol = headers.indexOf('sheet_url'); // New sheet_url column

  var found = false;
  
  // Loop through rows to check if 'unit' and 'type' match
  for (var i = 1; i < dataValues.length; i++) {
    var row = dataValues[i];
    if (row[unitCol] === unit && row[typeCol] === type) {
      // Update the row, but keep existing values if inputData fields are null
      if (inputData.in !== null) sheet.getRange(i + 1, inCol + 1).setValue(inputData.in);
      if (inputData.out !== null) sheet.getRange(i + 1, outCol + 1).setValue(inputData.out);
      if (inputData.total !== null) sheet.getRange(i + 1, totalCol + 1).setValue(inputData.total);
      
      // Always update the timestamp (current time)
      sheet.getRange(i + 1, timestampCol + 1).setValue(inputData.timestamp);
      
      if (inputData.url !== null) sheet.getRange(i + 1, urlCol + 1).setValue(inputData.url);
      if (inputData.sheet_url !== null) sheet.getRange(i + 1, sheetUrlCol + 1).setValue(inputData.sheet_url); // Update sheet_url
      
      found = true;
      break;
    }
  }
  
  // If no matching row is found, append the new data
  if (!found) {
    sheet.appendRow([
      unit, 
      type, 
      inputData.in || "", 
      inputData.out || "", 
      inputData.total || "", 
      inputData.timestamp, 
      inputData.url || "", 
      inputData.sheet_url || "" // Append sheet_url
    ]);
  }
}
```
## Step1 : set up google sheet data
```
// sheet url :: https://docs.google.com/spreadsheets/d/1qjwfbjsITCQXcdYV88soR3xk-NBUKpjGTuQ57IWG2Dc/edit?usp=sharing
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
## Dash Board All
#### https://armyweapon-dashboard.streamlit.app/
```
 code in https://github.com/phawitb/ArmyStock2-Dashboard.git
```


