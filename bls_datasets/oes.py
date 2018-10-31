import datetime

import pandas as pd

from . import util

# Previous year OES gets released in May
if datetime.date.today().month > 6:
    CUR_YEAR = datetime.date.today().year - 1
else:
    CUR_YEAR = datetime.date.today().year - 2

def _get_zip_urls(year):
    """Return urls for zip files based on pattern.

    Parameters
    ----------
    year : string
        4 digit year in string format 'YYYY'.

    Returns
    -------
    dict
    """

    suffix = f'oesm{year[2:]}'
    code = 4

    return {
        'national': f'https://www.bls.gov/oes/special.requests/{suffix}'
            'nat.zip',
        'state': f'https://www.bls.gov/oes/special.requests/{suffix}'
            'st.zip',
        'area': f'https://www.bls.gov/oes/special.requests/{suffix}ma.zip',
        'industry': f'https://www.bls.gov/oes/special.requests/{suffix}in'
            f'{code}.zip'}

def _get_filenames(year, industry_scope=None):
    """Return filenames for oes files based on pattern.

    Parameters
    ----------
    year : string
        4 digit year in string format 'YYYY'.

    Returns
    -------
    dict.

    """
    if industry_scope == None:
        prefix = 'natsector'
    elif (industry_scope == 5) or (industry_scope == 6):
        prefix = 'nat5d_6d'
    else:
        prefix = 'nat{}d'.format(industry_scope)

    return {
        'national': f'oesm{year[2:]}nat/national_M{year}_dl.xlsx',
        'state': f'oesm{year[2:]}st/state_M{year}_dl.xlsx',
        'metros': f'oesm{year[2:]}ma/MSA_M{year}_dl.xlsx',
        'metros-divisions': f'oesm{year[2:]}ma/aMSA_M{year}_dl.xlsx' ,
        'non-metros': f'oesm{year[2:]}ma/BOS_M{year}_dl.xlsx',
        'industry': f'oesm{year[2:]}in4/{prefix}_M{year}_dl.xlsx'
    }


def get_data(year=CUR_YEAR, cut_by='national', area_focus=None,
    industry_scope=None,rtype='dataframe', set_missing_figures_as_na=True):
    """Get a dataset from the Occupational Employment Statistics (OES).

    The OES database contains statistics for various occupations.
    Primary statistics include wage, salary and total employment by occupation.

    Default behavior returns occupational data at a national
    level. This behavior can be overridden by adding options.

    Intended usage is to return a pandas dataframe for easy data
    analysis. This can be overwridden to return a primitive i/o object for
    different data processing decisions.


    Parameters
    ----------
    year : str
        year must be in form 'YYYY'. This package only supports OES after 2014
    cut_by : str
        Get occupation figures that are either cut by location
        or industry. Only three options are allowed: `state`, `area`,
        or `industry`. If not specified, default behavior is
        to return nationwide figures.
    area_focus : str
        If `cut_by = area` then an `area_focus` must also be
        specifed. Options include: metros, metro-divisions, or non-metros
    industry_scope : int, or None
        If `cut_by = industry` then an `industry_scope` must also be specified.
        Options include 3, 4, 5 or 6 digit scope.
        If not specified, then the default is top level sectors (i.e 2 digit).
        Industry scope describes the level of industry granularity. Higher the
        scope, the more granular the industries will be.
    set_missing_figures_as_na : bool, Default = True
        BLS uses ['*', '**', '#', '~'] to designate missing non-numeric figures
        in columns that have numeric statistics, such as hourly wage. This
        mismatch converts the whole column to an object and not a number type.
        By keeping this argument to True, this symbols will get converted
        to NA values allowing these columns to be calculated and treated as
        numbers.
    rtype : str
        Default behavior is to return a pandas dataframe.
        If you want a primitive i/o object that supports open(),
        then specify rtype='io'.

    Returns
    -------
    pd.Dataframe, or io file like object

    Usage:

    >>> df = get_data(2017, cut_by='state')
    >>> df.head()
       AREA  ST    STATE OCC_CODE  ...   A_PCT75 A_PCT90 ANNUAL HOURLY
    0     1  AL  Alabama  00-0000  ...     52020   78690    NaN    NaN
    1     1  AL  Alabama  11-0000  ...    133360  188860    NaN    NaN
    2     1  AL  Alabama  11-1011  ...         #       #    NaN    NaN
    3     1  AL  Alabama  11-1021  ...    147860       #    NaN    NaN
    4     1  AL  Alabama  11-1031  ...     24630   47510   True    NaN

    [5 rows x 25 columns]

    """
    if int(year) < 2014:
        raise ValueError(f'Year:{year}. OES only supports years post 2014.')
    if int(year) > CUR_YEAR:
        raise ValueError(f'Year:{year}. OES data not available yet.')

    if industry_scope != None and industry_scope not in range(3, 7):
        raise ValueError(f'Industry scope:{industry_scope}. '
            'Not a valid industry scope. Options include ints from 3 to 6')

    OES_ZIP_URLS = _get_zip_urls(str(year))
    OES_FILENAMES = _get_filenames(str(year), industry_scope)

    zip_url = OES_ZIP_URLS.get(cut_by)
    if zip_url == None:
        raise ValueError('"{}" is not a valid cut_by option\n' \
            'valid options include:\n{}' \
            .format(cut_by, [k for k in OES_ZIP_URLS.keys()]))

    if cut_by == 'area':
        filename = OES_FILENAMES.get(area_focus)
        if filename == None:
            raise ValueError('"{}" is not a valid area focus\n' \
                'valid options include:\n{}' \
                .format(cut_by, ['metros', 'metros-divisions', 'non-metros']))
    else:
        filename = OES_FILENAMES.get(cut_by)

    fp = util.get_file(zip_url, filename)

    if set_missing_figures_as_na:
        na_values = ['*', '**', '#', '~']
    else:
        na_values = []
        
    if rtype == 'dataframe':
        return pd.read_excel(fp, na_values = na_values)
    elif rtype == 'io':
        return fp
    else:
        raise ValueError('{} is not a valid return type\n' \
            'valid return types are `dataframe` or `io`' \
            .format(rtype))
