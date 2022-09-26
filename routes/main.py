from flask import Blueprint, render_template

MainRoute = Blueprint('main',__name__,url_prefix='/')

@MainRoute.route('/',methods=['GET'])
def index():
    return render_template('index.html')
