from flask import Flask, request, abort, redirect
import logging
logging.basicConfig()
import base64

app = Flask(__name__)

totally_secure_auth_users = {'admin': 'password'}

@app.route('/', methods=['GET'])
def the_goods():
    return 'The Goods!'

@app.route('/auth-proxy', methods=['GET'])
def auth():
    nginx_auth = request.headers.get('nginxauth', None)

    if nginx_auth is None:
        return 'Auth Required', 401
    else:
        user, passwd = nginx_auth[:nginx_auth.find(';').split(':')]
        print(user, passwd)
        if user in totally_secure_auth_users and totally_secure_auth_users[user] == passwd:
            return "", 200
        else:
            return 'Auth Required', 401

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # try to get target location from header
        target = request.headers.get('X-Target', None)

        # form cannot be generated if target is unknown
        if target is None:
            logging.error('target url is not passed')
            abort(500)

        html = """
                <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
                <html>
                  <head>
                    <meta http-equiv=Content-Type content="text/html;charset=UTF-8">
                    <title>Auth form example</title>
                  </head>
                  <body>
                    <form action="/login" method="post">
                      <table>
                        <tr>
                          <td>Username: <input type="text" name="username"/></td>
                        <tr>
                          <td>Password: <input type="text" name="password"/></td>
                        <tr>
                          <td><input type="submit" value="Login"></td>
                      </table>
                        <input type="hidden" name="target" value="{}">
                    </form>
                  </body>
                </html>"""

        return html.format(target)
    else:
        user = request.form['username']
        passwd = request.form['password']
        target = request.form['target']

        response = app.make_response(redirect(target))
        response.set_cookie('nginxauth', value=user + ':' + passwd + '; httponly')
        response.headers['Location'] = target
        return response

if __name__ == '__main__':
    app.run(port=7777)