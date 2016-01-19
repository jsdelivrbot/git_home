from . import auth

@auth.route('/')
@auth.route('/home')
def home():
    return "<h1>Welcome</h1>"
