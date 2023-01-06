import warnings
warnings.filterwarnings("ignore")
import time
import requests

# Parameters
protocol="https://"
prefix_host = "api-"
region = "ap-west"
host=prefix_host+"sourabh"+("-"+region if len(region)!=0 else "") +".eng.macrometa.io"
userEmail = "mm@macrometa.io"
userPass = "Macrometa123!@#"
jwt = ""
headers = {}

# Operations
DELETE_ONLY_GLOBAL_URLS = True
DELETE_ALL_TENANTS = True

# -- DO NOT EDIT BELOW THIS LINE -- #

# URLs
login_url = protocol+host+"/_open/auth"
tenants_url = protocol+host+"/_api/tenants"
tenant_url = protocol+host+"/_api/tenant"
cursor_url = protocol+host+"/_fabric/_system/_api/cursor"
doc_url = protocol+host+"/_fabric/_system/_api/document"

# Start Here
print("Host: {}\n".format(host))

if jwt == "":
    res = requests.post(login_url, json={'email': userEmail, 'password': userPass})
    jwt = res.json()['jwt']

headers["authorization"] = "bearer " + jwt

if DELETE_ALL_TENANTS:
    res = requests.get(tenants_url, headers=headers)
    tenants = res.json()["result"]

    for i, tenant in enumerate(tenants):
        tenant_name = tenant["tenant"]
        if tenant_name != "_mm" and tenant_name != "demo":
            res = requests.delete(tenant_url + "/" + tenant_name, headers=headers)
            if res.status_code/100 != 2:
                print(res.json())
            print("DELETE_ALL_TENANTS {}/{} ({})".format(i+1, len(tenants), tenant_name))
        else:
            print("DELETE_ALL_TENANTS {}/{} ({}) [SKIPPED]".format(i+1, len(tenants), tenant_name))

    print("DELETE_ALL_TENANTS - Completed\n")

if DELETE_ONLY_GLOBAL_URLS:
    res = requests.post(cursor_url, json={"batchSize": 10000, "query": "for x in _dnsRecords return x", "ttl": 30}, headers=headers)
    records = res.json()["result"]

    dns_events = []
    for i, record in enumerate(records):
        dns_events.append({
            'createAt': 0,
            'fabric' : record["fabric"],
            'origin_region': region,
            'regions': [],
            'state': 'pending',
            'tenant_id': record["tenant_id"],
            'type': 'delete',
            'updatedAt': 0
        })
    
    res = requests.post(doc_url+"/_dnsEvents", json=dns_events, headers=headers)
    print("DELETE_ONLY_GLOBAL_URLS {} records are being deleted".format(len(records)))

    pending_records = 1
    inprogress_records = 1
    while True:
        pending_records = 0
        inprogress_records = 0
        res = requests.post(cursor_url, json={"query": "for x in _dnsEvents filter x.state != \"done\" return x", "ttl": 30}, headers=headers)
        records = res.json()["result"]

        for i, record in enumerate(records):
            if record["state"] == "pending":
                pending_records+=1
            if record["state"] == "inprogress":
                inprogress_records+=1
        print("DELETE_ONLY_GLOBAL_URLS Pending Records: {} InProgress Records: {}".format(pending_records, inprogress_records))
        if pending_records == 0 or inprogress_records == 0:
            break
        if len(records) == 0:
            print("DELETE_ONLY_GLOBAL_URLS - Check if C8DNS is Running as there exist non-completed events\n")
        time.sleep(5)
    print("DELETE_ONLY_GLOBAL_URLS - Completed\n")
    



