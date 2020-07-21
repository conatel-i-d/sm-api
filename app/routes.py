def register_routes(api, app, root="api"):
  from app.switch import register_routes as attach_switch
  from app.nics import register_routes as attach_nics
  from app.macs import register_routes as attach_macs
  from app.jobs import register_routes as attach_jobs
  from app.logs import register_routes as attach_logs
  attach_switch(api, app)
  attach_nics(api, app)
  attach_macs(api, app)
  attach_jobs(api, app)
  attach_logs(api, app)
