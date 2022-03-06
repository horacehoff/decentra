import socket, os
ENC_KEY = "94606366EF55EDEDB66E431153BD2E48BB5015A7F15371B2DF78D37C32B5E2886D4292F1D825BE32011BF7AA62FC2A2ACB8B765ABF6AB26099BAAF12943279FD"

class log():
    def info(data):
        print("INFO: "+data)
    def warning(data):
        print("WARNING: "+data)
    def critical(data):
        print("CRITICAL: "+data)
        
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

def parse_db(data):
    all_lists = data.replace("'","").split("!")
    data = ""
    for list in all_lists:
        if not data == all_lists[0]:
            data = data+"\n"+str(list.strip('][').split(', '))
        else:
            data = str(list.strip('][').split(', '))
    with open("db_decentra.txt","w+") as f:
        f.write(data.removeprefix("\n"))


def decrypt_data(data):
    return decrypt(decrypt(data.decode('utf-8'), "That's one small step for man, one giant leap for mankind"), ENC_KEY)

def encrypt_data(data):
    return bytes(encrypt(encrypt(data.encode('utf-8'), "That's one small step for man, one giant leap for mankind"), ENC_KEY))

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 1969        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    while True:
        s.connect((HOST, PORT))
        data = s.recv(4096)
        data = decrypt_data(data)
        log.info('Received database from '+HOST+"(PORT "+str(PORT)+") -> "+data.replace("!","[STRING TABLE SEPARATOR]"))
        parse_db(data)
