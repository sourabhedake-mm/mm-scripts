credentials()
{
    EMAIL='mm@macrometa.io'
    PASSWORD='Macrometa123!@#'
}

authenticate()
{
    auth=`curl -L -s -X POST "https://api-${FEDERATION}/_open/auth" -H "accept: application/json" -H "Content-Type: application/json" -d '{"email": "'"$EMAIL"'", "password": "'"$PASSWORD"'"}' | python3 -c 'import sys; import json; print("Authorization: bearer " + json.load(sys.stdin)["jwt"])'`
}

query()
{
    query=`echo "$1" | sed -e 's/"/\\\"/g'`
    curl -s -X POST -H "$auth" "https://api-${FEDERATION}/_fabric/_system/_api/cursor" -d '{ "batchSize": 100, "bindVars": {}, "count": true, "query": "'"$query"'", "ttl": 0}' | python3 -c 'import sys; import json; print(json.dumps(json.load(sys.stdin)["result"]))'
}

c8db_passwd()
{
    pass=`echo "$1" | sed -e 's/"/\\\"/g'`
    curl -X PATCH "https://api-${FEDERATION}/_fabric/_system/_api/user/root" -H "accept: application/json" -H "Content-Type: application/json" -H "$auth" -d '{"active": true, "extra": {}, "passwd": "$pass"}'
}
