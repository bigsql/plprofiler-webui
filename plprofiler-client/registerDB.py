from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from db import get_db

bp = Blueprint('registerDB', __name__, url_prefix='/registerDB')

@bp.route('/', methods=('GET', 'POST'))
def registerDB():
    if request.method == 'POST':
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
                         WHERE d.host = ? AND \
                               d.port = ? AND \
                               d.name = ?', (host, port, dbname,)
                        ).fetchone() is not None:
                            error = 'A database with those values is already stored'

        if error is None:
            db.execute(
                'INSERT INTO databases (host, port, name) VALUES (?, ?, ?)',
                (host, port, dbname)
            )

            db.commit()

            return redirect(url_for('home'))

        flash(error)

    return render_template('registerDB.html')
