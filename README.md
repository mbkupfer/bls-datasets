# bls-datasets
Wrapper for making datasets easily accessible to pyhon developers.

Integrated datasets include:
- [Occupational Employment Statistics (OES)](https://www.bls.gov/oes/)
- [Quarterly Census of Employment and Wages (QCEW)](https://www.bls.gov/cew/)

For BLS series lookups, checkout OlverSherouse's library [BLS](https://github.com/OliverSherouse/bls)
# Usage

```
>>> from bls_datasets import oes, qcew

# OES example:

>>> df_oes = oes.get_data(year=2017)
>>> df_oes.columns
Index(['OCC_CODE', 'OCC_TITLE', 'OCC_GROUP', 'TOT_EMP', 'EMP_PRSE', 'H_MEAN',
       'A_MEAN', 'MEAN_PRSE', 'H_PCT10', 'H_PCT25', 'H_MEDIAN', 'H_PCT75',
       'H_PCT90', 'A_PCT10', 'A_PCT25', 'A_MEDIAN', 'A_PCT75', 'A_PCT90',
       'ANNUAL', 'HOURLY'],
      dtype='object')

# Which occupation had the highest total employment in 2017?

>>> detailed = df_oes[df_oes.OCC_GROUP == 'detailed']
>>> detailed[detailed.TOT_EMP == detailed.TOT_EMP.max()].OCC_TITLE
772    Retail Salespersons

# QCEW example:
>>> df_qcew = qcew.get_data('industry', rtype='dataframe', year='2017',
...             qtr='1', industry='10')
>>> df_qcew.columns
Index(['area_fips', 'own_code', 'industry_code', 'agglvl_code', 'size_code',
       'year', 'qtr', 'disclosure_code', 'qtrly_estabs', 'month1_emplvl',
       'month2_emplvl', 'month3_emplvl', 'total_qtrly_wages',
       'taxable_qtrly_wages', 'qtrly_contributions', 'avg_wkly_wage',
       'lq_disclosure_code', 'lq_qtrly_estabs', 'lq_month1_emplvl',
       'lq_month2_emplvl', 'lq_month3_emplvl', 'lq_total_qtrly_wages',
       'lq_taxable_qtrly_wages', 'lq_qtrly_contributions', 'lq_avg_wkly_wage',
       'oty_disclosure_code', 'oty_qtrly_estabs_chg',
       'oty_qtrly_estabs_pct_chg', 'oty_month1_emplvl_chg',
       'oty_month1_emplvl_pct_chg', 'oty_month2_emplvl_chg',
       'oty_month2_emplvl_pct_chg', 'oty_month3_emplvl_chg',
       'oty_month3_emplvl_pct_chg', 'oty_total_qtrly_wages_chg',
       'oty_total_qtrly_wages_pct_chg', 'oty_taxable_qtrly_wages_chg',
       'oty_taxable_qtrly_wages_pct_chg', 'oty_qtrly_contributions_chg',
       'oty_qtrly_contributions_pct_chg', 'oty_avg_wkly_wage_chg',
       'oty_avg_wkly_wage_pct_chg'],
      dtype='object')

# What were the aberage weekly earnings in Fresno County for 2017 Q1?

# FIPS code, area title
# 06019,	Fresno County, California

>>> fresno = df_qcew[(df_qcew.own_code == 0) & (df_qcew.area_fips == '06019')]
>>> fresno.avg_wkly_wage.values[0]
803


```

# Notes on datasets


**OES**

OES consists of occupational statistics, primarily: employment, age, and salary. To learn more about this survey, you can visit this [link](https://www.bls.gov/oes/oes_emp.htm).

Note that due to idiosyncracies in filenaming conventions, this package only allows data access starting in 2014. Earlier files are available, although they are broken into multiple excel spreadsheets and have different naming patterns. I will not integrate any earlier years, unless I see it necessary, or recieve enough user requests.

**QCEW**

QCEW conists of employer reported occupational statistics. 

Common gotcha with QCEW data:
- Datatypes are not always what you expect them to be. Reference the following tables when performing dataframe operations
  - [Quarterly data slice layout](https://data.bls.gov/cew/doc/access/csv_data_slices.htm##QTR_LAYOUT)
  - [Annual averages slice layout](https://data.bls.gov/cew/doc/access/csv_data_slices.htm##ANNUAL_LAYOUT)
- Due to employer confidentiality, some of the figures may be unavailable. This is especially true when making more granular data cuts. Do check the disclosure_code columns for this.
