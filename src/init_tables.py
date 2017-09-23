import json

import pymongo

from config import settings

try:
    conn = pymongo.MongoClient(
                settings.MONGODB_URI,
                serverSelectionTimeoutMS=50
                )
    db = conn[settings.MONGODB_DB]
    ppl_coll = db[settings.MONGODB_PEOPLE]
    cmp_coll = db[settings.MONGODB_COMPANIES]

    ppl = []
    cmp = []

    with open(settings.PPL_JSON, mode='r') as ppl_file:
        ppl = json.loads(ppl_file.read())

    with open(settings.CMP_JSON, mode='r') as cmp_file:
        cmp = json.loads(cmp_file.read())

    ppl_coll.remove()
    ppl_coll.insert(ppl)
    cmp_coll.remove()
    cmp_coll.insert(cmp)
except pymongo.errors.ServerSelectionTimeoutError:
    print("Unable to connect to settings {db}".format(db=settings.MONGODB_DB))

