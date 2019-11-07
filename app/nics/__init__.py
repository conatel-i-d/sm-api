BASE_ROUTE = "nics"

def register_routes(api, app, root="api"):
    from .controller import api as nics_api

    api.add_namespace(nics_api, path=f"/{root}/{BASE_ROUTE}")