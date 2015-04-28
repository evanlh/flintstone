from flask import Flask, request
from flask.ext.restful import Resource, Api
from flask.ext.restful import reqparse
import fred

app = Flask(__name__)
api = Api(app)

class Series(Resource):
    def get(self, **kwargs):
        parser = reqparse.RequestParser()
        parser.add_argument('series_id', type=str, help='The id for a series')
        args = parser.parse_args()
        if not args.has_key('limit'):
            args['limit'] = 100000

        res = fred.get('series', args)
        return res['result'], res['status_code']

class SeriesSearch(Resource):
    def get(self, **kwargs):
        parser = reqparse.RequestParser()
        parser.add_argument('search_text', type=str, help='Keywords to search series by')
        parser.add_argument('limit', type=int, help='Max number of results to return')
        parser.add_argument('offset', type=int, help='Offset into results set')
        parser.add_argument('order_by', type=str, help='Order results by ...')
        parser.add_argument('sort_order', type=str, help='Sort: asc or desc')
        args = parser.parse_args()
        if not args.has_key('limit'):
            args['limit'] = 1000

        print args
        res = fred.get('series/search', args)
        return res['result'], res['status_code']

api.add_resource(Series, '/series')
api.add_resource(SeriesSearch, '/series/search')

if __name__ == '__main__':
    app.run(debug=True)
