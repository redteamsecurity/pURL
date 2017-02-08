import requests
import sys
import getopt


def usage():
    print "usage: pURL.py -u <url> -m <request method> -x X-API-KEY: 1234 -d <request body>"
    print ""
    print "-h or --help                               - display this usage information"
    print '-d "username=test&password=passwd"         - the data expected to be sent w/ the request'
    print '-f file.txt                                - the input file where each API request is stored'
    print "-m GET, POST, PUT...etc                    - the method used to connect to to the url"
    print "-p or --proxy host:port                    - pass through burp or any other proxy"
    print '-u or --url "https://api.endpoint.com"     - connect to the api endpoint specified'
    print '--unsafe                                   - turn off HTTPS cert checks'
    print '-v                                         - give verbose output for each request'
    print "-x header_name:value                       - insert a request header that may be needed"
    sys.exit()


def setProxy(proxy):
    proxyDict = {}
    # set the proxy location based on user input
    proxyDict['http'] = proxy
    proxyDict['https'] = proxy
    proxyDict['ftp'] = proxy
    return proxyDict


def configHeader(headerInfo):
    header_dict = {}
    # use this method to append multiple headers to the request.
    headerInfo = headerInfo.strip()
    head, value = headerInfo.split(":")
    header_dict[head] = value
    return header_dict


def assembleRequest(data, method, URL, safe, headerDict, proxyDict, verbose):


    # connect to the API endpoint, and send the data that was given
    # note the response variable will hold all of the information received back from the server
    try:
        if method == "GET":
            response = requests.get(URL, data, headers=headerDict,proxies=proxyDict, verify=safe)
        elif method == "POST":
            response = requests.post(URL, data, headers=headerDict, verify=safe, proxies=proxyDict)
        elif method == "PUT":
            response = requests.put(URL, data, headers=headerDict, verify=safe, proxies=proxyDict)
        elif method == "DELETE":
            response = requests.delete(URL, headers=headerDict, verify=safe, proxies=proxyDict)
        elif method == "OPTIONS":
            response = requests.options(URL, verify=safe, proxies=proxyDict)
        elif method == "HEAD":
            response = requests.head(URL, verify=safe, proxies=proxyDict)

        else:
            print "method not currently supported"
            print "current methods: GET, POST, PUT, DELETE, OPTIONS, HEAD"
            sys.exit()

        print ""
        # print response code (i.e. 404, 500, 200)
        print response.status_code
        if verbose:
            # response headers are saved as a dictionary. Loop through the dictionary and print information.
            for i in response.headers:
                print i + ":", response.headers[i]
            print ""
            # output response body
            print response.content
        else:
            pass
        print ""
        print ""

    except requests.exceptions.Timeout:
        print "Connection timeout - make sure a WAF or firewall rule is not blocking traffic."
    except requests.exceptions.TooManyRedirects:
        print "Too many redirects - URL may be bad"
    except requests.exceptions.SSLError:
        print "could not verify HTTPS certificate."
        print 'pURL tries to verify HTTPS certificates. If using a proxy try "--unsafe"'
    except requests.exceptions.RequestException as e:
        print e
    except Exception, e:
        print "catastrophic failure see below for details"
        print e
        sys.exit(1)


def parseFile(infile, safe, verbose):
    # open the file to read contents
    infile = open(infile)
    # loop through each line of the file, read values
    for line in infile:
        data = line.split("\t")
        # this will take the input values and start assigning to the different pieces of the request
        parseInput(data, safe, verbose)
    infile.close()


def parseInput(request, safe, verbose):
    URL = ""
    data = ""
    method = ""
    headerDict = {}

    # walk through the request and assign each piece of information to a variable
    i = 0
    try:
        if request != ['\n']:
            while i < len(request):
                method = request[i]
                i += 1
                URL = request[i]
                i += 1
                data = request[i]
                i += 1
                # loop until there are no more headers to add
                while i < len(request):
                    head, value = request[i].split(":")
                    headerDict[head] = value.strip('\n')
                    i += 1
                assembleRequest(data, method, URL, safe, headerDict, proxyDict, verbose)
        else:
            pass
    except:
        print "Something went wrong while making the request. Please review the input file for any errors"


if __name__=="__main__":
    URL = ""
    data = ""
    method = ""
    header = ""
    proxyDict = {}
    headerDict = {}
    safe = True
    verbose = False
    infile = ""

    if not len(sys.argv[1:]):
        print "no options specified"
        usage()

    try:
        # read expected user input, throw an error if unknown options are set.
        opts, args = getopt.getopt(sys.argv[1:], "h:x:d:f:u:m:p:v", ["help", "proxy=", "unsafe", "url="])

        # set all user input to variables
        for o,a in opts:
            if o in ("-d"):
                data = a
            elif o in ("-f"):
                infile = a
            elif o in ("-u","--url"):
                URL = a
            elif o in ("-m"):
                method = a
            elif o in ("-x"):
                headerDict = configHeader(a)
            elif o in ("-h","--help"):
                usage()
                sys.exit()
            elif o in ("-p","--proxy"):
               proxyDict = setProxy(a)
            elif o in ("--unsafe"):
                safe = False
            elif o in ("-v"):
                verbose = True
            else:
                assert False, "Unexpected input"
    except getopt.GetoptError as e:
        print "one of the options isn't quite right"
        print e
        usage()
        sys.exit(2)

    # This will assemble all variables to submit the requests.
    if infile != "":
        parseFile(infile, safe, verbose)
    else:
        assembleRequest(data, method, safe, headerDict, proxyDict, verbose)

# main()