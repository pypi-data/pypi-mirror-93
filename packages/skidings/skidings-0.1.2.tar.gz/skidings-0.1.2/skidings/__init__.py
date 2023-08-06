import datetime
import subprocess
import time
import mysql.connector
import requests
import json
from dhooks import Webhook

# Get current hwid
def get_hwid():
    hwid = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
    return hwid


# Get current ip
def get_ip():
    query = requests.get("https://api.ipify.org").text
    return query


# Hwid check using pastebin
def check_hwid(paste_url):
    current_hwid = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()

    query = requests.get(paste_url).text

    if current_hwid in query:
        return True
    else:
        return False


# Username check using pastebin
def check_user(paste_url, username):
    username_query = requests.get(paste_url).text

    if username in username_query:
        return True
    else:
        return False


# Password check using pastebin
def check_password(paste_url, password):
    password_query = requests.get(paste_url).text

    if password in password_query:
        return True
    else:
        return False


# Ip Check using pastebin
def check_ip(paste_url):
    ip_query = requests.get(paste_url).text

    ip_query2 = requests.get("https://api.ipify.org").text

    if ip_query2 in ip_query:
        return True
    else:
        return False


# Send http Requests
def send_request(url):
    request = requests.get(url).text
    return request


# Getting data without using index's
def get_sql_data(host_name, user_name, pass_word, db_name, query):
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


# Getting data using index's
def fetch_sql_data(host_name, user_name, pass_word, db_name, query, index1, index2):
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

    return f'{data[number2][number1]}'


# Encrpyt data contents
def encrypt_key(contents):
    query = requests.get(f"https://api.apithis.net/encrypt.php?type=md5&content={contents}").text
    return query


# Ip Lookup
def geo_location(ip):
    query = requests.get(f"http://ip-api.com/json/{ip}?fields=66846719").text
    json_loaded = json.loads(query)

    return json_loaded


# Port Scan
def portscan(ip):
    query = requests.get(f"https://api.hackertarget.com/nmap/?q={ip}").text
    return query


# Reverse Hostname
def reverse_hostname(hostname):
    query = requests.get(f"https://api.apithis.net/host2ip.php?hostname={hostname}").text
    return query


# Phone Lookup
def phone_lookup(phn):
    query = requests.get(f"https://api.apithis.net/numberinfo.php?number={phn}").text
    return query


# Webhook delete
def webhook_delete(webhook_url):
    query = requests.delete(webhook_url)
    return "Webhook Deleted."


# Webhook Spammer
def webhook_spammer(webhook_url, message, delay):
    webhookurl = Webhook(webhook_url)

    while True:
        time.sleep(delay)
        webhookurl.send("Made By Aeron: " + message)
        return ("Sent.")


# Get Current Time
def current_time():
    date_time = datetime.datetime.now()
    return date_time