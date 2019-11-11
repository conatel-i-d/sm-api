def register_routes(api, app, root="api"):
  # Importamos el metodo `register_routes` de cada `switch` y lo renombramos
  from app.switch import register_routes as attach_switch
  from app.nics import register_routes as attach_nics
  from app.results import register_routes as attach_results
  # Registramos las rutas
  attach_switch(api, app)
  attach_nics(api, app)
  attach_results(api, app)
