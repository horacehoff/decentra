import os
i = 0
max_i = int(input("Number of tries: "))
while i < max_i:
    try:
        os.system("python decentra_client.py")
    except:
        pass
    i = i+1
    