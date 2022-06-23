from flask_classful import FlaskView
from flask import Flask, Response, send_file, request
import logging
import yaml, json, io
from PIL import Image
import sys
from waitress import serve
import threading
from werkzeug.utils import secure_filename
JSON_CONTENT_TYPE = "application/json"

class ConvertImageToThumnail(FlaskView):
    def __init__(self, host="http://127.0.0.1", port=8080, api_url="/api/convertImage", resolution=100, config_file=None):
        self.host = host
        self.port = int(port) 
        self.api_url = api_url
        self.config_file = config_file
        self.resolution = resolution
        self.logger = logging.getLogger()
        self.__load_configurations_from_config(self.config_file)
        self.app = Flask("Image Conversion Service")

        self.app.add_url_rule(self.api_url, methods=['POST'], view_func=self.convert_image_index)

    def __load_configurations_from_config(self, config_file):
        try:
            if config_file is not None:
                with open(config_file, 'r') as f:
                    doc = yaml.safe_load(f)

                deployment_info = doc['deployment']
                self.host = deployment_info['host']
                self.port = int(deployment_info['port'])
                self.api_url = deployment_info['api_url']

                other_config = doc['otherConfig']            
                self.resolution = other_config['resolution']

        except Exception as ex:
            self.logger.error("Read configurations from file met error %s" % str(ex))
    
    def convert_image_index(self):
        try:
            raw_image = request.files["image"] 
            file_name = secure_filename(raw_image.filename).split('.')[0]
            if not raw_image:
                msg_data = {"message" : "No image file is specified. Please upload valid image file."}
                status_code = 503
            else:
                raw_image_byte = raw_image.read()
                thumbnail_img = self.resize_image(raw_image_byte)
                return send_file(io.BytesIO(thumbnail_img), mimetype='image/jpeg',as_attachment=True, download_name='%s.thumbnails' % file_name)


        except Exception as ex:
            self.logger.debug("Server met error when receiving the image: %s" % str(ex))
            status_code = 503
            msg_data = {"message" : "Server met error: %s" % str(ex)}
            return Response(response=json.dumps(msg_data),  status=status_code, mimetype=JSON_CONTENT_TYPE)

    def resize_image(self, image_byte):
        try:
            img_obj = Image.open(io.BytesIO(image_byte))
            img_obj.thumbnail((self.resolution, self.resolution))
            img_byte_arr = self.convert_img_to_array(img_obj)
            return img_byte_arr

        except Exception as ex:
            self.logger.debug("Conversion of image met error: %s " % str(ex))
            return None 

    def convert_img_to_array(self, img_obj):
        img_byte_arr = io.BytesIO()
        img_obj.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        return img_byte_arr

    def page_not_found(self, error=None):
        self.logger.info("The API Endpoint Not Found on the server.")
        data = {"Message" : "API Endpoint Found on the Server"}
        status_code = 404
        return Response(response=json.dumps(data),  status=status_code, mimetype=JSON_CONTENT_TYPE)

    def register_not_found_handler(self):
        self.app.register_error_handler(404, self.page_not_found)

    def deploy_app_in_production(self):
        serve(self.app, host=self.host, port=self.port)
        
    def start_server(self):
        self.logger.info("Start The Image Conversion Service")
        server_thread = threading.Thread(target=self.deploy_app_in_production)
        server_thread.start()

    def run_app(self):
        self.app.run(host=self.host, port=self.port, debug=True)

if __name__ == '__main__':
    argv_par = sys.argv
    if len(argv_par) == 2:
        config_file = argv_par[1]
        server = ConvertImageToThumnail(config_file=config_file)
        server.run_app()
    else:
        server = ConvertImageToThumnail()
        server.run_app()

