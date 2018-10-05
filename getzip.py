import zipfile

import requests
import io


def getzip(url):
    r = requests.get(url)
    return r.content


if __name__ == '__main__':
    URLS = {
        'national': 'https://www.bls.gov/oes/special.requests/oesm17nat.zip',
        'state': 'https://www.bls.gov/oes/special.requests/oesm17st.zip',
        'area': 'https://www.bls.gov/oes/special.requests/oesm17ma.zip',
        'industry': ''
        }
    r = requests.get(URLS['state'])
    z = zipfile.ZipFile(io.BytesIO(r.content))
