def register_routes(api, app, root="api"):
  from app.switch import register_routes as attach_switch
  from app.nics import register_routes as attach_nics
  from app.auth import register_routes as attach_auth
  from app.jobs import register_routes as attach_jobs
  attach_switch(api, app)
  attach_nics(api, app)
  attach_jobs(api, app)
  attach_auth(api, app)
