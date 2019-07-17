import os

from flask import Flask

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'plprofiler.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello World!'

    # start the db
    from . import db
    db.init_app(app)

    # register the blueprint
    from . import direct_profile
    app.register_blueprint(direct_profile.bp)

    # register the blueprint
    from . import define_connections
    app.register_blueprint(define_connections.bp)

    # register the blueprint
    from . import monitor
    app.register_blueprint(monitor.bp)

    from . import home
    app.register_blueprint(home.bp)
    # makes the home index the main index (i.e. no url prefix)
    app.add_url_rule('/', endpoint='home')

    return app
