from json.decoder import JSONDecodeError
from c8 import C8Client, C8AuthenticationError, cursor
from c8.exceptions import DocumentInsertError
import argparse
import json
import datetime;

# Constants
PROTOCOL = "https"
PORT = 443
FABRIC = "_system"

# Class responsible to perform collection operations
class C8Collection:
    def __init__(self, client):
        self.client = client
        
    def validate(self, collectionName, allowColCreate):
        print ("Validating the collection parameters...")
        if not collectionName:
            print(">>> Specify the collection name to be used for further operations: --collection")
            return False
        
        try:
            self.client.get_collection(name=collectionName)
        except Exception as ex:
            print(">>> Collection " + collectionName + " not found.")
            if not allowColCreate:
                print(">>> If you want the collection to be created, specify --allow-col-create")
                return False 
            self.client.create_collection(name=collectionName)
            print(">>> Created the collection - " + collectionName)

        self.collection = collectionName
        print(">>> Collection validation is successful.\n")
        return True
    
    def performOperation(self, args):
        if not args.insert_doc and not args.query_doc:
            print("No collection operation provided.")
            print("Insert operations available: --insert-doc")
            print("Query operations available: --query-doc")
            print("Remove operations available: --remove-doc")
            return False

        if args.insert_doc:
            print("Performing the insert operation...")
            try:
                jsonDoc = json.loads(args.insert_doc)
                ct = datetime.datetime.now()
                jsonDoc["_created_at"] = ct.isoformat()
                self.client.insert_document(collection_name=self.collection, document=jsonDoc)

                print(">>> Inserted the document successfully.\n")
            except DocumentInsertError as ex:
                print("ERR: " + ex.message)
            except JSONDecodeError as ex:
                print("ERR: Input document has incorrect JSON format. " + ex.msg)

        if args.query_doc:
            print("Performing the query operation...")
            try:
                field,value = args.query_doc.split("=")
                query = 'FOR doc IN ' + self.collection + ' FILTER doc.' + '`' + field + '` == "' + value + '" RETURN doc'
                cursor = self.client.execute_query(query)
                docs = [document for document in cursor]
                print(docs)
                print(">>> Query completed.\n")
            except ValueError as ex:
                print(">>> ERR: Incorrect format for query specified. Specify field to search and value in FIELD=VALUE format.")

        if args.remove_doc:
            print("Performing the remove operation...")
            try:
                field,value = args.remove_doc.split("=")
                query = 'FOR doc IN ' + self.collection + ' FILTER doc.' + '`' + field + '` == "' + value + '" REMOVE doc._key IN ' + self.collection
                self.client.execute_query(query)
                print(">>> Remove operation completed.\n")
            except ValueError as ex:
                print(">>> ERR: Incorrect format for remove specified. Specify field to search and value in FIELD=VALUE format.")

class Login:
    def connectEmail(self, host, email, password, fabric):
        print("Connecting to C8 using email...")
        try:
            client = C8Client(protocol=PROTOCOL,
                        host=host,
                        port=PORT,
                        email=email,
                        password=password,
                        geofabric=fabric)
        except C8AuthenticationError as err:
            print("ERR: " + err.message)
            self.client = None
            return

        print(">>> Connected to C8\n")
        self.client = client

    # Login with the API KEY
    def connectAPIKey(self, host, apiKey):
        print("Connecting to C8 using API key...")
        try:
            client = C8Client(protocol=PROTOCOL,
                        host=host,
                        port=PORT,
                        apikey=apiKey)
        except C8AuthenticationError as err:
            print("ERR: " + err.message)
            self.client = None
            return

        print(">>> Connected to C8\n")
        self.client = client
    
    def auth(self, args):
        if args.email:
            self.connectEmail(args.host, args.email, args.password, args.fabric)
        elif args.apiKey:
            self.connectEmail(args.host, args.email, args.password, args.fabric)
        return self.client is not None

class ArgParser:
    def parseArguments(self):
        parser = argparse.ArgumentParser(description='pyC8 - Collection Editor')
        parser.add_argument('--host', help='Hostname of the cluster')
        parser.add_argument('--email', help='Email ID')
        parser.add_argument('--password', help='Password. Required if `email` is specified')
        parser.add_argument('--apikey', help='API Key to authenticate the client')
        parser.add_argument('--fabric', help='GeoFabric to use. Default: _fabric', default=FABRIC)
        parser.add_argument('--collection', help='Name of the collection to be used')
        parser.add_argument('--allow-col-create', dest='allowColCreate', help='Allow creation of collection if it do not exist', action='store_true')
        parser.add_argument('--insert-doc', help='Insert the JSON document in the collection')
        parser.add_argument('--query-doc', help='Query the document using the field and value', metavar="FIELD=VALUE")
        parser.add_argument('--remove-doc', help='Remove the document using the field and value', metavar="FIELD=VALUE")

        parser._optionals.title = "Arguments"
        self.args = parser.parse_args()

    def validate(self):
        if not self.args.host:
            print("Hostname not specified: --host")
            return False

        if not self.args.email and not self.args.apikey:
            print("None of the auth methods provided: --email, --apiKey")
            return False
        
        if self.args.email and not self.args.password:
            print("Specify password for the email - " + self.args.email)
            return False

        return True

# Parse the input arguments
parser = ArgParser()
parser.parseArguments()

# Validate the arguments
validated = parser.validate()
if not validated:
    print(">>> Exiting the program")
    exit(-1)

# Connect to C8
c8client = Login()
authenticated = c8client.auth(parser.args)
if not authenticated:
    print(">>> Exiting the program")
    exit(-1)

# Perform collection validate
collection = C8Collection(c8client.client)
collValidated = collection.validate(parser.args.collection, parser.args.allowColCreate)
if not collValidated:
    print(">>> Exiting the program")
    exit(-1)

# Execute the operation
collection.performOperation(parser.args)
print(">>> Exiting the program")

