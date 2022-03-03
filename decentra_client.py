import socket, os
ENC_KEY = "94606366EF55EDEDB66E431153BD2E48BB5015A7F15371B2DF78D37C32B5E2886D4292F1D825BE32011BF7AA62FC2A2ACB8B765ABF6AB26099BAAF12943279FD"
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
    articles = all_lists[0].strip('][').split(', ')
    articles_descriptions = all_lists[1].strip('][').split(', ')
    articles_titles = all_lists[2].strip('][').split(', ')
    print(articles, articles_descriptions, articles_titles)
    with open("db_decentra.txt","w+") as f:
        f.write(str(articles)+"\n"+str(articles_descriptions)+"\n"+str(articles_titles)+"\n")


def decrypt_data(data):
    return decrypt(decrypt(data.decode('utf-8'), "get fucked"), ENC_KEY)

def encrypt_data(data):
    return bytes(encrypt(encrypt(data.encode('utf-8'), "get fucked"), ENC_KEY))

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 10969        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    while True:
        if os.path.isfile("./db_decentra.txt"):
            s.connect((HOST, PORT))
            data = s.recv(4096)
            data = decrypt_data(data)
            print('Received', data)
            parse_db(data)
        else:
            s.connect((HOST, PORT))
            s.sendall(encrypt_data("request_db"))
