'''Unit test using PyTest'''
from urllib import response
from xmlrpc.client import ResponseError
import yaml 
from PIL import Image
from image_convert_service import ConvertImageToThumnail
import io 

img_thumbnail_service = ConvertImageToThumnail(config_file="./config.yaml")
test_img = Image.open("./images/seattle.jpeg")

def load_config(config_file="./config.yaml"):
    with open(config_file, 'r') as f:
        doc = yaml.safe_load(f)

    deployment_info = doc['deployment']
    host = deployment_info['host']
    port = int(deployment_info['port'])
    api_url = deployment_info['api_url']
    return (host, port, api_url)

def test_basic_config():
    host, port, api_url = load_config()
    assert host == img_thumbnail_service.host
    assert port == img_thumbnail_service.port
    assert api_url == img_thumbnail_service.api_url

def test_convert_img_to_array():
    img_byte_arr = img_thumbnail_service.convert_img_to_array(test_img)
    assert isinstance(img_byte_arr, bytes)

def test_img_service():
    service_app = img_thumbnail_service.app
    api_url = load_config()[2]
    with service_app.test_client() as test_client:
        # Test 404 Page 
        response = test_client.post('/')
        assert response.status_code == 404
        assert response.status == "404 NOT FOUND"

        # Test API 
        response = test_client.get(api_url)
        assert response.status_code == 405
        assert response.status == "405 METHOD NOT ALLOWED"

        response = test_client.post("/api/convertImage")
        assert response.status_code == 503
        assert response.status == "503 SERVICE UNAVAILABLE"

        data = {"image":open('./images/seattle.jpeg','rb')}
        response = test_client.post("/api/convertImage",data=data)
        assert response.status_code == 200

