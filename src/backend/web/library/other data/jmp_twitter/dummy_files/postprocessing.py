from pymongo import MongoClient
import urllib

if __name__ == '__main__':

    try:
        # connect to database
        mongo_uri = "mongodb://iotlabRoot:" + urllib.parse.quote("wsnlab123@") + "@192.168.99.11"
        connection = MongoClient(mongo_uri, 27017)
        #connect to database "threats"
        db = connection.admin
        # connect to database "threats"
        print("Database connection successful..")
        print()
        print('searching dbs:')
        # find the db
        allergydb = connection.allergy

        # find the right collection
        allergyGlobal = allergydb.allergyGlobal

        print("retrieved dbs successful..")
        print()
        print('findOne:')
        print()
        x = allergyGlobal.find_one()
        print(x)

    except Exception as e:
        print('error on connection:', e)
