from flask import Flask, request, session, redirect, Response, render_template
import os
import click
import logging
logging.basicConfig()


local_dir = os.path.abspath(os.path.join(__file__, '..'))


@click.command()
@click.option('--config_module', default='authorizers.test_auth', help='Import of the configuration module.')
@click.option('--port', default=80, help='Port ot serve on.')
@click.option('--secret_key', default=os.urandom(24), help='Secret key.')
@click.option('--template',
              default='login_form.html',
              help='Path to the template to render.')
def server(config_module, port, secret_key, template):
    app = Flask(__name__, template_folder=os.path.abspath(os.path.join(__file__, '..', 'templates')))

    config = __import__(config_module, globals(), locals(), ['object'], 0)

    @app.route('/auth-proxy', methods=['GET'])
    def auth():
        # Try to validate an existing session first.
        sid = session.get('sid', None)
        if sid is not None:
            if config.validate_session(int(sid)):
                return Response('Authenticated!', 200, {})
            else:
                # sid was invalid- either the session expired, was removed, or was bogus in the first place.
                # Clear it from the session, then fall out to check for auth_credentials.
                session.pop('sid')

        # No existing session. See if credentials a present in the session to validate.
        if 'auth_credentials' in session:
            username, password = session.pop('auth_credentials').split(chr(0))
            success, sid = config.authenticate(request, username, password)
            session.modified = True
            if success:
                # Set the sid on the session to be persisted to subsequent requests.
                session['sid'] = str(sid)
                return Response('Authenticated!', 200, {})
        return Response('Authentication Required', 401, {})

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            # Parse the credentials from the form and save them on the session to be processed later.
            session['auth_credentials'] = request.form['username'] + chr(0) + request.form['password']

            # Redirect to wherever the user was trying to go in the first place.
            return redirect(request.headers['Origin'] + request.form['target'])
        else:
            # Present the login form, with a hidden target field to redirect with later.
            return render_template(template, target=request.headers['X-Target'])

    @app.route('/')
    def test_backend():
        return "Hello from the test backend!"

    @app.errorhandler(500)
    def catch_server_errors(e):
        logging.exception("Exception Caught!")

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
    app.run(host='0.0.0.0',
            port=options['port'])

if __name__ == '__main__':
    server()