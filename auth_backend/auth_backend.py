from flask import Flask, request, session, redirect, Response, render_template
import logging
logging.basicConfig()
import os


def server(port=80, secret_key=os.urandom(24)):
    app = Flask(__name__)

    @app.route('/auth-proxy', methods=['GET'])
    def auth():
        if 'nginxauth' in session:
            username, password = session['nginxauth'].split(chr(0))
            if username == 'test' and password == 'test':
                return Response('Authenticated!', 200, {})
        return Response('Authentication Required', 401, {})


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            session['nginxauth'] = request.form['username'] + chr(0) + request.form['password']
            return redirect(request.headers['Origin'] + request.form['target'])
        else:
            return  '''
                    <form action="login" method="post">
                        <p><input type="text" name="username">
                        <p><input type="password" name="password">
                        <input type="hidden" name="target">
                        <p><input type="submit" value="Login">
                    </form>'''.format(request.headers['X-Target'])

    @app.route('/')
    def test_backend():
        return "Hello from the test backend!"

    app.secret_key = secret_key
    app.run(port=port)

if __name__ == '__main__':
    server()