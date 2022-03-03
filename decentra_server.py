import socket
from datetime import datetime

ENC_KEY = "94606366EF55EDEDB66E431153BD2E48BB5015A7F15371B2DF78D37C32B5E2886D4292F1D825BE32011BF7AA62FC2A2ACB8B765ABF6AB26099BAAF12943279FD"
nodes = []

with open("decentra_server.log","w+") as f:
    f.write("Decentra Server Log")

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
    with open("decentra_server.log","a") as f:
        now = datetime.now()
        current_time = now.strftime("%Y/%m/%d/%H:%M:%S")
        f.write("\n("+current_time+")  -  "+data)
        print("\n("+current_time+")  -  "+data)

class log():
    def info(data):
        add_to_log("INFO: "+data)
    def warning(data):
        add_to_log("WARNING: "+data)
    def critical(data):
        add_to_log("CRITICAL: "+data)
        


HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 10969        # Port to listen on (non-privileged ports are > 1023)
articles = ["heyya","ayo"]
articles_descriptions = ["ayo bitch"]
articles_titles = ["noice"]

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
            if "request_db" in decrypt(decrypt(s.recv(4096).decode('utf-8'), "That's one small step for man, one giant leap for mankind"), ENC_KEY):
                    import random
                    try:
                        selected_node = random.choice(nodes)
                        conn.sendall(encrypt(selected_node, ENC_KEY))
                        log.info("Sent node adress("+selected_node+") to requesting node -> "+str(addr))
                    except:
                        log.warning("Failed to send node adress("+selected_node+") to requesting node -> "+str(addr))
            else:
                log.info("New node -> "+str(addr))
                nodes.append(addr)
                print(nodes)
                try:
                    conn.sendall(send_db())
                    log.info("Sent database to node -> "+str(addr))
                    conn.close()
                except Exception as e:
                    print(e)
                    log.warning("Failed to send database to node -> "+str(addr))
                    pass