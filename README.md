# Customers handler



This project will make requests to two endpoints.
Will work with a json and a csv endpoint.

CSV example:

```
gender,name.title,name.first,name.last,location.street,location.city,location.state,location.postcode,location.coordinates.latitude,location.coordinates.longitude,location.timezone.offset,location.timezone.description,email,dob.date,dob.age,registered.date,registered.age,phone,cell,picture.large,picture.medium,picture.thumbnail
male,mr,joselino,alves,2095 rua espirito santo ,são josé de ribamar,paraná,96895,-35.8687,-131.8801,-10:00,Hawaii,joselino.alves@example.com,1996-01-09T02:53:34Z,22,2014-02-09T19:19:32Z,4,(97) 0412-1519,(94) 6270-3362,https://randomuser.me/api/portraits/men/75.jpg,https://randomuser.me/api/portraits/med/men/75.jpg,https://randomuser.me/api/portraits/thumb/men/75.jpg
```
JSON example:

```
{"gender":"male","name":{"title":"mr","first":"antonelo","last":"da conceição"},"location":{"street":"8986 rua rui barbosa ","city":"santo andré","state":"alagoas","postcode":40751,"coordinates":{"latitude":"-69.8704","longitude":"-165.9545"},"timezone":{"offset":"+1:00","description":"Brussels, Copenhagen, Madrid, Paris"}},"email":"antonelo.daconceição@example.com","dob":{"date":"1956-02-12T10:38:37Z","age":62},"registered":{"date":"2005-12-05T15:22:53Z","age":13},"phone":"(85) 8747-8125","cell":"(87) 2414-0993","picture":{"large":"https://randomuser.me/api/portraits/men/8.jpg","medium":"https://randomuser.me/api/portraits/med/men/8.jpg","thumbnail":"https://randomuser.me/api/portraits/thumb/men/8.jpg"}}
```

### Changes that must be deployed

There are customers in the **5 country regions**: 

- Norte
- Nordeste
- Centro-Oeste
- Sudeste
- Sul

Customers are classified with the following tags:

- **ESPECIAL**

```
minlon: -2.196998
minlat -46.361899
maxlon: -15.411580
maxlat: -34.276938
```
```
minlon: -19.766959
minlat -52.997614
maxlon: -23.966413
maxlat: -44.428305
```

- **NORMAL**

```
minlon: -26.155681
minlat -54.777426
maxlon: -34.016466
maxlat: -46.603598
```

- **Laborious:** Any other user that doesn't fit on the preivous rules.

Other improvements that must be present:


1. Transform telephone contacts in the format [E.164](https://en.wikipedia.org/wiki/E.164). Example: (86) 8370-9831 becomes +558683709831.
2. Insert the nationality. As all customers are still from Brazil, the default value will be BR.
3. Change the value of the `gender` field to `F` or `M` instead of `female` or `male`.
4. Remove the `age` field from `dob` and `registered`.
5. Change structure to simplify reading and use arrays in specific fields (see example below)

OUTPUT Example:

```
{
  "type": "laborious"
  "gender": "m",
  "name": {
    "title": "mr",
    "first": "quirilo",
    "last": "nascimento"
  },
  "location": {
    "region": "sul"
    "street": "680 rua treze ",
    "city": "varginha",
    "state": "paraná",
    "postcode": 37260,
    "coordinates": {
      "latitude": "-46.9519",
      "longitude": "-57.4496"
    },
    "timezone": {
      "offset": "+8:00",
      "description": "Beijing, Perth, Singapore, Hong Kong"
    }
  },
  "email": "quirilo.nascimento@example.com",
  "birthday": "1979-01-22T03:35:31Z",
  "registered": "2005-07-01T13:52:48Z",
  "telephoneNumbers": [
    "+556629637520"
  ],
  "mobileNumbers": [
    "+553270684089"
  ],
  "picture": {
    "large": "https://randomuser.me/api/portraits/men/83.jpg",
    "medium": "https://randomuser.me/api/portraits/med/men/83.jpg",
    "thumbnail": "https://randomuser.me/api/portraits/thumb/men/83.jpg"
  },
  "nationality": "BR"
}

```

## API

Think of an API that given the **user's region** and its **type of rating**, responds to the **listing of eligible**. There is no routing defined for the application, it's up to you.

It is **mandatory** to work with all data manipulation **in memory**. The loading of the input data must be via HTTP request **when uploading your application**, that is, before your App is `ready`, you will make a request for the links provided below.

In addition to the list of eligible users, to allow navigation between records, **the following paging metadata must be implemented**:
```
  {
    pageNumber: X,
    pageSize: P,
    totalCount: T,
    users: [
      ...
    ]
  }
```

Links for requests:

- https://storage.googleapis.com/juntossomosmais-code-challenge/input-backend.csv
- https://storage.googleapis.com/juntossomosmais-code-challenge/input-backend.json