import csv
from datetime import datetime as dt
from datetime import timedelta as td
from flask import Flask, jsonify
import requests

class MetadataHelper:

	def __init__(self):
		self.licenses = self.populate_licenses()
		self.vulnerabilities = self.populate_vulnerabilities()

	def populate_licenses(self):
		licenses = {}
		with open('licenses.csv') as licenses_csv:
			csv_reader = csv.reader(licenses_csv, delimiter=',')
			line_count = 0 
			for row in csv_reader:
				package = row[0]
				license = row[1]
				licenses[package] = license
		return licenses


	def populate_vulnerabilities(self):
		vulnerabilities = {}
		
		with open('vulnerabilities.csv') as vulnerabilities_csv:
			csv_reader = csv.reader(vulnerabilities_csv, delimiter=',')
			line_count = 0 
			for row in csv_reader:
				info = []
				info.append(row[0])
				info.append(row[2])
				info.append(row[3])
				info.append(dt.fromtimestamp(int(row[4])))
				package = row[1]

				if package in vulnerabilities:
					vulnerabilities[package].append(info)
				else:
					vulnerabilities[package] = [info]
		
		return vulnerabilities


	def return_security_vulnerabilities(self, package, version):
		if package in self.licenses:
			license = self.licenses[package]
			vulnerabilities_info = []

			for data in self.vulnerabilities[package]:
				info = {}
				if data[1] == version:
					info['id'] = data[0]
					info['description'] = data[2]
					info['created'] = data[3].strftime("%Y-%m-%dT%H:%M:%SZ")
					vulnerabilities_info.append(info)

			return jsonify({"name": package, "version": version, "license": license, "vulnerabilities": vulnerabilities_info})
		
		else:
			response = jsonify("Package and license not found.")
			response.status_code = 404
			return response 



	def return_package_info(self, package):
		if package is not None:
			url = 'https://registry.npmjs.org/' + package
			resp = requests.get(url)
			if resp is not None:
				return self.parse_package_info(resp.json(), package)
			
		else:
			response = jsonify("Invalid package name received.")
			response.status_code = 406
			return response 

	def parse_package_info(self, json, package):
		versions = json['versions']
		times = json['time']
		times_versions = {}
		releases = []
		for v in versions:
			# Only include active versions
			if ('deprecated' in versions[v]):
				continue
			else:
				releases.append(v)

		# Creating a dict of dates : version number to guarantee I'm returning the latest version
		for k in times:
			if k not in ['created', 'modified']:
				date = dt.strptime(times[k], "%Y-%m-%dT%H:%M:%S.%fZ")
				times_versions[date] = k
		
		max_time = max(times_versions, key=times_versions.get)	
		response = jsonify({"name":package, "latest":times_versions[max_time], "releases":releases})
		response.status_code = 200
		return response


