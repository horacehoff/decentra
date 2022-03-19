import socket
from datetime import datetime
import os

ENC_KEY = "$52A5E5ABC427Fp9430BC5D435F9om0CE3BEC257C2E9DF122DD9178D29E7DAC8EB6E3E5ABC4907F9430BC5D435F2E9DF12FB1DZeN_RCE3BEC257C2@2&8zk$NkqKzh-Vr2$AGTJf!L&p3=Zx?vmg45272C0F58BB404766A81F1__Z$sKfj6vT-Fs49RAxU6%5NxkPB=rT%QK%d&+*UkPjp&=7ebZptW$xYp*Mg-GLVe$-JsBJ*f5A5rvKJvtEx*T@hTer^tWd4GAcxP!NLNhBTx-?NvqS4@tt_uMa!=?Uxz7hSAZ&7RZ4CUEHt3k4Qggt9M!9Fn#CU6AVNZ+rv93VunG4!E7hHtQ=*DMDmLSD9D3C32C003C342F0DD401FF926508605DB68B9D975A49EB4A8FB92ED0F0CC4Bf8pr@NZe$59jE6735686C6A05C7F83556114355912ECB1D033843DD50FB15D2F788E93EFEBC593A0A37C84803C5C04A7070097DE8AEACAE213DBF223B52B772690ED1ADBE9F6GQw6PdjYxH%FvLWKLa$n&zVJ5_AFhMxtWL7sD+Dx4W7qa7Hk47Q&B975956D9199B98CD48D4CD37293C64A7617E8738064DFFFA402762C36D0569DA032F833D4EB399C55671940D49AB94BDED593C5BD585"
nodes = []

os.remove("decentra_server.log")
with open("decentra_server.log","w+") as f:
    f.write("+-------------------+\n|Decentra Server Log|\n+-------------------+\n")
    


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


def add_to_log(data):
    """
    Add a line to the log file
    
    :param data: The data to be logged
    """
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
        

def send_db():
    """
    It takes the articles and their descriptions and titles and combines them into a single string. Then
    it encrypts that string with the encryption key. Then it returns the encrypted string as
    bytes
    :return: The encrypted data.
    """
    all_articles = str(articles)+"!"+str(articles_descriptions)+"!"+str(articles_titles)
    all_articles = encrypt(all_articles, ENC_KEY)
    all_articles = encrypt(all_articles, "That's one small step for man, one giant leap for mankind")
    return bytes(all_articles, 'utf-8')


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


# Creating a socket object and setting the host and port to localhost and 1969 respectively.
HOST = '127.0.0.1'
PORT = 1969
# The database.
articles = ["articcle1","articllle2"]
articles_descriptions = ["first description","seconddddescription"]
articles_titles = ["first title","second title"]



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    while True:
        s.listen()
        conn, addr = s.accept()
        if "MODIFYDB" in "null":
            modified_data = data.split("!")
            modified_articles = modified_data[0]
            print(modified_articles)
        else:
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
        