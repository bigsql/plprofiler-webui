import os

from flask import (
    Blueprint, g, render_template, request, redirect, current_app, url_for
)

from db import get_db

from plprofiler import plprofiler, plprofiler_tool

bp = Blueprint('direct_profile', __name__, url_prefix='/direct_profile')

@bp.route('/', methods=('GET', 'POST'))
def direct_profile():
    if request.method == 'POST':
        host     = request.form['host']
        port     = request.form['port']
        username = request.form['username']
        password = request.form['password']
        database = request.form['dbname']
        query    = request.form['query']
        name     = request.form['result_name']
        title    = request.form['result_title']
        desc     = request.form['result_description']

        error = None

        if not host:
            error = 'Host is required'
        if not port:
            error = 'Port is required'
        if not database:
            error = 'Database is required'
        if not username:
            error = 'Username is required.'
        if not query:
            error = 'query is required'

        if not name:
            name = 'current'
        if not title:
            title = 'PL PROFILER REPORT for %s' %(name, )
        if not desc:
            desc = ("<h1>PL Profiler Report for %s</h1>\n" +
                    "<p>\n<!-- description here -->\n</p>") %(name, )

        args = ['--command']
        args.append(str(query))

        args.append('-h')
        args.append(str(host))

        args.append('-p')
        args.append(str(port))

        args.append('-d')
        args.append(str(database))

        args.append('-U')
        args.append(str(username))

        args.append('--name')
        args.append(str(name))

        args.append('--title')
        args.append(str(title))

        args.append('--desc')
        args.append(str(desc))

        dirpath = os.path.join(current_app.root_path, 'templates/test.html')
        args.append('--output')
        args.append(dirpath)

        try:
            a = plprofiler_tool.run_command(args)
            if a is 0:
                return render_template('/test.html')

            elif a is 1:
                error = "Could not connect to server"
        except Exception as err:
            print('error: ' + str(err) + '\n')

    db = get_db();

    stored_servers = db.execute('SELECT * FROM databases d').fetchall()
    return render_template('direct_profile.html', server_list=stored_servers)
