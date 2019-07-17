from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from db import get_db

bp = Blueprint('define_connections', __name__, url_prefix='/define_connections')

@bp.route('/', methods=('GET', 'POST'))
def register_connection():
    if request.method == 'POST':
        servername = request.form['servername']
        host = request.form['host']
        port = request.form['port']
        dbname = request.form['dbname']

        db = get_db()

        error = None

        if not host:
            error = 'host is required'

        elif not port:
            error = 'port is required.'

        elif not dbname:
            error = 'dbname is required'

        elif db.execute('SELECT * \
                         FROM databases AS d \
                         WHERE d.servername = ?',
                         (servername,)
                        ).fetchone() is not None:
                            error = 'A database with that name is already stored'

        if error is None:
            db.execute(
                'INSERT INTO databases (servername, host, port, name) \
                                VALUES (?, ?, ?, ?)',
                                       (servername, host, port, dbname)
            )

            db.commit()

            return redirect(url_for('home'))

        flash(error)

    return render_template('define_connections.html')
