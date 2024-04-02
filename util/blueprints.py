import routes


def register_blueprints(app):
    app.register_blueprint(routes.category)
    app.register_blueprint(routes.event)
    app.register_blueprint(routes.reminder)
