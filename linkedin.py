from linkedin import linkedin

# Define CONSUMER_KEY, CONSUMER_SECRET,
# USER_TOKEN, and USER_SECRET from the credentials
# provided in your LinkedIn application

CONSUMER_KEY = 7
CONSUMER_SECRET = 8
USER_TOKEN = 9
USER_SECRET = 4

# Instantiate the developer authentication class
RETURN_URL = 'http://localhost:8080'


authentication = linkedin.LinkedInDeveloperAuthentication(
                    CONSUMER_KEY,
                    CONSUMER_SECRET,
                    USER_TOKEN,
                    USER_SECRET,
                    RETURN_URL,
                    linkedin.PERMISSIONS.enums.values()
                )

# Optionally one can send custom "state" value that will be returned from OAuth server
# It can be used to track your user state or something else (it's up to you)
# Be aware that this value is sent to OAuth server AS IS - make sure to encode or hash it

# authorization.state = 'your_encoded_message'

# Pass it in to the app...

application = linkedin.LinkedInApplication(authentication)

# Use the app....

application.get_profile()