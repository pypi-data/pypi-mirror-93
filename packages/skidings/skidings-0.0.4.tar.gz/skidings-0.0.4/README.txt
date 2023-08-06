[Skidings-lib Docs]

About this lib:
---------------
this library was primarly made for people that are getting into networking and sql databases, also requests library ect. this is just a shortcut for learning these librarys and makes you're code more simple and easier to use, this is a open source project so this means you are able to upload community versions of this applications and add and improve the current source code.

Module Functions
-----------------
- get_hwid() // Getting a clients Hwid
- get_ip() // Getting a clients Ip
- check_user(pastebin_url,username_input) // pastebin_url is where the usernames are kept (PASTEBIN URL RAW), and username is a users input.
- check_password(pastebin_url,password_input) // pastebin_url is where the password are kept (PASTEBIN URL RAW), and password is a password input.
- check_ip(pastebin_url) // This function will get the clients current ip and check for it in the pastebin url.
- send_request(url) // This Function will allow you to send requests to sites/apis.
- get_sql_data(host_name,user_name,pass_word,db_name,query) // This function will allow you to send a sql query to you're db.
- fetch_sql_data(host_name,user_name,pass_word,db_name,query,index1,index2) // This function will allow you to send a sql query with indexis to you're db.
- encrypt_key(contents) // This function will allow you to encrypt any text/data you enter.
- geo_location(ip) // This function will ip lookup any ip entered.
- reverse_hostname(hostname) // This function will reverse lookup any hostname you enter.
- phone_lookup(phone_number) //This function will lookup any international number (without the +).
- webhook_delete(webhook_url) // This function will alow you to delete discord urls.