from views import post_list, post_detail


def setup_routes(app):
    app.router.add_get('/', post_list)
    app.router.add_get('/post/{id}', post_detail)
