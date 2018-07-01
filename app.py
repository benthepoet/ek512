import bottle
import datetime
import json

from routes import auth, documents, users

class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return str(obj.strftime("%Y-%m-%d %H:%M:%S"))
        return json.JSONEncoder.default(self, obj)

app = bottle.app()
app.install(bottle.JSONPlugin(json_dumps=lambda s: json.dumps(s, cls=JsonEncoder)))

if __name__ == '__main__':
    bottle.run(app=app)