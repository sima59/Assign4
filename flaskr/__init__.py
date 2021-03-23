import os
import barky

from flask import Flask

def create_app(test_config=None):
    """
    From the "Patterns for Flask" section in the documentation, this is a factory pattern for Flask:
    https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "bookmarks.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/barky")
    def barky():
        return barky

    # @app.route("/index")
    # def index():
    #     return "where it all begins"

    # register the database commands
    from . import db

    db.init_app(app)

    # apply the blueprints to the app
    from . import auth, blog

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    

    return app