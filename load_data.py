import json
from csv import DictReader
import requests
import io

url_csv = 'https://storage.googleapis.com/juntossomosmais-code-challenge/input-backend.csv'
response_csv = requests.get(url_csv)
response_csv.encoding = 'utf-8'
users_csv = io.StringIO(response_csv.text, newline="")
users_csv = DictReader(users_csv, delimiter=',')


url_json = 'https://storage.googleapis.com/juntossomosmais-code-challenge/input-backend.json'
response_json = requests.request('GET', url_json)
users_json = response_json.json()


dict_regions = {'acre': 'norte', 'amapá': 'norte', 'amazonas': 'norte', 'pará': 'norte', 'rondônia': 'norte', 
                'roraima': 'norte', 'tocantins': 'norte', 'alagoas': 'nordeste', 'bahia': 'nordeste',
                'ceará': 'nordeste', 'maranhão': 'nordeste', 'paraíba': 'nordeste', 'pernambuco': 'nordeste',
                'piauí': 'nordeste', 'rio grande do norte': 'nordeste', 'sergipe': 'nordeste', 'goiás': 'cetro oeste',
                'mato grosso': 'cetro oeste', 'mato grosso do sul': 'cetro oeste', 'distrito federal': 'cetro oeste',
                'são paulo': 'sudeste', 'rio de janeiro': 'sudeste', 'espírito santo': 'sudeste', 'minas gerais':
                'sudeste', 'paraná': 'sul', 'santa catarina': 'sul', 'rio grande do sul': 'sul'}


"""
def dict_regions():
    norte = 'acre, amapá, amazonas, pará, rondônia, roraima, tocantins'
    nordeste = 'alagoas, bahia, ceará, maranhão, paraíba, pernambuco, piauí, rio grande do norte, sergipe'
    centro = 'goiás, mato grosso, mato grosso do sul, distrito federal'
    sudeste = 'são paulo, rio de janeiro, espírito santo, minas gerais'
    sul = 'paraná, santa catarina, rio grande do sul'
    lista = ['norte', 'nordeste', 'cetro oeste', 'sudeste', 'sul']
    lista_estado = [norte, nordeste, centro, sudeste, sul]
    dict_region = dict()
    [dict_region.update(dict.fromkeys(k.split(', '), v)) for k, v in zip(lista_estado, lista)]
    return dict_region
"""


def type_verify(coordinates):
    coord_normal = {'latitude': [-54.777426, -46.603598], 'longitude': [-34.016466, -26.155681]}
    coord_espec = [{'latitude': [-46.361899, -34.276938], 'longitude': [-15.411580, -2.196998]},
                   {'latitude': [-52.997614, -44.428305], 'longitude': [-23.966413, -19.766959]}]
    type_dict = {'normal': [False, False], 'especial': [False, False]}
    i = 0
    for coord in coordinates:
        if coord_normal[coord][0] <= float(coordinates[coord]) <= coord_normal[coord][1]:
            type_dict['normal'][i] = True
            i += 1
    i = 0
    if type_dict['normal'][0] is False or type_dict['normal'][1] is False:
        for j in range(len(coord_espec)):
            for coord in coordinates:
                if not coord_espec[j][coord][0] <= float(coordinates[coord]) <= coord_espec[j][coord][1]:
                    continue
                else:
                    type_dict['especial'][i] = True
                    if type_dict['especial'][0] and type_dict['especial'][1] is False:
                        i += 1
            if [True, True] == type_dict['especial']:
                break
            else:
                type_dict['especial'] = [False, False]
                    
    for typ in type_dict:
        if [True, True] == type_dict[typ]:
            return typ
    return "laborious"


def change_numbers(number):
    num = [x for x in number if x in '0123456789']
    return "+55"+"".join(num)


def change_data_json(response):
    for user in response:
        user['type'] = type_verify(user["location"]["coordinates"])
        user['location']['region'] = dict_regions[user['location']['state']]
        user['gender'] = user['gender'][0]
        number = user.pop("phone")
        user['telephoneNumbers'] = [change_numbers(number)]
        number = user.pop('cell')
        user["mobileNumbers"] = [change_numbers(number)]
        date = user.pop('dob')
        user["birthday"] = date["date"]
        user["nationality"] = "BR"
        user['registered'] = user['registered']['date']


def transform_csv(response):
    
    for user in response:
        new_data = {
                    "type": type_verify({'latitude': user['location__coordinates__latitude'],
                                         'longitude': user['location__coordinates__longitude']}),
                    "gender": 'f' if 'female' in user.values() else 'm',
                    "name": {
                            "title": user['name__title'],
                            "first": user['name__first'],
                            "last": user['name__last']
                        },
                    "location": {
                            "region": dict_regions[user['location__state']],
                            "street": user['location__street'],
                            "city": user['location__city'],
                            "state": user['location__state'],
                            "postcode": user['location__postcode'],
                            "coordinates": {
                                    "latitude": user['location__coordinates__latitude'],
                                    "longitude": user['location__coordinates__longitude']
                                         },
                            "timezone": {
                                    "offset": user['location__timezone__offset'],
                                    "description": user['location__timezone__description']
                                        }
                                },
                    "email": user['email'],
                    "birthday": user['dob__date'],
                    "registered": user['registered__date'],
                    "telephoneNumbers": [change_numbers(user['phone'])],
                    "mobileNumbers": [change_numbers(user['cell'])],
                    "picture": {
                            "large": user['picture__large'],
                            "medium": user['picture__medium'],
                            "thumbnail": user['picture__thumbnail']
                            },
                    "nationality": "BR"
                }
        users_json["results"].append(new_data)


change_data_json(users_json["results"])
transform_csv(users_csv)


with open("data.json", 'w', encoding='utf8') as json_file:
    json.dump(users_json, json_file, ensure_ascii=False)
