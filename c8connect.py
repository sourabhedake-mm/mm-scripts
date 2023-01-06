from c8 import C8Client
'''
This script connects to c8 using various methods
'''
# Connnection Constants
PROTOCOL = "https"
HOST = "sourabh-ap-west.eng.macrometa.io"
PORT = 443

# Auth Constants
EMAIL = "mm@macrometa.io"
PASSWORD = "Macrometa123!@#"
FABRIC = "_system"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjEuNjE4NTU3NjgwNDM0MTgyZSs2LCJleHAiOjE2MTg2MDA4ODAsImlzcyI6Im1hY3JvbWV0YSIsInByZWZlcnJlZF91c2VybmFtZSI6InJvb3QiLCJzdWIiOiJfbW0iLCJ0ZW5hbnQiOiJfbW0ifQ==.rPE0gweaWpFyttX1dfo6Ydjvrok5anvSPnCgZvWchFI="
API_KEY = "apiFullAccess.cDegDsVCoxdUTVCwOhDZqBF7TekGZyhmNoYhlemcKtlpmPLW1r0xhbF9YTSxAo8r84ad5e"

def connectSimple():
    print("Connecting to C8 using email/password...")
    client = C8Client(protocol=PROTOCOL,
                    host=HOST,
                    port=PORT,
                    email=EMAIL,
                    password=PASSWORD,
                    geofabric=FABRIC)

    print(">>> Connected to C8\n")
    return client

# Try with Token
def connectToken():
    print("Connecting to C8 using JWT token...")
    client = C8Client(protocol=PROTOCOL,
                    host=HOST,
                    port=PORT,
                    token=TOKEN)
    print(">>> Connected to C8\n")
    return client

# Try with API KEY
def connectAPIKey():
    print("Connecting to C8 using apiKey...")
    client = C8Client(protocol=PROTOCOL,
                    host=HOST,
                    port=PORT,
                    apikey=API_KEY)
    print(">>> Connected to C8\n")

    return client

if __name__ == "__main__":
    connectSimple()
    connectToken()
    connectAPIKey()
