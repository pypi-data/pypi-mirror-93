""" ---- PYNETMODULE ----
	Version: 1.0 31.01.21
	Author: Danila Kisluk
	(vk.com/kislukdanila)
	---------------------
"""

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


from http.client import HTTPConnection
from http.client import HTTPSConnection


def UrlParser(url):
	""" System function """

	if url[:7] == "http://":
		protocol = "http"
		url = url[7:]

	elif url[:8] == "https://":
		protocol = "https"
		url = url[8:]

	else:
		protocol = "https"

	if "/" in url:
		domain = url[:url.find("/")]
		urlway = url.replace(domain, "")

	else:
		domain = url
		urlway = "/"

	return protocol, domain, urlway


def NetRequest(url, method = "GET", data = "", headers = {}):
	""" ----------- USAGE EXAMPLES -----------
		import:
		>>> from pynetmodule import NetRequest

		using get request:
		>>> NetRequest("some_url")

		using put request:
		>>> NetRequest("some_url",
				       method = "PUT",
				       data = "something")

		using post request:
		>>> NetRequest("some_url",
				   	   method = "POST",
				       data = "something",
				       headers = "something")
		--------------------------------------
	"""

	if method not in ["GET", "PUT", "POST"]:
		method = "GET"

	protocol, domain, urlway = UrlParser(url)

	if protocol == "https":
		server = HTTPSConnection(domain)

	else:
		server = HTTPConnection(domain)

	server.request(method, urlway, data, headers)
	response = server.getresponse()
	response = response.read()
	response = response.decode()

	return response
