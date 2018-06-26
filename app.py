import bottle

import resources.auth

app = bottle.app()

if __name__ == '__main__':
    bottle.run(app=app)