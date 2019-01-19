from flask import Flask, redirect, request
from linkedin import linkedin
app = Flask(__name__)

DOMAIN = 'http://127.0.0.1:5000'
# DOMAIN = 'https://job-matcher-hack-n-roll.herokuapp.com'
RETURN_URL = f'{DOMAIN}/auth'

APPLICATON_KEY    = '78hh02ldxxcnrh'
APPLICATON_SECRET = 'X7ybGWKcUlhjkdff'


@app.route("/")
def start():
    return "<a href='/linkedin'><img src='static/images/linkedin-signin.png'></img></a>"

@app.route("/linkedin")
def linkedin_redirect():
    authentication = linkedin.LinkedInAuthentication(
                        APPLICATON_KEY,
                        APPLICATON_SECRET,
                        RETURN_URL,
                        ['r_basicprofile']
                    )
    print(dir(authentication))
    return redirect(authentication.authorization_url, code=302)


@app.route("/auth")
def auth():
    authentication = linkedin.LinkedInAuthentication(
                    APPLICATON_KEY,
                    APPLICATON_SECRET,
                    RETURN_URL,
                    ['r_basicprofile']
                )
    auth_code = request.args.get('code', default = None, type = str)
    authentication.authorization_code = auth_code
    token = authentication.get_access_token().access_token

    li_application = linkedin.LinkedInApplication(token=token)
    print(li_application.get_profile())
    return redirect('/user')


@app.route("/user")
def user_authenticated():
    # li_profile = linkedin.LinkedInApplication(token=authentication.get_access_token().access_token)
    return 'Tailored lakjkdsfj'



