# import http.client, urllib.request, urllib.parse, urllib.error, base64

# headers = {
#     # Request headers
#     'Content-Type': 'application/json',
#     'Ocp-Apim-Subscription-Key': 'cae01e753c8c4867bf6edb25db9348e1',
# }

# params = urllib.parse.urlencode({
#     "contentContainerUrl":"https://divyapattisapu.blob.core.windows.net/audiofiles?sp=rl&st=2021-05-29T14:05:45Z&se=2021-05-29T22:05:45Z&sv=2020-02-10&sr=c&sig=aQjurwTjP6D%2BdUgDwiVFS3u1j56RDV7KktJs6ZsVwz0%3D"
# })

# try:
#     conn = http.client.HTTPSConnection('centralindia.api.cognitive.microsoft.com')
#     conn.request("POST", "/speechtotext/v3.0/transcriptions?%s" % params, "{body}", headers)
#     response = conn.getresponse()
#     data = response.read()
#     print(data)
#     conn.close()
# except Exception as e:
#     print("[Errno {0}] {1}".format(e.errno, e.strerror))


import http.client, urllib.request, urllib.parse, urllib.error, base64


headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'cae01e753c8c4867bf6edb25db9348e1',
}

# params = urllib.parse.urlencode({
#     # Request parameters
#     'skip': '{integer}',
#     'top': '{integer}',
# })

try:
    conn = http.client.HTTPSConnection('centralindia.api.cognitive.microsoft.com')
    conn.request("GET", "/speechtotext/v3.0/transcriptions", "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    # for i in data.keys:
    #     print(data.get(i))
    #     # print('\n')
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))