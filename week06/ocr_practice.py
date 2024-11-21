import requests
import uuid
import time
import json
from io import BytesIO


api_url = 'https://q8aaxtua7s.apigw.ntruss.com/custom/v1/36126/d65e9be2c84264d9ee2964558ed94d9e63381b768b247295d879138276425873/general'
secret_key = ''

medicine_data_list = {"레보트로시럽", "새로딘시럽", "유시락스시럽", "아토크건조시럽", "싱카스트츄정", "삼아리도맥스크림"}


def extraction_medicine(image_data):
    # 이미지 데이터를 BytesIO 객체로 변환
    image_file = BytesIO(image_data)
    
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
        ('file', image_file)  # BytesIO 객체를 파일처럼 사용
    ]
    headers = {
        'X-OCR-SECRET': secret_key
    }

    response = requests.request("POST", api_url, headers=headers, data=payload, files=files)

    # 약품명 추출
    found_medicines = []
    for word_field in response.json()['images'][0]['fields']:
        word = word_field['inferText']
        if word in medicine_data_list:
            found_medicines.append(word)

    return found_medicines
