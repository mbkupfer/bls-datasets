import io

import requests
import pandas as pd

def _get_area_url(**kwargs):
    '''Get url for QCEW data by area.

    Parameters
    ----------
    year : string
        'YYYY'
    qtr : string
        Use `a` for annual averages.
    area : string
        For all area codes and titles see:
        http://www.bls.gov/cew/doc/titles/area/area_titles.htm.

    Returns
    -------
    string
        URL that will be used for main function.

    '''

    for arg in ['year', 'qtr', 'area']:
        if arg not in kwargs:
            raise ValueError('Must specify {}'.format(arg))

    url = 'http://data.bls.gov/cew/data/api/[YEAR]/[QTR]/area/[AREA].csv'
    url = url.replace('[YEAR]', kwargs.get('year'))
    url = url.replace('[QTR]', kwargs.get('qtr').lower())
    url = url.replace('[AREA]', kwargs.get('area').upper())
    return url

def _get_industry_url(**kwargs):
    '''Get url for QCEW data by industry.

    Parameters
    ----------
    year : string
        'YYYY'
    qtr : string
        Use `a` for annual averages.
    industry : string
        For all industry codes and titles see:
        http://www.bls.gov/cew/doc/titles/industry/industry_titles.htm

    Returns
    -------
    string
        URL that will be used for main function.

    '''

    for arg in ['year', 'qtr', 'industry']:
        if arg not in kwargs:
            raise ValueError('Must specify {}'.format(arg))

    url = 'http://data.bls.gov/cew/data/api/[YEAR]/[QTR]/industry/[IND].csv'
    url = url.replace('[YEAR]', kwargs.get('year'))
    url = url.replace('[QTR]', kwargs.get('qtr').lower())
    url = url.replace('[IND]', kwargs.get('industry'))
    return url


def _get_size_url(**kwargs):
    '''Get url for QCEW data by size.

    Note that size data is only available for the first quarter of each year
    Parameters
    ----------
    year : string
        'YYY'.
    size : string
        For all establishment size classes and titles see:
        http://www.bls.gov/cew/doc/titles/size/size_titles.htm

    Returns
    -------
    string
        URL that will be used for main function.

    '''

    for arg in ['year', 'size']:
        if arg not in kwargs:
            raise ValueError('Must specify {}'.format(arg))

    url = 'http://data.bls.gov/cew/data/api/[YEAR]/1/size/[SIZE].csv'
    url = url.replace('[YEAR]', kwargs.get('year'))
    url = url.replace('[SIZE]', kwargs.get('size'))
    return url

def get_data(cut_by, rtype='dataframe', **kwargs):
    """Get a dataset from the Quarterly Census of Employment and Wages (QCEW)

    Parameters
    ----------
    cut_by : str
        Specify QCEW data cut/sliced. Occupations can be cut/sliced by industry,
        area, and size class
    rtype : str
        Default behavior is to return a pandas dataframe.
        If you want a primitive i/o csv file, then specify rtype='csv'.
    **kwargs :
        Allows `get_data()` to act as a wrapper funciton.
        Arguments vary by how the data is being cut/sliced

        Required argument by data cut/slice

        Area: year, qtr, area
            For all area codes and titles see:
            http://www.bls.gov/cew/doc/titles/area/area_titles.htm.
        Industry: year, qtr, industry
            For all industry codes and titles see:
            http://www.bls.gov/cew/doc/titles/industry/industry_titles.htm
        Size: year, size
            For all establishment size classes and titles see:
            http://www.bls.gov/cew/doc/titles/size/size_titles.htm


    Returns
    -------
    pandas.Dataframe, or csv file

    """

    for k, v in kwargs.items():
        if not isinstance(v, str):
            raise ValueError('{} must be a str. Instead got {}'
                .format(k, type(v)))

    method = '_get_{}_url'.format(cut_by)
    url = eval(method)(**kwargs)

    try:
        r = requests.get(url)
        if r.ok:
            pass
        else:
            raise requests.exceptions.HTTPError('Not a valid request.'
                'Double check for valid parameters.')
    except requests.exceptions.ConnectionError as e:
        print(e, '\nFailed to establish a new connection. Check internet.')

    if rtype == 'dataframe':
        return pd.read_csv(io.BytesIO(r.content), low_memory=False)
    elif rtype == 'csv':
        return io.BytesIO(r.content)
    else:
        raise ValueError('{} is not a valid return type\n' \
            'valid return types are `dataframe` or `io`' \
            .format(rtype))
