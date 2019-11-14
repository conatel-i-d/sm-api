from .model import Result

BASE_ROUTE = "results"

def register_routes(api, app, root="api"):
    from .controller import api as results_api

    api.add_namespace(results_api, path=f"/{root}/{BASE_ROUTE}")