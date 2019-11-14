
BASE_ROUTE = "auth"

def register_routes(api, app, root="api"):
    from .controller import api as auth_api

    app.register_blueprint(auth_api)
