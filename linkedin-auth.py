
from linkedin import linkedin

APPLICATON_KEY    = '78hh02ldxxcnrh'
APPLICATON_SECRET = 'X7ybGWKcUlhjkdff'

# RETURN_URL = 'https://job-matcher-hack-n-roll.herokuapp.com/auth'
RETURN_URL = 'http://127.0.0.1:5000//auth'

authentication = linkedin.LinkedInAuthentication(
                    APPLICATON_KEY,
                    APPLICATON_SECRET,
                    RETURN_URL,
                    ['r_basicprofile']
                )

print ('Auth url: ', authentication.authorization_url)  # open this url on your browser

print('Waiting for auth code ...')
code = input()
authentication.authorization_code = code
result = authentication.get_access_token()
print ("Access Token:", result.access_token)

application = linkedin.LinkedInApplication(token=result.access_token)
print(application.get_profile())







