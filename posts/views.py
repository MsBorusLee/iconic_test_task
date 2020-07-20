import datetime as dt
import json
from collections import Counter

from aiohttp import web
from dateutil.parser import parse


async def post_list(request):
    with open('post.json') as f:
        posts_data = json.load(f)

    posts = posts_data['posts']
    posts = list(filter(lambda x: not x['deleted'], posts))
    posts = list(filter(lambda x: parse(x['date'], ignoretz=True) <= dt.datetime.now(),
                        posts))
    posts = sorted(posts, key=lambda x: x['date'])

    with open('comments.json') as f:
        comments_data = json.load(f)

    comments = comments_data['comments']
    post_comments = Counter()
    for comment in comments:
        post_comments[comment['post_id']] += 1

    for post in posts:
        post['comments_count'] = post_comments[post['id']]

    return web.json_response({'posts': posts, 'posts_count': len(posts)})


async def post_detail(request):
    post_id = int(request.match_info.get('id'))

    with open('post.json') as f:
        posts_data = json.load(f)

    posts = posts_data['posts']
    posts = list(filter(lambda x: x['id'] == post_id, posts))
    if len(posts) == 0:
        raise web.HTTPNotFound()

    post = posts[0]
    if post['deleted'] or parse(post['date'], ignoretz=True) > dt.datetime.now():
        raise web.HTTPNotFound()

    with open('comments.json') as f:
        comments_data = json.load(f)

    post_comments = list(filter(lambda x: x['post_id'] == post['id'], comments_data['comments']))
    post['comments_count'] = len(post_comments)
    post['comments'] = sorted(post_comments, key=lambda x: x['date'])

    return web.json_response(post)
