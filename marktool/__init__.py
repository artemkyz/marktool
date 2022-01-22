import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        # DATABASE=os.path.join(app.instance_path, "db.sqlite"),
        SQLALCHEMY_DATABASE_URI='sqlite:///../instance/db.sqlite',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        DEBUG='1',
    )

    # Initialize logging system
    file_log = logging.FileHandler(os.path.join(app.instance_path, 'record.log'))
    console_out = logging.StreamHandler()
    # logging.basicConfig(handlers=(file_log, console_out), level=logging.DEBUG,
    #                     format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
    logging.basicConfig(level=logging.DEBUG,
                        format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


    # logging.basicConfig(filename=os.path.join(app.instance_path, 'record.log'), level=logging.DEBUG,
    #                     format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
        app.logger.info('Load by condition test_config is None')
    else:
        # load the test config if passed in
        app.config.update(test_config)
        app.logger.info('Load by condition test_config is not None')

    # ensure the instance folder exists
    try:
        os.makedirs(os.path.join(app.instance_path, 'xml'))
        app.logger.info('instance folders not exists. creating folders')

    except OSError:
        app.logger.info('instance folders exists. pass creating folders')
        pass

    # register the database commands
    #
    db.init_app(app)
    app.logger.info('Base instance initialization complete')

    # apply the blueprints to the app
    from marktool.home import home
    from marktool.auth import auth
    from marktool.area import area
    from marktool.error import error
    app.logger.info('Import Blueprints')

    app.register_blueprint(home.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(area.bp)
    app.register_blueprint(error.bp)
    app.logger.info('Register Blueprints')

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule('/', endpoint="home")
    app.add_url_rule('/registration', endpoint="registration")
    app.add_url_rule('/login', endpoint="login")
    app.add_url_rule('/logout', endpoint="logout")
    app.add_url_rule('/confirm_registration', endpoint="confirm_registration")
    app.add_url_rule('/area', endpoint="area")
    app.add_url_rule('/marked', endpoint="marked")
    app.add_url_rule('/action20', endpoint="action20")
    app.logger.info('Adding rules Blueprints')

    return app
