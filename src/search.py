import os
import subprocess

import pymongo
from bottle import route, run, template, error, static_file, request

from config import settings, templates


def search_company(company):
    try:
        conn = pymongo.MongoClient(
            settings.MONGODB_URI,
            serverSelectionTimeoutMS=50
        )
        db = conn[settings.MONGODB_DB]
        ppl_coll = db[settings.MONGODB_PEOPLE]
        cmp_coll = db[settings.MONGODB_COMPANIES]
        cmp = cmp_coll.find_one({'company': company})

        emp_tplt = '''
Employees of the company {company}:

{txt}'''

        no_emp_tplt = '''
Company '{c}' has no employees.'''

        no_cmp_tplt = '''
Company '{c}' doesn't exist.'''

        if cmp:
            cmp_id = cmp['index']
            ppl = ppl_coll.find({'company_id': cmp_id})
            if ppl.count() > 0:
                ppl = [person['name'] for person in ppl]
                ppl = emp_tplt.format(company=company, txt='\n'.join(ppl))
                return ppl
            else:
                return no_emp_tplt.format(c=company)
        else:
            return no_cmp_tplt.format(c=company)

    except pymongo.errors.ServerSelectionTimeoutError:
        return "Sorry!!! Unable to connect to {db}".format(db=settings.MONGODB_DB)


def segregate_favourites(ppl):
    fruits = settings.FRUITS
    vegetables = settings.VEGETABLES

    favs = ppl.pop('favouriteFood')
    ppl['fruits'] = list(set(fruits).intersection(set(favs)))
    ppl['vegetables'] = list(set(vegetables).intersection(set(favs)))

    return ppl


def find_person(person, find_friends=False, id=None):
    try:
        conn = pymongo.MongoClient(
            settings.MONGODB_URI,
            serverSelectionTimeoutMS=50
        )
        db = conn[settings.MONGODB_DB]
        ppl_coll = db[settings.MONGODB_PEOPLE]
        fields = {"name": 1, "age": 1, "address": 1, "phone": 1, "friends": 1, "_id": 0} if find_friends else {
            "name": 1, "age": 1, "favouriteFood": 1, "_id": 0}
        ppl = ppl_coll.find_one({'name': person}, fields)
        return ppl

    except pymongo.errors.ServerSelectionTimeoutError:
        print("Unable to connect to settings {db}".format(db=settings.MONGODB_DB))


def get_name_by_index(idx_list):
    try:
        conn = pymongo.MongoClient(
            settings.MONGODB_URI,
            serverSelectionTimeoutMS=50
        )
        db = conn[settings.MONGODB_DB]
        ppl_coll = db[settings.MONGODB_PEOPLE]
        fields = {"name": 1, "_id": 0}
        conditions = {'index': {'$in': idx_list}, "eyeColor": "brown", "has_died": False}
        ppl = list(ppl_coll.find(conditions, fields))
        if ppl:
            ppl = [x['name'] for x in ppl]
        return ppl

    except pymongo.errors.ServerSelectionTimeoutError:
        print("Unable to connect to settings {db}".format(db=settings.MONGODB_DB))


def search_person(person):
    ppl = find_person(person)
    if ppl:
        ppl = segregate_favourites(ppl)
        res = '''
'''
        res_tplt = '''Name: {name}, Age: {age}, Fruits: {fruits}, Vegetables: {veg}'''
        res += res_tplt.format(name=ppl['name'], age=ppl['age'], fruits=ppl['fruits'], veg=ppl['vegetables'])
        return res
    else:
        return '''
People named '{person}' not found.'''.format(person=person)


def find_common(person1, person2):
    if person1 == person2:
        return '''
You entered the same name twice'''
    ppl1 = find_person(person1, True)
    ppl2 = find_person(person2, True)

    if not ppl1 or not ppl2:
        return '''
One or Both of the people you searched for do not exist'''

    friends1 = ppl1.pop('friends')
    friends2 = ppl2.pop('friends')
    friends1 = [x['index'] for x in friends1]
    friends2 = [x['index'] for x in friends2]
    res = '''
1st Person: '''
    res += '\n'
    res_tplt = 'Name: {name}, Age: {age}, Address: {address}, phone: {phone}'
    res += res_tplt.format(
        name=ppl1['name'], age=ppl1['age'], address=ppl1['address'], phone=ppl1['phone'])
    res += '\n'
    res += '\n'

    res += '2nd Person: '
    res += '\n'
    res += res_tplt.format(
        name=ppl2['name'], age=ppl2['age'], address=ppl2['address'], phone=ppl2['phone'])

    common = list(set(friends1).intersection(set(friends2)))
    common = get_name_by_index(common)
    if common:
        common = '\n'.join(common)
        res += '\n'
        res += '''

Friends in common with brown eyes:

{txt}'''.format(txt=common)
    else:
        res += '''

They don't have any friends in common who are alive and have brown eyes'''

    return res


@route('/')
@route('/search/')
def search():
    tpl = templates.tpl_home
    return template(tpl)


@route('/', method="POST")
@route('/search/company', method="POST")
def formhandler():
    company = request.forms.get('company').strip()
    ppl = search_company(company)
    tpl = templates.tpl_start + templates.tpl_form_cmp.format(res_tag=ppl) \
          + templates.tpl_form_ppl.format(res_tag='') + templates.tpl_end
    return tpl


@route('/', method="POST")
@route('/search/people', method="POST")
def formhandler():
    ppl1 = request.forms.get('p1').strip()
    ppl2 = request.forms.get('p2').strip()
    if ppl2:
        res = find_common(ppl1, ppl2)
    else:
        res = search_person(ppl1)
    tpl = templates.tpl_start + templates.tpl_form_ppl.format(res_tag=res) \
          + templates.tpl_form_cmp.format(res_tag='') + templates.tpl_end
    return template(tpl)


@route('/<filename>')
def server_static(filename):
    cwd = os.getcwd()
    root = cwd + '/config'
    return static_file(filename, root=root)


@error(404)
def error404(error):
    return templates.tpl_404


if os.path.isfile('/sys/hypervisor/uuid') \
        and 'ec2' in subprocess.check_output(['head', '-1', '/sys/hypervisor/uuid']).decode():
    host = subprocess.check_output(['curl', 'http://169.254.169.254/latest/meta-data/public-hostname']).decode()
    run(server='auto', host=host, port=8080)
else:
    run()