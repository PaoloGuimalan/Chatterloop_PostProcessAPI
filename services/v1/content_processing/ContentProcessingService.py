import spacy
from connections.mongo import MongoConnection
from schemas.UserPostSchema import UserPosts
from models.UserPostsModel import PostSchema

class ContentProcessingService:

    def __init__(self):
        self.nlp = None

    def load_model(self):
        if self.nlp == None:
            self.nlp = spacy.load("xx_ent_wiki_sm")

    async def content_check(self, referenceID: str, referenceType: str):
        if referenceType == "post":
            db_posts = MongoConnection.execute("posts")
            post_data: PostSchema = UserPosts(db_posts.find_one({ "postID": referenceID }))
            
            if post_data != {}:
                main_content = post_data["content"]["data"]
                references = [{ "referenceID": reference["referenceID"], "caption": reference["caption"] } for reference in post_data["content"]["references"]]

                doc_main_content = self.nlp(main_content)
                print(doc_main_content, references)

        if referenceType == "message":
            db_messages = MongoConnection.execute("messages")

        print(referenceID, referenceType)