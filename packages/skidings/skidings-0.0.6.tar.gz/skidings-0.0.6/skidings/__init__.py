import subprocess
import requests
import mysql.connector
import datetime

#Get current hwid
def get_hwid():
    hwid_input = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
    return hwid_input

#Get current ip
def get_ip():
    query = requests.get("https://api.ipify.org")
    ip = (query.text)
    return ip

#Hwid check using pastebin
def check_hwid(paste_url,hwid):
    current_hwid = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()

    query = requests.get(paste_url)
    pastebin = (query.text)

    if current_hwid in pastebin:
        return True
    else:
        return False

#Username check using pastebin
def check_user(paste_url,username):
    username_query = requests.get(paste_url)
    username_name = (username_query.text)
    
    if username in username_name:
        return True
    else:
        return False

#Password check using pastebin
def check_password(paste_url,password):
    password_query = requests.get(paste_url)
    password_password = (password_query.text)

    if password in password_password:
        return True
    else:
        return False

#Ip Check using pastebin
def check_ip(paste_url):
    ip_query = requests.get(paste_url)
    ip_ip = (ip_query.text)

    ip_query2 = requests.get("https://api.ipify.org")
    ip = (ip_query2.text)

    if ip in ip_ip:
        return True
    else:
        return False 

#Send http Requests
def send_request(url):
    request = requests.get(url)
    return (request.text)

#Getting data without using index's
def get_sql_data(host_name,user_name,pass_word,db_name,query):

    mydb = mysql.connector.connect(
        host=f"{host_name}",
        user=f"{user_name}",
        passwd=f"{pass_word}",
        database=f"{db_name}"
    )

    cursor = mydb.cursor()
    cursor.execute(query)
    data = cursor.fetchall()

    return data[0]

#Getting data using index's
def fetch_sql_data(host_name,user_name,pass_word,db_name,query,index1,index2):

    mydb = mysql.connector.connect(
        host=f"{host_name}",
        user=f"{user_name}",
        passwd=f"{pass_word}",
        database=f"{db_name}"
    )

    cursor = mydb.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    number1 = int(index1)
    number2 = int(index2)

    return (f'{data[number2][number1]}')

#Encrpyt data contents
def encrypt_key(contents):
    query = requests.get(f"https://api.apithis.net/encrypt.php?type=md5&content={contents}")
    return query.text

#Ip Lookup
def geo_location(ip):
    query = requests.get(f"https://api.apithis.net/geoip.php?ip={ip}")
    return query.text

#Port Scan
def portscan(ip):
    query = requests.get(f"https://api.hackertarget.com/nmap/?q={ip}")
    return query.text

#Dns Lookup
def dns_lookup(ip):
    query = requests.get(f"https://api.hackertarget.com/dnslookup/?q={ip}")

#Reverse Hostname
def reverse_hostname(hostname):
    query = requests.get(f"https://api.apithis.net/host2ip.php?hostname={hostname}")
    return query.text

#Phone Lookup
def phone_lookup(phn):
    query = requests.get(f"https://api.apithis.net/numberinfo.php?number={phn}")
    return True

#Webhook delete
def webhook_delete(webhook_url):
    query = requests.delete(webhook_url) 
    return True

#Get Current Time
def current_time():
    date_time = datetime.datatime.now()
    return date_time
