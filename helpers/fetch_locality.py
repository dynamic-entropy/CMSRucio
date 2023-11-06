import requests
import json
from urllib.parse import urlparse
import os


def parse_host_path_map(urls):
    parsed_urls = [urlparse(url) for url in urls]

    # group by netloc
    # for each netloc, get the list of files

    host_files_map = {}
    for url in parsed_urls:
        hostname = 'https://' + url.netloc
        if hostname not in host_files_map:
            host_files_map[hostname] = []
        host_files_map[hostname].append(url.path)

    return host_files_map


def get_locality(urls):
    host_files_map = parse_host_path_map(urls)

    # do a post request to each hostname with the list of files in the json body
    # to the endpoint /api/v1/archiveinfo
    # with body format {
    # "paths":[
    # "/path/example.txt",
    # "/path/example2.txt"
    # ]
    # }
    # an example curl request would be:
    #     curl -X POST --cert $X509_USER_PROXY --key $X509_USER_PROXY --capath /etc/grid-security/certificates https://xfer-cms.cr.cnaf.infn.it:8443/api/v1/archiveinfo --data '{"paths":["/cmstape/store/test/rucio/store/express/Run2023C/StreamALCAPPSE
    # xpress/ALCARECO/PPSCalMaxTracks-Express-v4/000/367/880/00000/0d829297-280c-403e-ac5b-edfade7446b7.root"]}'
    # request should contain authentication too

    for hostname, files in host_files_map.items():
        # print(hostname, files)
        # print(json.dumps({"paths": files}))
        response = requests.post(hostname + '/api/v1/archiveinfo',
                                 data=json.dumps({"paths": files}),
                                 verify='/etc/grid-security/certificates',
                                 cert=(os.environ['X509_USER_PROXY'], os.environ['X509_USER_PROXY']),
                                 headers={'Content-Type': 'application/json'},
                                 timeout=180
                                 )
        print(response.text)


if __name__ == "__main__":
    urls = ["davs://eoscms.cern.ch:443/eos/cms/store/express/Run2023C/StreamALCAPPSExpress/ALCARECO/PPSCalMaxTracks-Express-v4/000/367/880/00000/0d829297-280c-403e-ac5b-edfade7446b7.root",
            "davs://xfer-cms.cr.cnaf.infn.it:8443/cmstape/store/test/rucio/store/express/Run2023C/StreamALCAPPSExpress/ALCARECO/PPSCalMaxTracks-Express-v4/000/367/880/00000/0d829297-280c-403e-ac5b-edfade7446b7.root"]

    get_locality(urls)
