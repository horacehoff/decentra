import socket, os
ENC_KEY = "$52A5E5ABC427Fp9430BC5D435F9om0CE3BEC257C2E9DF122DD9178D29E7DAC8EB6E3E5ABC4907F9430BC5D435F2E9DF12FB1DZeN_RCE3BEC257C2@2&8zk$NkqKzh-Vr2$AGTJf!L&p3=Zx?vmg45272C0F58BB404766A81F1__Z$sKfj6vT-Fs49RAxU6%5NxkPB=rT%QK%d&+*UkPjp&=7ebZptW$xYp*Mg-GLVe$-JsBJ*f5A5rvKJvtEx*T@hTer^tWd4GAcxP!NLNhBTx-?NvqS4@tt_uMa!=?Uxz7hSAZ&7RZ4CUEHt3k4Qggt9M!9Fn#CU6AVNZ+rv93VunG4!E7hHtQ=*DMDmLSD9D3C32C003C342F0DD401FF926508605DB68B9D975A49EB4A8FB92ED0F0CC4Bf8pr@NZe$59jE6735686C6A05C7F83556114355912ECB1D033843DD50FB15D2F788E93EFEBC593A0A37C84803C5C04A7070097DE8AEACAE213DBF223B52B772690ED1ADBE9F6GQw6PdjYxH%FvLWKLa$n&zVJ5_AFhMxtWL7sD+Dx4W7qa7Hk47Q&B975956D9199B98CD48D4CD37293C64A7617E8738064DFFFA402762C36D0569DA032F833D4EB399C55671940D49AB94BDED593C5BD585"

class log():
    def info(data):
        print("INFO: "+data)
    def warning(data):
        print("WARNING: "+data)
    def critical(data):
        print("CRITICAL: "+data)
        

def encrypt(data, key):
    """
    Given a string and a key, return a string where each character in the original string is replaced by
    a character 
    in the shuffled list with the same index

    :param data: The data to be encrypted
    :param key: The seed for the random number generator
    :return: The encrypted message.
    """
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


def decrypt(data, key):
    """
    Given a string and a key, the function will return the decrypted string
    
    :param data: The data to be decrypted
    :param key: The seed for the random number generator
    :return: The result is the decrypted message.
    """
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
    """
    Decrypts the data using the key and returns the decrypted data
    
    :param data: The data to be decrypted
    :return: The encrypted data.
    """
    return decrypt(decrypt(data.decode('utf-8'), "That's one small step for man, one giant leap for mankind"), ENC_KEY)


def encrypt_data(data):
    """
    Encrypt the data using the encrypt function, then encrypt the result using the ENC_KEY
    
    :param data: The data to be encrypted
    :return: The encrypted data.
    """
    return bytes(encrypt(encrypt(data.encode('utf-8'), "That's one small step for man, one giant leap for mankind"), ENC_KEY))


def request_database():
    """
    Connect to the database and request the database
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        data = s.recv(4096)
        data = decrypt_data(data)
        log.info('Received database from '+HOST+"(PORT "+str(PORT)+") -> "+data.replace("!","[STRING TABLE SEPARATOR]"))
        parse_db(data)
        

def modify_database(data_row, modified_data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        modified_data = "MODIFYDB"+modified_data.replace(",","!")
        data = s.sendall(encrypt_data(modified_data))
        data = decrypt_data(data)
        log.info('Sent modified database to '+HOST+"(PORT "+str(PORT)+") -> "+data.replace("!","[STRING TABLE SEPARATOR]"))
        parse_db(data)
    

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 1969        # The port used by the server


request_database()
# os.system('cls' if os.name == 'nt' else 'clear')
# while True:
#     choice = input("""
#      +--------+
#      |Decentra|
# +----+--------+----+
# | 1. Request DB    |
# | 2. Modify DB     |
# +------------------+
#    Choice:
# """)
#     if choice == '1':
#         os.system('cls' if os.name == 'nt' else 'clear')
#         request_database()
#     elif choice == "2":
#         os.system('cls' if os.name == 'nt' else 'clear')
#         modify_database(input("Data row to modify: "), input("New value (separated by commas): "))
#     else:
#         os.system('cls' if os.name == 'nt' else 'clear')
#         pass
