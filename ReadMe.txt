This script was build to help automate REST API calls, which currently have no standard format for documentation. Using the formatting in the example document provided, the basic information required for REST API calls can be gathered from the developer and built into a request. Using the proxy functionality will allow for requests to be intercepted and manipulated by tools like Burp or ZAP. This application will function similar to cURL, but has the -f option to read multiple requests from a file. For tools like Burp this will help put each of the requests into the proxy history and targets tab; allowing for less back and forth when building requests into the repeater and performing active/passive scanning. Below are some quick specifications for using the -f option:

1) this tool was build with using a text file in mind
2) 1 request per line in the text document. The tool parses each request based on \n.
3) the format of the document should be: method url data headers
	Note: some APIs require multiple headers (i.e. content-type, x-api-key, etc.), simply place them all at the end of the line, and the tool will append them all to the request.

FAQ:
Python is throwing an error "No module named requests," How can I fix this?
	A: you need to install the requests library. Below is the URL where it can be found. once downloaded run "python setup.py install"
	https://github.com/kennethreitz/requests/

