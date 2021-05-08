import os
import tempfile

import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_hello(client):
    """Prints Hello World"""

    rv = client.get("/")
    assert b"Hello, World" in rv.data


def test_security_vulnerabilities(client):
	resp_get = client.get("/package/health/dummy/0.8")
	assert 200 == resp_get.status_code
	assert "MIT" == resp_get.get_json(force=True).get("license")

def test_security_vulnerabilities(client):
	resp_get = client.get("/package/health/dummy/0.4")
	assert 200 == resp_get.status_code
	assert None == resp_get.get_json(force=True).get("releases")


def test_invalid_request(client):
	resp_get = client.get("/package/health/")
	assert 404 == resp_get.status_code

def test_package_info(client):
	resp_get = client.get("/package/releases/tiny-tarball")
	assert 200 == resp_get.status_code
	assert "1.0.0" == resp_get.get_json(force=True).get("latest")

def test_package_info(client):
	resp_get = client.get("/package/releases/test")
	assert 200 == resp_get.status_code
	assert "0.6.0" == resp_get.get_json(force=True).get("latest")
