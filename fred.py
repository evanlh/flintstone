import requests
from pymongo import MongoClient
import settings
import datetime
import json

client = MongoClient(settings.MONGOURL)
cache = client.econocards.cache

# TODO api rate-limiting
def get(path, params, cache=True):
    if cache:
        key = cache_key(path, params)
        result = get_from_cache(key)
        if result:
            return { "status_code": 200, "result": result }

    url = settings.APIROOT + path
    query = params.copy()
    query['api_key'] = settings.FRED_API_KEY
    if not query.has_key('file_type'):
        query['file_type'] = 'json'
    if not query.has_key('limit'):
        query['limit'] = 100000

    result = requests.get(url, params=query)
    # TODO paging?
    if result.status_code == 200:
        decoded = json.loads(result.text)
        if cache:
            put_in_cache(key, decoded)
        return { "status_code": 200, "result" : decoded }
    # TODO error handling
    return { "status_code" : result.status_code, "result" : result.reason }

def cache_key(path, params):
    if not type(params) is dict:
        params = {}
    key = params.copy()
    key['path'] = path
    return json.dumps(key)

def get_from_cache(key):
    res = cache.find_one({"_id": key, "expires": {"$gt": datetime.datetime.now() }})
    if res and res['result']:
        return res['result']
    return None

def put_in_cache(key, result):
    print key
    print result

    payload = { "_id" : key, "query": json.loads(key), "result": result }
    payload['expires'] = datetime.datetime.now() + datetime.timedelta(days=settings.CACHEDAYS)
    cache.insert_one(payload)
