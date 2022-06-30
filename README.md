
# Documentation for Cogent-Labs-Assignment

## Submission Deatils 
Applicant Name: Jiaming Nie
Applicant E-mail: jiaming.nie13@gmail.com 

## Introduction to the Assignment

The image conversion to thumbnail service is written in Python and Flask. Project structure is on the following:

* `imag_convert_service.py` -- The service implemented in Flask using Python 
* `unit_test.py` -- Unit test for the application usingh PyTest 
* `config.yaml` -- Basic configurations for the service, here the host, port and the resolution of the thumbnail can be defined here.
* `Dockerfile` -- A Docker file for building and running the service 
* `Makefile` -- A make file creates the binary executable file 
* `requirements.txt` -- dependencies for this project, using `pip install -r requirements.txt`

## API Usage 

| API Path(Name)       | API Method | Argument | API Description | 
| ---                  | ---        | ---      | ---             |
| /api/convertImage    | POST       | Image file path.       | Upload Image file to the app, then return a thumbnail image with 100px \times 100px  | 

This API doesn't have authentication part and the method is `POST`.

### Using Postman
In the Postman, after typing the address, then in the body part, add one field with `image` then select the image file from local directory. Then click Send button, the result will return.

![Postman Screenshot](/images/postman.png) 

### CURL Command 

Use the `curl` command on the following also helps (Note: the path of the image is relative path):

```
curl --location --request POST 'http://localhost:8080/api/convertImage' \
--form 'image=@"./images/seattle.jpeg"'
```

### Python Requests

Alternatively, you can use the following `python` syntax for making the request:

```
import requests
url = "http://localhost:8080/api/convertImage"
payload={}
files=[
  ('image',('seattle.jpeg',open('/images/seattle.jpeg','rb'),'image/jpeg'))
]
headers = {}
response = requests.request("POST", url, headers=headers, data=payload, files=files)
print(response.text)
```

## How to run the service 
Here provides 3 ways to run the service, using docker command, makefile and running in local environment.

### Running in Docker 

`Dockerfile` includes the basic configurations packaging the service. (Make sure docker is installed.)

* `docker image build -t app .`
* `docker run -p 5000:5000 -d app`

### Using Makefile 

Makefile will build the binary executable file for the service.

* `make` in command line
* `/bin/image_service_app` run the binary executable file 

### Local Debugging 

* Create the virtual environment: `python3 -m venv virtualenv`
* Activate the virtualenv: source `virtualenv/bin/activate`
* Install the prerequisites: `pip install -r requirements.txt`
* It provides the following methods to run the service:
  * `python image_convert_service.py path_config_file` It will read configurations including host address, port and resolution.
  * `python image_convert_service.py` All the configurations will be 

## Unit Test of the code 
`pytest` is the library used for unit testing. In local debugging mode, after installing the prerequisites using `pip install -r requirements.txt`, then in the command line, typr `pytest`, tehn the unit testing will be performed. 
