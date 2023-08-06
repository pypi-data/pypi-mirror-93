from skidings import *

webhook_url = input("Enter webhook url: ")

request = webhook_delete(webhook_url)

print(request)