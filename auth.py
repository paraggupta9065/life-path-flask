from main import bp

@bp.route('/login')
def index():
    return 'This is The Main Blueprint'

