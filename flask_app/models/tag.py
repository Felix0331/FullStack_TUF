from flask_app.config.mysqlconnection import connectToMySQL

class Tag:
    def __init__(self, data):
        self.tag_id = data['tag_id']
        self.tag_name = data['tag_name']

    @classmethod
    def get_tags(cls):
        query = "SELECT * FROM tags;"
        return connectToMySQL('tuf_db').query_db(query)

    @classmethod
    def get_post_tags(cls,data):
        query = "SELECT tags.tag_name, tags.tag_id FROM tags, tag_map WHERE tags.tag_id = (SELECT tag_map.tags_id WHERE tag_map.posts_id = %(post_id)s);"
        return connectToMySQL('tuf_db').query_db(query,data)

    @classmethod
    def get_post_by_tag(cls,data):
        query = "SELECT * FROM posts,tag_map WHERE posts.post_id = (SELECT tag_map.posts_id WHERE tag_map.tags_id = %(tag_id)s);"
        return connectToMySQL('tuf_db').query_db(query,data)
        
# Tag_Map is the join table between posts and tag tables.
class Tag_Map:
    def __init__(self, data):
        self.tag_map_id = data['tag_map_id']
        self.posts_id = data['posts_id']
        self.tags_id = data['tags_id']

    @classmethod
    def delete_post_tags(cls,data):
        query = "DELETE  FROM tag_map WHERE tag_map.posts_id = %(post_id)s"
        return connectToMySQL('tuf_db').query_db(query,data) 

    @classmethod
    def add_tags_to_post(cls,data):
        for tag in data['tag_list']:
            query = f"INSERT INTO tag_map (posts_id, tags_id) VALUES (%(posts_id)s,{tag});"
            connectToMySQL('tuf_db').query_db(query,data)    