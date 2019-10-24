from .model import Switch

BASE_ROUTE = "switch"

def register_routes(api, app, root="api"):
    from .controller import api as switch_api

    api.add_namespace(switch_api, path=f"/{root}/{BASE_ROUTE}")