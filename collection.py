from c8 import C8Client
import c8connect
'''
This script creates collection on GDN
'''

# Connnection Constants
COL_NAME = "key_val_col"

def create(client, type, name, clean = False):

    print("Creating the collection - ", COL_NAME)

    if type == "kv":

        # Create a new collection if it does not exist
        if client.has_collection(name):
            print(">>> Collection already exists")
            if clean:
                print(">>> Provided cleanup option...")
            else:
                return

        client.create_collection_kv(name=name)
        print(">>> Collection created - ", name)

    else:
        print(">>> Invalid collection type - ", type)

def delete (client, collection):
    client.delete_collection_kv(collection)
    print (">>> Deleted the collection")

if __name__ == "__main__":
    client = c8connect.connectAPIKey()
    create(client, "kv", COL_NAME)
    delete(client, COL_NAME)
