from skidings import *

host = "DB IP/URL"
username = "DB USERNAME"
password = "DB PASSWORD"
database = "DB NAME"
query = "SQL QUERY"
index1 = int(NUMBER)
index2 = int(NUMBER)

connect = get_sql_data(host,username,password,database,query,index1,index2)

print(connect)

input()