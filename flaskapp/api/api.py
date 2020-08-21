'''API'''
from flask import Blueprint
from flaskapp import ma
from flaskapp.models import Post

apibp = Blueprint('api', __name__)

class PostSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'date_posted', 'content', 'user_id')

post_schema = PostSchema()
posts_schema = PostSchema(many=True)

# Get Single Post
@apibp.route('/post/<id>', methods=['GET'])
def get_post(id):
    '''Get Single Post'''
    post = Post.query.get(id)
    return post_schema.jsonify(post)
