import zipfile
import io

import requests

def _get_zip(url):
    """Retrieve zipfile using http request.

    zipfiles

    Parameters
    ----------
    url : type
        Description of parameter `url`.

    Returns
    -------
    zipfile.ZipFile

    Usage:

    >>> zip = _get_zip('https://www.bls.gov/oes/special.requests/oesm17nat.zip')
    >>> type(zip)
    <class 'zipfile.ZipFile'>

    >>> for file in zip.filelist:
    ...     print(file.filename)
    ...
    oesm17nat/field_descriptions.xlsx
    oesm17nat/national_M2017_dl.xlsx

    # accessing zipfile obects for i/o operations

    >>> fp = zip.open('oesm17nat/field_descriptions.xlsx', 'r')
    >>> fp.readable()
    True

    fp.close()

    """
    try:
        r = requests.get(url)
        if r.ok:
            return zipfile.ZipFile(io.BytesIO(r.content))
        else:
            raise requests.exceptions.HTTPError('Not a valid request.'
                'Double check for valid parameters.')
    except requests.exceptions.ConnectionError as e:
        print(e, '\nFailed to establish a new connection. Check internet.')

def get_file(url, filename):
    try:
        zip = _get_zip(url)
        fp = zip.open(filename, 'r')
        return fp
    except Exception as e:
        print(e)
