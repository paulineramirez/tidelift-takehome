from flask import Flask, request
from helper import MetadataHelper

app = Flask(__name__)

helper = MetadataHelper()
@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/package/health/<package_name>/<version>", methods=['GET'])
def return_vulnerabilities(package_name, version):
	if request.method == 'GET':
		return helper.return_security_vulnerabilities(package_name, version)
		
	else:
		return "Invalid request received", 400

@app.route("/package/releases/<package_name>", methods=['GET'])
def return_packages(package_name):
	if request.method == 'GET':
		print(package_name)
		return helper.return_package_info(package_name)
	else:
		return "Invalid request received", 400
