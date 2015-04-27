from flask import Flask, request
from flask.ext.restful import Resource, Api
import fred

app = Flask(__name__)
api = Api(app)

class Series(Resource):
    def get(self, **kwargs):
        res = fred.get('series', kwargs)
        return res['result'], res['status_code']

class SeriesSearch(Resource):
    def get(self, **kwargs):
        res = fred.get('series/search', kwargs)
        return res['result'], res['status_code']

api.add_resource(Series, '/series')
api.add_resource(SeriesSearch, '/series/search')

if __name__ == '__main__':
    app.run(debug=True)
