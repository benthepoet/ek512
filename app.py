import bottle
from api import app

if __name__ == '__main__':
    bottle.run(app=app)