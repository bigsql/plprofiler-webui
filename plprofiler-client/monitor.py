from flask import (
    Blueprint, g, render_template, request, session, current_app, url_for
)

from db import get_db
from plprofiler import plprofiler

bp = Blueprint('monitor', __name__, url_prefix='/monitor')
plp = None

@bp.route('/', methods=('GET', 'POST'))
def monitor():
    db = get_db();
    stored_servers = db.execute('SELECT * FROM databases d').fetchall()


    if request.method == 'POST':

        # Connect to database, check for plprofiler extension, check if global profiling enabled
        if request.form['submit'] == 'connect':

            # Set options for connecting
            connoptions = {}
            connoptions['host']     = request.form['host']
            connoptions['port']     = request.form['port']
            connoptions['user']     = request.form['username']
            connoptions['database'] = request.form['dbname']
            session['connoptions']  = connoptions

            try:
                # Connect/check for plprofiler extension
                global plp

                plp = plprofiler()
                plp.connect(connoptions)
                session['plprofiler_present'] = True

                # Check if global profiling is enabled
                session['global_enabled'] = check_global_enabled(plp)
                session['interval'] = get_monitoring_interval(plp)
            except Exception as err:
                if str(err).find('plprofiler extension not found'):
                    session['plprofiler_present'] = False

                print(str(err) + '\n')
                session['error'] = str(err)

                return render_template('monitor.html',
                                   server_list=stored_servers,
                                   session=session)

        # Enable global profiling
        elif request.form['submit'] == 'enable_global':
            try:
                plp.enable_monitor()
                session['global_enabled'] = check_global_enabled(plp)
                session['interval'] = get_monitoring_interval(plp)
            except Exception as err:
                print(str(err) + '\n')
                session['error'] = str(err)

                return render_template('monitor.html',
                                   server_list=stored_servers,
                                   session=session)

        # Disable global profiling
        elif request.form['submit'] == 'disable_global':
            try:
                plp.disable_monitor()
                session['global_enabled'] = check_global_enabled(plp)
                session['interval'] = get_monitoring_interval(plp)
            except Exception as err:
                print(str(err) + '\n')
                session['error'] = str(err)

                return render_template('monitor.html',
                                   server_list=stored_servers,
                                   session=session)

        elif request.form['submit'] == 'reset':
            try:
                plp.reset_shared()
            except Exception as err:
                print(str(err) + '\n')
                session['error'] = str(err)

                return render_template('monitor.html',
                                   server_list=stored_servers,
                                   session=session)

        elif request.form['submit'] == 'save':
            try:
                name     = request.form['name']
                title    = request.form['title']
                desc     = request.form['desc']
                force    = request.form.getlist('force')[0] \
                           if len(request.form.getlist('force')) > 0 \
                           else False

                if not name:
                    name = 'current'
                if not title:
                    title = 'PL PROFILER REPORT for %s' %(name, )
                if not desc:
                    desc = ("<h1>PL Profiler Report for %s</h1>\n" +
                            "<p>\n<!-- description here -->\n</p>") %(name, )

                config = {
                    'name':         name,
                    'title':        title,
                    'tabstop':      8,
                    'svg_width':    1200,
                    'table_width':  '80%',
                    'desc':         desc,
                }

                plp.save_dataset_from_shared(name, config, force)
            except Exception as err:
                print(str(err) + '\n')
                session['error'] = str(err)

                return render_template('monitor.html',
                                   server_list=stored_servers,
                                   session=session)

    if request.method == 'GET':
        session['plprofiler_present'] = None
        session['global_enabled'] = None
        session['interval'] = None
        session['error'] = ""
        connoptions = {}
        connoptions['host']     = ''
        connoptions['port']     = ''
        connoptions['database'] = ''
        session['connoptions']  = connoptions

    session['error'] = ''
    return render_template('monitor.html',
                           server_list=stored_servers,
                           session=session)

# Checks to see if global profiling is enabled once connected to a database
def check_global_enabled(plp):
    cur = plp.dbconn.cursor()
    cur.execute("""SELECT pl_profiler_get_enabled_global()""")
    return cur.fetchone()[0]

def get_monitoring_interval(plp):
    cur = plp.dbconn.cursor()
    cur.execute("""SELECT pl_profiler_get_collect_interval()""")
    return cur.fetchone()[0]
