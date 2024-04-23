import routes


def register_blueprints(app):
    app.register_blueprint(routes.category)
    app.register_blueprint(routes.event)
    app.register_blueprint(routes.socials)
    app.register_blueprint(routes.users)
    app.register_blueprint(routes.auth)
    app.register_blueprint(routes.contacts)
