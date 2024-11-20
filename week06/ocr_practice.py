import requests
import uuid
import time
import json

api_url = 'https://q8aaxtua7s.apigw.ntruss.com/custom/v1/36126/d65e9be2c84264d9ee2964558ed94d9e63381b768b247295d879138276425873/general'
secret_key = ''
image_file = 'test.jpg'

request_json = {
    'images': [
        {
            'format': 'jpg',
            'name': 'demo'
        }
    ],
    'requestId': str(uuid.uuid4()),
    'version': 'V2',
    'timestamp': int(round(time.time() * 1000))
}

payload = {'message': json.dumps(request_json).encode('UTF-8')}
files = [
  ('file', open(image_file,'rb'))
]
headers = {
  'X-OCR-SECRET': secret_key
}

response = requests.request("POST", api_url, headers=headers, data = payload, files = files)

# with open('output.json', 'w', encoding='utf-8') as json_file:
#     json.dump(response.json(), json_file, ensure_ascii=False, indent=4)

# print(response.json())

for i in response.json()['images'][0]['fields']:
    text = i['inferText']
    print(text)
