NOTE: we have redacted our private_key.json (for GOOGLE_APPLICATION_CREDENTIALS) and the telegram token  
  
if you want to test our app, message https://t.me/NSBuddyPythonbot. We will keep our server running from 15-17 June from 9am to 11pm.  
  
if you want to run this code, you will have to create a dialogflow project, import dialogflow.zip and download a service account key from the google cloud console. You will also need to create a telegram bot using https://t.me/botfather and copy the token into the python script.

Set up virtual environment:
```
cd NSBuddy
python -m pip install --upgrade pip
python -m pip install --user virtualenv
python -m venv env
```
Activate virtual environment (Windows users):
```
.\env\Scripts\activate
```
Activate virtual environment (MacOS users):
```
source ./env/bin/activate
```
Install dependencies
```
python -m pip install --no-deps -r requirements.txt
```  
Run the server:
```
cd NSBuddy
.\env\Scripts\activate
NSBuddy_telegram.py  
```
