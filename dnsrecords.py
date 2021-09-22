import subprocess
import json
import time

getPodsCmd = "kubectl --kubeconfig ~/kubeconfig get pods -n c8 | grep c8gui | cut -f1 -d\" \""
execCmd = "kubectl --kubeconfig ~/kubeconfig -n c8 exec -it $1 -- $2"
getDnsAPI = "curl http://c8dns.c8:8000/_api/dns/urls"
deleteDnsAPI = "curl -XDELETE http://c8dns.c8:8000/_api/dns/urls/$1"

print ("Getting GUI pod name to perform curl operations")
p = subprocess.Popen(getPodsCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
output = p.stdout.readlines()
if len(output) == 0:
    print ("No DNS pod found.")
    exit(1)

guiPodName = output[0].decode('utf-8').strip()

print ("Getting DNS records from c8dns service")

retry=3
dnsRecFound = False
while retry>0:
    print (execCmd.replace("$1", guiPodName).replace("$2", getDnsAPI))
    p = subprocess.Popen(execCmd.replace("$1", guiPodName).replace("$2", getDnsAPI), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdoutdata, stderrdata = p.communicate()

    if len(stdoutdata) == 0:
        print ("No DNS records found.")
        exit(1)

    dnsEntries = stdoutdata.decode('utf-8').strip()
    if (len(dnsEntries) != 0 and dnsEntries[-1] == "}"):
        dnsRecFound = True
        break
    retry -= 1

if dnsRecFound == False:
    print ("Failed to get DNS records. Please retry.")
    exit(1)

entJson = eval(dnsEntries)
entryCount = len(entJson)
print ("Found", entryCount, "DNS records...")
for idx, url in enumerate(entJson):
    print ("{}/{} - Deleting {}".format(idx+1, entryCount, url))
    p = subprocess.Popen(execCmd.replace("$1", guiPodName).replace("$2", deleteDnsAPI.replace("$1", url)), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdoutdata, stderrdata = p.communicate()
    print (stdoutdata)        
    time.sleep(0.1)
    