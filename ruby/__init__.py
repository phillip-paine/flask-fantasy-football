import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app: instance_relative_config means that config files will be
    # stored outside of the ruby (flask) folder. E.g. db secrets etc that will not be committed to git
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'placeholdername.sqlite')
    )
    # we can override the config from_mapping command with either the test_config or the config.py file
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    # create the instance folder
    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass

    # create a request for hte server to display in html:
    @app.route('/hello')
    def hello():
        return 'Hello'

    from . import db  # I think this has to be inside the app function so app instance has access to funcs
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)  # register the blueprint with the app to handle requests

    return app
