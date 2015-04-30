import requests
from pymongo import MongoClient
import settings
import datetime
import json
import time

DEBUG = True

client = MongoClient(settings.MONGOURL)
cache = client.flintstone.cache

###############################
# Core FRED API interface
###############################
last_query = datetime.datetime.now()
api_wait = 2 # second

def get(path, params, cache=True):
    global last_query
    global api_wait

    if cache:
        key = cache_key(path, params)
        print key
        print params
        result = get_from_cache(key)
        if result:
            return { "status_code": 200, "result": result }

    # make sure we wait api_wait seconds since the last query
    delta = datetime.datetime.now() - last_query
    if delta.seconds < api_wait:
        time.sleep(api_wait - delta.seconds)

    if DEBUG:
        print path
        print params

    url = settings.APIROOT + path
    query = params.copy()
    query['api_key'] = settings.FRED_API_KEY
    if not query.has_key('file_type'):
        query['file_type'] = 'json'
    result = requests.get(url, params=query)

    # TODO paging?
    if result.status_code == 200:
        decoded = json.loads(result.text)
        if cache:
            put_in_cache(key, decoded)
        return { "status_code": 200, "result" : decoded }

    # Common rate-limiting status codes, back off by doubling api_wait
    elif result.status_code == 403 or result.status_code == 420 or result.status_code == 429:
        api_wait = api_wait*2

    last_query = datetime.datetime.now()
    return { "status_code" : result.status_code, "result" : result.reason, "text":  result.text }


# Turn path & query parameters into a sorted json hash
def cache_key(path, params):
    if not isinstance(params, dict):
        print type(params)
        params = {}
    # sort keys for consistency
    key = { x: params[x] for x in sorted(params.keys()) }
    # append path
    key['path'] = path
    return json.dumps(key)

def get_from_cache(key):
    res = cache.find_one({
        "_id": key,
        "cached_on": {"$gt": datetime.datetime.now() - datetime.timedelta(days=settings.CACHEDAYS)}
    })
    if res and res['result']:
        return res['result']
    return None

def put_in_cache(key, result):
    query = { "_id" : key }
    payload = { '$set': {
        "query": json.loads(key),
        "result": result,
        "cached_on": datetime.datetime.now()
    }}
    cache.update_one(query, payload, upsert=True)


##############################
# FRED Categories local mirror
##############################
categoriesdb = client.flintstone.categories

def scrape_categories(category_id=0):
    res = get('category/children', { "parent_id": category_id })
    print res
    if res['status_code'] == 200 and res['result'] and res['result']['categories']:
        # insert to mongo, TODO batch api
        for cat in res['result']['categories']:
            categoriesdb.update_one({ 'id': cat['id'] }, {'$set': cat}, upsert=True)
        for cat in res['result']['categories']:
            scrape_categories(cat['id'])

############################
# FRED Series local mirror
############################
seriesdb = client.flintstone.series
def get_series_by_category(category_id):
    pass
