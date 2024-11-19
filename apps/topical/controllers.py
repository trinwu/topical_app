from py4web import action, request, URL
from .common import auth
from .models import db, parse_post_content, get_user_email

@action('index')
@action.uses('index.html', db, auth)
def index():
    return dict()

@action('get_posts')
@action.uses(db, auth)
def get_posts():
    posts = db(db.post).select(orderby=~db.post.created_on).as_list()
    for post in posts:
        # Get tags for each post
        tags = db(db.tag.post_id == post['id']).select(db.tag.name)
        post['tags'] = ['#' + tag.name for tag in tags]
    return dict(
        posts=posts,
        user_email=get_user_email()
    )

@action('create_post', method="POST")
@action.uses(db, auth.user)
def create_post():
    content = request.json.get('content')
    if not content:
        return dict(status='error', message='No content provided')
    
    # Create post
    post_id = db.post.insert(content=content)
    
    # Extract and save tags
    tags = parse_post_content(content)
    for tag in tags:
        db.tag.insert(name=tag, post_id=post_id)
    
    return dict(status='success')

@action('delete_post', method="POST")
@action.uses(db, auth.user)
def delete_post():
    post_id = request.json.get('post_id')
    if not post_id:
        return dict(status='error', message='No post ID provided')
    
    # Check if user owns the post
    post = db.post[post_id]
    if post and post.user_email == get_user_email():
        # Delete associated tags first
        db(db.tag.post_id == post_id).delete()
        # Then delete the post
        db(db.post.id == post_id).delete()
        return dict(status='success')
    return dict(status='error', message='Not authorized')

@action('get_tags')
@action.uses(db, auth)
def get_tags():
    # Get unique tags from posts that still exist
    tags = db().select(
        db.tag.name,
        groupby=db.tag.name,
    )
    return dict(tags=[tag.name for tag in tags])
