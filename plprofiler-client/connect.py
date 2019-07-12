import os

from flask import (
    Blueprint, g, render_template, request, session, url_for, flash, g, redirect, current_app
)

from plprofiler import plprofiler, plprofiler_tool

bp = Blueprint('connect', __name__, url_prefix='/connect')

@bp.route('/', methods=('GET', 'POST'))
def connect():
    if request.method == 'POST':
        host     = request.form['host']
        port     = request.form['port']
        username = request.form['username']
        password = request.form['password']
        database = request.form['dbname']
        query    = request.form['query']

        error = None

        if not host:
            error = 'Host is required'
        if not port:
            error = 'Port is required'
        if not database:
            error = 'Database is required'
        if not username:
            error = 'Username is required.'

        args = ['--command']
        args.append(query)
        args.append('-h')
        args.append(host)
        args.append('-p')
        args.append(port)
        args.append('-d')
        args.append(database)
        args.append('-U')
        args.append(username)

        args.append('--name')
        args.append('test')

        args.append('--title')
        args.append('test title')

        args.append('--desc')
        args.append('test description')

        dirpath = os.path.join(current_app.root_path, 'templates/test.html')
        print(dirpath)
        args.append('--output')
        args.append(dirpath)

        try:
            a = plprofiler_tool.run_command(args)
            if a is 0:
                return render_template('/test.html')

            print('a: ' + a + '\n')
        except Exception as err:
            print('error: ' + str(err) + '\n')

    return render_template('connect.html')
