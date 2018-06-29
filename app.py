import bottle

from routes import auth, documents, users

app = bottle.app()

if __name__ == '__main__':
    bottle.run(app=app)