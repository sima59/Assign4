"""
The Flask documentation provides this code as the suggested pattern for working with SQLite i Flask:
https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
"""
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    # the 'g' object is a piece of magic described here: https://flask.palletsprojects.com/en/1.1.x/api/#flask.g
    if "db" not in g:
        # the sqlite3 library is a built-in Python module: https://docs.python.org/3/library/sqlite3.html#sqlite3.connect
        g.db = sqlite3.connect(
            # since Flask can specify different apps to work with, the `current_app` object
            # provides a reference to the application in current use: https://flask.palletsprojects.com/en/1.1.x/api/#flask.current_app
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """Clear existing data and create new tables."""    
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """    
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
