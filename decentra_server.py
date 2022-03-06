import socket
from datetime import datetime
import os

ENC_KEY = "3957396E9C956A6F8E435D43D11112455CCCB7F9F3C146D3CC63F2E4E5644D978035DB2EBB57CD15DAD4AC3E7CC6F286B6DA2DA88C8E97B6D12EA61A3A0B0E94"
nodes = []

os.remove("decentra_server.log")
with open("decentra_server.log","w+") as f:
    f.write("|-------------------|\n|Decentra Server Log|\n|-------------------|\n")

def encrypt(data, key): # encrypt(no explanation either)
    import random
    result = ''
    message = ''
    characters_in_order = [chr(x) for x in range(16, 128)]
    message = data
    r_seed = key
    random.seed(r_seed)
    shuffled_list = [chr(x) for x in range(16, 128)]
    random.shuffle(shuffled_list)
    for i in range(0, len(message)):
        result += shuffled_list[characters_in_order.index(message[i])]
    return result

def decrypt(data, key): #decrypt(no explanation)
    import random
    result = ''
    message = ''
    characters_in_order = [chr(x) for x in range(16, 128)]
    message = data
    r_seed = key
    random.seed(r_seed)
    shuffled_list = [chr(x) for x in range(16, 128)]
    random.shuffle(shuffled_list)
    for i in range(0, len(message)):
        result += characters_in_order[shuffled_list.index(message[i])]
    return result

def add_to_log(data):
    with open("./decentra_server.log","a") as f:
        now = datetime.now()
        current_time = now.strftime("%Y/%m/%d/%H:%M:%S")
        f.write("\n("+current_time+")  -  "+data)
        print("("+current_time+")  -  "+data)

class log():
    def info(data):
        add_to_log("INFO: "+data)
    def warning(data):
        add_to_log("WARNING: "+data)
    def critical(data):
        add_to_log("CRITICAL: "+data)
        


HOST = '127.0.0.1'
PORT = 1969
articles = ["article1","article22"]
articles_descriptions = ["first description","second description"]
articles_titles = ["first title","second title"]

def send_db():
    all_articles = str(articles)+"!"+str(articles_descriptions)+"!"+str(articles_titles)
    all_articles = encrypt(all_articles, ENC_KEY)
    all_articles = encrypt(all_articles, "That's one small step for man, one giant leap for mankind")
    return bytes(all_articles, 'utf-8')

def decrypt_data(data):
    return decrypt(decrypt(data.decode('utf-8'), "That's one small step for man, one giant leap for mankind"), ENC_KEY)

def encrypt_data(data):
    return bytes(encrypt(encrypt(data.encode('utf-8'), "That's one small step for man, one giant leap for mankind"), ENC_KEY))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    while True:
        s.listen()
        conn, addr = s.accept()
        with conn:
            if not any(str(addr[0]) in node for node in nodes):
                log.info("New node -> "+str(addr))
                nodes.append(addr)
            else:
                log.info("Known node with different port -> "+str(addr))
            log.info("Reminder of all existing nodes -> "+str(nodes))
            try:
                conn.sendall(send_db())
                log.info("Sent database to node -> "+str(addr))
                conn.close()
            except Exception as e:
                print(e)
                log.warning("Failed to send database to node -> "+str(addr))
                pass