import os
import threading
import webbrowser
from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect

def create_app():
    # to make oauth2 work with http
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    # config
    client_id = 'TRADELAB-TEST'
    web_url = 'https://mimik.tradelab.in'
    client_secret = 'XYZ8eoAf0s4l1PPSJQBzFEX10ytP6lBLTBYJn10gYLYIWJqpOcn9zEYI96SJRzZ1'
    redirect_uri = 'http://127.0.0.1:65010'
    authorization_base_url = f'{web_url}/oauth2/auth'
    token_url = f'{web_url}/oauth2/token'
    scope='orders holdings'
    # state='https://www.google.com'
    # creating instance of Flask
    app = Flask(__name__)
    # access token
    access_token = None

    @app.route('/getcode')
    def get_authorization_url():
        oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
        authorization_url, _state = oauth.authorization_url(authorization_base_url, access_type="authorization_code")
        print('authorization_url')
        print(authorization_url)
        return redirect(authorization_url)

    @app.route('/')
    def callback():
        global access_token
        print("Inside callback function")
        oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
        token = oauth.fetch_token(token_url, authorization_response=request.url, client_secret=client_secret)
        print(token)
        access_token = token['access_token']
        f=open("access_token.txt", "a+")
        f.write(access_token)
        f.close()
        print('access token is:', access_token)

        ## we will be shutting down the server after getting access_token
        ## the thread created here is copied in if __name__ == '__main__' block
        ## and will run after closing the server

        # th = threading.Thread(target=data_from_resource_server, args=(access_token,))
        # th.start()

        func = request.environ.get('werkzeug.server.shutdown')
        if func:
            print('stoping server')
            func()


        return 'see terminal for logs'

    return app

if __name__ == '__main__':
    app = create_app()
    # app.secret_key = 'example'
    # app.env = 'development'
    # print()
    print('Open this url in browser:', 'http://127.0.0.1:65010/getcode', end='\n\n')

    app.run(host='127.0.0.1', debug=False, port=65010)
    webbrowser.open('127.0.0.1:65010/getcode')
    print('server stopped')

    ## got access_token, closed the server, now running ray integration code
    if access_token:
        th = threading.Thread(target=data_from_resource_server, args=(access_token,))
        th.start()