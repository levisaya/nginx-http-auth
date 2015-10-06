from flask import Flask, request, session, redirect, Response, render_template
import os
import click
import logging
logging.basicConfig()
import traceback

@click.command()
@click.option('--config_module', default='authorizers.test_auth', help='Import of the configuration module.')
@click.option('--port', default=80, help='Port ot serve on.')
@click.option('--secret_key', default=os.urandom(24), help='Secret key.')
@click.option('--template', default='templates/login_form.html', help='Path to the template to render.')
def server(config_module, port, secret_key, template):
    app = Flask(__name__)

    config = __import__(config_module, globals(), locals(), ['object'], 0)

    @app.route('/auth-proxy', methods=['GET'])
    def auth():
        if 'nginxauth' in session:
            username, password = session['nginxauth'].split(chr(0))
            if config.authenticate(request, username, password):
                return Response('Authenticated!', 200, {})
        return Response('Authentication Required', 401, {})


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            session['nginxauth'] = request.form['username'] + chr(0) + request.form['password']
            return redirect(request.headers['Origin'] + request.form['target'])
        else:
            return render_template(template, target=request.headers['X-Target'])


    @app.route('/')
    def test_backend():
        return "Hello from the test backend!"

    @app.errorhandler(500)
    def catch_server_errors(e):
        logging.exception("Something awful happened!")

    options = {}

    for option in ['port', 'secret_key', 'template']:
        # Try the configuration file.
        options[option] = getattr(config, option, None)
        if options[option] is None:
            try:
                # If not specified in the config, fall back to defaults/command line.
                options[option] = locals()[option]
            except AttributeError:
                # Set to None earlier; Fall through.
                pass

    app.secret_key = options['secret_key']
    app.run(host='0.0.0.0', port=options['port'])

if __name__ == '__main__':
    server()