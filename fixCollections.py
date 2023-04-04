import requests
import json
import time

base_url = 'https://api-sde-sin.eng.macrometa.io'
email = 'MM TENANT'
password = 'PASSWORD'
auth = (email, password)

# Perform login and get the JWT
response = requests.post(f'{base_url}/_open/auth', json={'email': email, 'password': password})
jwt = json.loads(response.text)['jwt']
auth_headers = {'Authorization': f'Bearer {jwt}'}

HORROR_NO = 18446744073709552
recalculate_collections = {}

def get_collections():
    data = {
        "query": "FOR fabric IN _guestdbs \n SORT fabric.name \n RETURN fabric.name",
        "batchSize": 100
    }

    response = requests.post(f'{base_url}/_api/cursor', headers=auth_headers, json = data)
    fabrics = json.loads(response.text)["result"]


    for j, fabric in enumerate(fabrics):
        response = requests.get(f'{base_url}/_fabric/{fabric}/_api/collection', headers=auth_headers)
        collections = json.loads(response.text)["result"]

        for i,coll in enumerate(collections):
            recalculate = False
            coll_name = coll["name"]
            print_string = f'** Fabric: {j+1}/{len(fabrics)} [{round(i*100/len(collections), 2)}%] Checking {coll_name} from the fabric {fabric}...'
            blank_string = " " * len(print_string)
            print (print_string, end='\r')
            response = requests.get(f'{base_url}/_fabric/{fabric}/_api/collection/{coll_name}/count', headers=auth_headers)
            if response.status_code//100 != 2:
                recalculate = True
            else:
                count = json.loads(response.text)["count"]
                if count > HORROR_NO:
                    recalculate = True
            print (blank_string, end='\r')

            if recalculate:
                print(f'Fabric: {fabric}, Collection: {coll_name}, Count: {count}  << Recalculate the count')
                if fabric in recalculate_collections:
                    recalculate_collections[fabric].append(coll_name)
                else:
                    recalculate_collections[fabric] = [coll_name]
            else:
                print(f'Fabric: {fabric}, Collection: {coll_name}, Count: {count}')

def recalculate_coll():
    if (len(recalculate_collections) == 0):
        print("All the collections look fine. Enjoy your day!")
        exit()


    print("\n")
    print("Need to calculate the count for the following collections.")
    print(recalculate_collections)
    print("\nPress Enter to start recalculating the count...")
    input()

    for fabric in recalculate_collections:
        for collection in recalculate_collections[fabric]:
            stable = False
            prev_count = -1
            i = 1
            while (stable == False):
                print_string = f"** Fabric: {fabric} Recalculating count for {collection}"
                blank_string = " " * len(print_string)
                print(print_string, end = '\r')

                response = requests.put(f'{base_url}/_db/{fabric}/_api/collection/{collection}/recalculateCount', headers=auth_headers)
                count = json.loads(response.text)["count"]
                print (blank_string, end = '\r')

                if prev_count != -1 and prev_count == count:
                    stable = True
                
                prev_count = count
                
                print(f"Fabric: {fabric} - {collection} - Attempt {i} - Current count of documents: {count}")
                i+=1

get_collections()
recalculate_coll()

print("Done")