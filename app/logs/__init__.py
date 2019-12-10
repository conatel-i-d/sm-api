from .model import Log

BASE_ROUTE = "logs"

def register_routes(api, app, root="api"):
    from .controller import api as logs_api

    api.add_namespace(logs_api, path=f"/{root}/{BASE_ROUTE}")