from pymongo.mongo_client import MongoClient # type: ignore
from configs.env_exports import envs

class MongoConnection:

    def connect():
        uri = f"mongodb+srv://{envs.mongodb_cluster_un}:{envs.mongodb_cluster_pass}@cluster0.6uzwm.mongodb.net/{envs.mongodb_cluster_db}?w=majority"
        client = MongoClient(uri)
        
        try:
            client.admin.command('ping')
            print("Ping success from MongoDB")
        except Exception as e:
            print(e)

    def execute(collection: str):
        uri = f"mongodb+srv://{envs.mongodb_cluster_un}:{envs.mongodb_cluster_pass}@cluster0.6uzwm.mongodb.net/{envs.mongodb_cluster_db}?w=majority"
        client = MongoClient(uri)
        collection_name = client.chatterloop[collection]
        return collection_name;