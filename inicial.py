import os
import shutil
import time
import requests
import sys

time.sleep(10)

internet = 'google.com'

rep = os.system('ping -i 1 -c 3  ' + internet)

if rep == 0:
    print ('Connected to the internet!')
else:
    print ('No internet connection!')
    sys.exit()

os.chdir("/home/pi/")
os.system("sudo apt-get install git")

dht_lib = os.path.exists("./Adafruit_Python_DHT")

if(dht_lib):
    shutil.rmtree("Adafruit_Python_DHT")

os.system("git clone https://github.com/adafruit/Adafruit_Python_DHT.git")
os.chdir("/home/pi/Adafruit_Python_DHT")
os.system("sudo python setup.py install")

os.chdir("/home/pi/")

requests_lib = os.path.exists("./requests")

if(requests_lib):
    shutil.rmtree("requests")

os.system("git clone git://github.com/kennethreitz/requests.git")
os.chdir("/home/pi/requests")
os.system("sudo python setup.py install")

os.chdir("/home/pi/")

vinos_lib = os.path.exists("./VinusIOT")

if(vinos_lib):
    shutil.rmtree("VinusIOT")

os.system("git clone https://github.com/joaomateusferr/VinusIOT.git")

os.system("sudo apt-get install python-rpi.gpio python3-rpi.gpio")

os.system("clear")

print("All downloads and updates done!\n")     

url_login = 'http://ec2-18-228-191-79.sa-east-1.compute.amazonaws.com:8080/api/login'

print("Fill in the Vinos data!")

email = raw_input('Email: ')
password = raw_input('Password: ')

payload = "{\n\t\"email\": \""+ email +"\",\n\"password\": \""+ password +"\"\n}"
headers = {'Content-Type': "application/json",'cache-control': "no-cache"}

api = 'http://ec2-18-228-191-79.sa-east-1.compute.amazonaws.com'

rep = os.system('ping -i 1 -c 3  ' + api)

if rep == 0:
    print ('API online!')
else:
    print ('API offline!\nTry agan later!')
    sys.exit()

try:
    response = requests.request("POST", url_login, data = payload, headers = headers)

except:
    print("Login Response Error\n")

token = '**************'

os.chdir("/home/pi/VinusIOT/")
token_file = open("token.txt", "w+")
token_file.write(token)
token_file.close()

#devices = response.text

#selecionar qual dispositivo sera usado para gerar a ulr

url_device = 'aaaaaaaaaaa'

url_file = open("url.txt", "w+")
url_file.write(url_device)
url_file.close()

os.system("sudo echo '#!/bin/sh -e' | sudo tee /etc/rc.local")
os.system("sudo echo '#Startup' | sudo tee -a /etc/rc.local")
os.system("sudo echo 'sudo python /home/pi/VinosIOT/code.py &' | sudo tee -a /etc/rc.local")
os.system("sudo echo 'exit 0' | sudo tee -a /etc/rc.local")

os.system("sudo raspi-config nonint do_boot_behaviour B2")
os.system("sudo reboot")
