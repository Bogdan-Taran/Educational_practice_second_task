#Check Python
*Windows*
```bash
python --version
```
*Ubuntu*
```bash
python3 --version
```
```bash
sudo apt update && sudo apt install python3 python3-pip python3-venv -y
```



#Create venv
*Win*
``` bash
python -m venv .venv
```
*Ubuntu*
``` bash
python3 -m venv .venv
```



#Activate venv
*Win*
``` bash
.venv\Scripts\activate.bat
```
*Ubuntu*
```bash
source venv/bin/activate
```


#Download all packages:
*Win, ubuntu*
```bash
pip install -r requirements.txt
```
#Check Django
```bash
python -m django --version
```


#Run server on different port 
```bash
python manage.py runserver 8089
```

All users and their login information are located in the file Users.txt
