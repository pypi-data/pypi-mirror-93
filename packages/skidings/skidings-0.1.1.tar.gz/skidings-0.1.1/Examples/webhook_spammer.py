from skidings import *

url = ("URL")
message = "TEXT"
delay = DELAY

while True:
    spam = webhook_spammer(url,message,delay)
    print(spam)