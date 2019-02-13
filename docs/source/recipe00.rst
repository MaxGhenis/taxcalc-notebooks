
Basic Recipe: Static Analysis of a Simple Reform
================================================

This is the recipe you should follow first. Mastering this recipe is a
prerequisite for all the other recipes in this cookbook.

**Ingredients**

`Policy
reform <http://open-source-economics.github.io/Tax-Calculator/reformA.json>`__
in the ``ingredients/reformA.json`` file.

*When following the recipe as shown below, you will get several
instances of the same **ignored** error message from deep inside the
Pandas library that is being used by Tax-Calculator. After conferring
with the Pandas developers, our expectation is these error messages will
go away when we upgrade to Pandas version 0.22.0, which is scheduled to
be released in January 2018, and which fixes a bug in the Pandas
library. Meanwhile, the error messages are annoying but harmless.*

Imports
-------

.. code:: ipython3

    from __future__ import print_function  # Necessary only if using Python 2.7.
    import taxcalc as tc
    import pandas as pd
    import json
    from bokeh.io import show, output_notebook

Setup
-----

Use publicly-available CPS input file.

NOTE: if you have access to the restricted-use IRS-SOI PUF-based input
file and you have that file (named 'puf.csv') located in the directory
where this script is located, then you can substitute the following
statement for the prior statement:

``recs = Records()``

.. code:: ipython3

    recs = tc.Records.cps_constructor()

Specify ``Calculator`` object for static analysis of current-law policy.

.. code:: ipython3

    pol = tc.Policy()
    calc1 = tc.Calculator(policy=pol, records=recs)


.. parsed-literal::

    You loaded data for 2014.
    Tax-Calculator startup automatically extrapolated your data to 2014.


NOTE: ``calc1`` now contains a PRIVATE COPY of ``pol`` and a PRIVATE
COPY of ``recs``, so we can continue to use ``pol`` and ``recs`` in this
script without any concern about side effects from ``Calculator`` method
calls on ``calc1``.

Calculate aggregate current-law income tax liabilities for 2018.

.. code:: ipython3

    calc1.advance_to_year(2018)
    calc1.calc_all()
    itax_rev1 = calc1.weighted_total('iitax')


.. code:: ipython3

    print('2018_CLP_itax_rev($B)= {:.2f}'.format(itax_rev1 * 1e-9))


.. parsed-literal::

    2018_CLP_itax_rev($B)= 1220.29


Read JSON reform file and use (the default) static analysis assumptions.

*Requires ``reformA.json`` to have been downloaded and put in
``ingredients`` folder.*

.. code:: ipython3

    reform_filename = './ingredients/reformA.json'
    params = tc.Calculator.read_json_param_objects(reform=reform_filename,
                                                   assump=None)
    print(f"raw param data: {json.dumps(params, indent=4)}")


.. parsed-literal::

    raw param data: {
        "policy": {
            "2018": {
                "_STD": [
                    [
                        12000,
                        24000,
                        12000,
                        18000,
                        24000
                    ]
                ],
                "_STD_Dep": [
                    0
                ],
                "_STD_Aged": [
                    [
                        0,
                        0,
                        0,
                        0,
                        0
                    ]
                ],
                "_II_rt5": [
                    0.35
                ],
                "_II_rt6": [
                    0.37
                ],
                "_II_rt7": [
                    0.42
                ],
                "_PT_rt5": [
                    0.35
                ],
                "_PT_rt6": [
                    0.37
                ],
                "_PT_rt7": [
                    0.42
                ]
            }
        },
        "consumption": {},
        "growdiff_baseline": {},
        "growdiff_response": {}
    }


Print reform documentation.

.. code:: ipython3

    print(tc.Calculator.reform_documentation(params))


.. parsed-literal::

    REFORM DOCUMENTATION
    Baseline Growth-Difference Assumption Values by Year:
    none: using default baseline growth assumptions
    Policy Reform Parameter Values by Year:
    2018:
     _II_rt5 : 0.35
      name: Personal income (regular/non-AMT/non-pass-through) tax rate 5
      desc: The third highest tax rate, applied to the portion of taxable income
            below tax bracket 5 and above tax bracket 4.
      baseline_value: 0.32
     _II_rt6 : 0.37
      name: Personal income (regular/non-AMT/non-pass-through) tax rate 6
      desc: The second higher tax rate, applied to the portion of taxable income
            below tax bracket 6 and above tax bracket 5.
      baseline_value: 0.35
     _II_rt7 : 0.42
      name: Personal income (regular/non-AMT/non-pass-through) tax rate 7
      desc: The tax rate applied to the portion of taxable income below tax
            bracket 7 and above tax bracket 6.
      baseline_value: 0.37
     _PT_rt5 : 0.35
      name: Pass-through income tax rate 5
      desc: The third highest tax rate, applied to the portion of income from sole
            proprietorships, partnerships and S-corporations below tax bracket 5
            and above tax bracket 4.
      baseline_value: 0.32
     _PT_rt6 : 0.37
      name: Pass-through income tax rate 6
      desc: The second higher tax rate, applied to the portion of income from sole
            proprietorships, partnerships and S-corporations below tax bracket 6
            and above tax bracket 5.
      baseline_value: 0.35
     _PT_rt7 : 0.42
      name: Pass-through income tax rate 7
      desc: The highest tax rate, applied to the portion of income from sole
            proprietorships, partnerships and S-corporations below tax bracket 7
            and above tax bracket 6.
      baseline_value: 0.37
     _STD : [12000, 24000, 12000, 18000, 24000]
            ['single', 'joint', 'separate', 'headhousehold', 'widow']
      name: Standard deduction amount
      desc: Amount filing unit can use as a standard deduction.
      baseline_value: [12000.0, 24000.0, 12000.0, 18000.0, 24000.0]
     _STD_Aged : [0, 0, 0, 0, 0]
                 ['single', 'joint', 'separate', 'headhousehold', 'widow']
      name: Additional standard deduction for blind and aged
      desc: To get the standard deduction for aged or blind individuals, taxpayers
            need to add this value to regular standard deduction.
      baseline_value: [1600.0, 1300.0, 1300.0, 1600.0, 1300.0]
     _STD_Dep : 0
      name: Standard deduction for dependents
      desc: This is the maximum standard deduction for dependents.
      baseline_value: 1050.0
    


Implement reform and check for reform error messages.

.. code:: ipython3

    pol.implement_reform(params['policy'])
    if pol.parameter_errors:
        print(f"The policy reform generated the following errors: {pol.parameter_errors}")

Calculate
---------

Specify Calculator object for static analysis of reform policy.

.. code:: ipython3

    calc2 = tc.Calculator(policy=pol, records=recs)


.. parsed-literal::

    You loaded data for 2014.
    Tax-Calculator startup automatically extrapolated your data to 2014.


Calculate reform income tax liabilities for 2018.

.. code:: ipython3

    calc2.advance_to_year(2018)
    calc2.calc_all()
    itax_rev2 = calc2.weighted_total('iitax')
    print('2018_REF_itax_rev($B)= {:.2f}'.format(itax_rev2 * 1e-9))


.. parsed-literal::

    2018_REF_itax_rev($B)= 1249.73


Results
-------

Print total revenue estimates for 2018.

*Estimates in billons of dollars rounded to nearest hundredth of a
billion.*

.. code:: ipython3

    print('2018_CLP_itax_rev($B)= {:.2f}'.format(itax_rev1 * 1e-9))
    print('2018_REF_itax_rev($B)= {:.2f}'.format(itax_rev2 * 1e-9))


.. parsed-literal::

    2018_CLP_itax_rev($B)= 1220.29
    2018_REF_itax_rev($B)= 1249.73


Generate several other standard results tables.

.. code:: ipython3

    # aggregate diagnostic tables for cyr
    clp_diagnostic_table = calc1.diagnostic_table(1)
    ref_diagnostic_table = calc2.diagnostic_table(1)
    
    # income-tax distribution for cyr with CLP and REF results side-by-side
    dist_table1, dist_table2 = calc1.distribution_tables(calc2, 'weighted_deciles')
    assert isinstance(dist_table1, pd.DataFrame)
    assert isinstance(dist_table2, pd.DataFrame)
    dist_extract = pd.DataFrame()
    dist_extract['funits(#m)'] = dist_table1['s006']
    dist_extract['itax1($b)'] = dist_table1['iitax']
    dist_extract['itax2($b)'] = dist_table2['iitax']
    dist_extract['aftertax_inc1($b)'] = dist_table1['aftertax_income']
    dist_extract['aftertax_inc2($b)'] = dist_table2['aftertax_income']
    
    # income-tax difference table by expanded-income decile for cyr
    diff_table = calc1.difference_table(calc2, 'weighted_deciles', 'iitax')
    assert isinstance(diff_table, pd.DataFrame)
    diff_extract = pd.DataFrame()
    dif_colnames = ['count', 'tot_change', 'mean',
                    'pc_aftertaxinc']
    ext_colnames = ['funits(#m)', 'agg_diff($b)', 'mean_diff($)',
                    'aftertaxinc_diff(%)']
    for dname, ename in zip(dif_colnames, ext_colnames):
        diff_extract[ename] = diff_table[dname]

Plotting
--------

Generate a decile graph and display it using Bokeh.

.. code:: ipython3

    fig = calc1.decile_graph(calc2)

.. code:: ipython3

    output_notebook()



.. raw:: html

    
        <div class="bk-root">
            <a href="https://bokeh.pydata.org" target="_blank" class="bk-logo bk-logo-small bk-logo-notebook"></a>
            <span id="1113">Loading BokehJS ...</span>
        </div>




.. code:: ipython3

    show(fig)



.. raw:: html

    
    
    
    
    
    
      <div class="bk-root" id="81145574-dff6-45ec-bcdb-07ceea3324bc" data-root-id="1002"></div>





Print tables
------------

CLP diagnostic table for 2018.

.. code:: ipython3

    clp_diagnostic_table




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>2018</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>Returns (#m)</th>
          <td>162.860</td>
        </tr>
        <tr>
          <th>AGI ($b)</th>
          <td>10772.526</td>
        </tr>
        <tr>
          <th>Itemizers (#m)</th>
          <td>28.270</td>
        </tr>
        <tr>
          <th>Itemized Deduction ($b)</th>
          <td>763.152</td>
        </tr>
        <tr>
          <th>Standard Deduction Filers (#m)</th>
          <td>134.600</td>
        </tr>
        <tr>
          <th>Standard Deduction ($b)</th>
          <td>2314.591</td>
        </tr>
        <tr>
          <th>Personal Exemption ($b)</th>
          <td>0.000</td>
        </tr>
        <tr>
          <th>Taxable Income ($b)</th>
          <td>8153.662</td>
        </tr>
        <tr>
          <th>Regular Tax ($b)</th>
          <td>1379.356</td>
        </tr>
        <tr>
          <th>AMT Income ($b)</th>
          <td>10234.318</td>
        </tr>
        <tr>
          <th>AMT Liability ($b)</th>
          <td>1.330</td>
        </tr>
        <tr>
          <th>AMT Filers (#m)</th>
          <td>0.250</td>
        </tr>
        <tr>
          <th>Tax before Credits ($b)</th>
          <td>1380.686</td>
        </tr>
        <tr>
          <th>Refundable Credits ($b)</th>
          <td>78.899</td>
        </tr>
        <tr>
          <th>Nonrefundable Credits ($b)</th>
          <td>90.133</td>
        </tr>
        <tr>
          <th>Reform Surtaxes ($b)</th>
          <td>0.000</td>
        </tr>
        <tr>
          <th>Other Taxes ($b)</th>
          <td>8.634</td>
        </tr>
        <tr>
          <th>Ind Income Tax ($b)</th>
          <td>1220.289</td>
        </tr>
        <tr>
          <th>Payroll Taxes ($b)</th>
          <td>1193.607</td>
        </tr>
        <tr>
          <th>Combined Liability ($b)</th>
          <td>2413.895</td>
        </tr>
        <tr>
          <th>With Income Tax &lt;= 0 (#m)</th>
          <td>59.700</td>
        </tr>
        <tr>
          <th>With Combined Tax &lt;= 0 (#m)</th>
          <td>38.060</td>
        </tr>
      </tbody>
    </table>
    </div>



REF diagnostic table for 2018.

.. code:: ipython3

    ref_diagnostic_table




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>2018</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>Returns (#m)</th>
          <td>162.860</td>
        </tr>
        <tr>
          <th>AGI ($b)</th>
          <td>10772.526</td>
        </tr>
        <tr>
          <th>Itemizers (#m)</th>
          <td>29.250</td>
        </tr>
        <tr>
          <th>Itemized Deduction ($b)</th>
          <td>781.724</td>
        </tr>
        <tr>
          <th>Standard Deduction Filers (#m)</th>
          <td>133.620</td>
        </tr>
        <tr>
          <th>Standard Deduction ($b)</th>
          <td>2230.969</td>
        </tr>
        <tr>
          <th>Personal Exemption ($b)</th>
          <td>0.000</td>
        </tr>
        <tr>
          <th>Taxable Income ($b)</th>
          <td>8184.432</td>
        </tr>
        <tr>
          <th>Regular Tax ($b)</th>
          <td>1408.941</td>
        </tr>
        <tr>
          <th>AMT Income ($b)</th>
          <td>10223.472</td>
        </tr>
        <tr>
          <th>AMT Liability ($b)</th>
          <td>1.232</td>
        </tr>
        <tr>
          <th>AMT Filers (#m)</th>
          <td>0.240</td>
        </tr>
        <tr>
          <th>Tax before Credits ($b)</th>
          <td>1410.173</td>
        </tr>
        <tr>
          <th>Refundable Credits ($b)</th>
          <td>78.874</td>
        </tr>
        <tr>
          <th>Nonrefundable Credits ($b)</th>
          <td>90.202</td>
        </tr>
        <tr>
          <th>Reform Surtaxes ($b)</th>
          <td>0.000</td>
        </tr>
        <tr>
          <th>Other Taxes ($b)</th>
          <td>8.634</td>
        </tr>
        <tr>
          <th>Ind Income Tax ($b)</th>
          <td>1249.731</td>
        </tr>
        <tr>
          <th>Payroll Taxes ($b)</th>
          <td>1193.607</td>
        </tr>
        <tr>
          <th>Combined Liability ($b)</th>
          <td>2443.338</td>
        </tr>
        <tr>
          <th>With Income Tax &lt;= 0 (#m)</th>
          <td>59.180</td>
        </tr>
        <tr>
          <th>With Combined Tax &lt;= 0 (#m)</th>
          <td>37.750</td>
        </tr>
      </tbody>
    </table>
    </div>



Extract of 2018 distribution tables by baseline expanded-income decile.

*Note: deciles are numbered 0-9 with top decile divided into bottom 5%,
next 4%, and top 1%, in the lines numbered 11-13, respectively.*

.. code:: ipython3

    dist_extract




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>funits(#m)</th>
          <th>itax1($b)</th>
          <th>itax2($b)</th>
          <th>aftertax_inc1($b)</th>
          <th>aftertax_inc2($b)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0-10n</th>
          <td>0.05</td>
          <td>0.004</td>
          <td>0.004</td>
          <td>-11.895</td>
          <td>-11.895</td>
        </tr>
        <tr>
          <th>0-10z</th>
          <td>0.91</td>
          <td>0.000</td>
          <td>0.000</td>
          <td>0.000</td>
          <td>0.000</td>
        </tr>
        <tr>
          <th>0-10p</th>
          <td>15.33</td>
          <td>-4.254</td>
          <td>-4.242</td>
          <td>159.359</td>
          <td>159.348</td>
        </tr>
        <tr>
          <th>10-20</th>
          <td>16.29</td>
          <td>-2.556</td>
          <td>-2.534</td>
          <td>371.961</td>
          <td>371.939</td>
        </tr>
        <tr>
          <th>20-30</th>
          <td>16.29</td>
          <td>1.750</td>
          <td>1.785</td>
          <td>496.507</td>
          <td>496.472</td>
        </tr>
        <tr>
          <th>30-40</th>
          <td>16.29</td>
          <td>7.262</td>
          <td>7.336</td>
          <td>612.681</td>
          <td>612.607</td>
        </tr>
        <tr>
          <th>40-50</th>
          <td>16.29</td>
          <td>15.018</td>
          <td>15.213</td>
          <td>755.652</td>
          <td>755.458</td>
        </tr>
        <tr>
          <th>50-60</th>
          <td>16.29</td>
          <td>26.517</td>
          <td>26.813</td>
          <td>930.189</td>
          <td>929.893</td>
        </tr>
        <tr>
          <th>60-70</th>
          <td>16.29</td>
          <td>52.589</td>
          <td>53.086</td>
          <td>1144.049</td>
          <td>1143.551</td>
        </tr>
        <tr>
          <th>70-80</th>
          <td>16.29</td>
          <td>92.978</td>
          <td>93.818</td>
          <td>1435.491</td>
          <td>1434.652</td>
        </tr>
        <tr>
          <th>80-90</th>
          <td>16.29</td>
          <td>188.085</td>
          <td>189.455</td>
          <td>1915.081</td>
          <td>1913.711</td>
        </tr>
        <tr>
          <th>90-100</th>
          <td>16.29</td>
          <td>842.895</td>
          <td>868.999</td>
          <td>3871.005</td>
          <td>3844.901</td>
        </tr>
        <tr>
          <th>ALL</th>
          <td>162.86</td>
          <td>1220.289</td>
          <td>1249.731</td>
          <td>11680.079</td>
          <td>11650.637</td>
        </tr>
        <tr>
          <th>90-95</th>
          <td>8.14</td>
          <td>189.931</td>
          <td>191.090</td>
          <td>1305.858</td>
          <td>1304.699</td>
        </tr>
        <tr>
          <th>95-99</th>
          <td>6.51</td>
          <td>287.130</td>
          <td>289.200</td>
          <td>1505.038</td>
          <td>1502.968</td>
        </tr>
        <tr>
          <th>Top 1%</th>
          <td>1.63</td>
          <td>365.834</td>
          <td>388.709</td>
          <td>1060.109</td>
          <td>1037.234</td>
        </tr>
      </tbody>
    </table>
    </div>



Extract of 2018 income-tax difference table by expanded-income decile.

.. code:: ipython3

    diff_extract




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>funits(#m)</th>
          <th>agg_diff($b)</th>
          <th>mean_diff($)</th>
          <th>aftertaxinc_diff(%)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0-10n</th>
          <td>0.05</td>
          <td>0.000</td>
          <td>0.0</td>
          <td>0.0</td>
        </tr>
        <tr>
          <th>0-10z</th>
          <td>0.91</td>
          <td>0.000</td>
          <td>0.0</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>0-10p</th>
          <td>15.33</td>
          <td>0.012</td>
          <td>0.8</td>
          <td>-0.0</td>
        </tr>
        <tr>
          <th>10-20</th>
          <td>16.29</td>
          <td>0.022</td>
          <td>1.4</td>
          <td>-0.0</td>
        </tr>
        <tr>
          <th>20-30</th>
          <td>16.29</td>
          <td>0.035</td>
          <td>2.2</td>
          <td>-0.0</td>
        </tr>
        <tr>
          <th>30-40</th>
          <td>16.29</td>
          <td>0.074</td>
          <td>4.5</td>
          <td>-0.0</td>
        </tr>
        <tr>
          <th>40-50</th>
          <td>16.29</td>
          <td>0.194</td>
          <td>11.9</td>
          <td>-0.0</td>
        </tr>
        <tr>
          <th>50-60</th>
          <td>16.29</td>
          <td>0.295</td>
          <td>18.1</td>
          <td>-0.0</td>
        </tr>
        <tr>
          <th>60-70</th>
          <td>16.29</td>
          <td>0.497</td>
          <td>30.5</td>
          <td>-0.0</td>
        </tr>
        <tr>
          <th>70-80</th>
          <td>16.29</td>
          <td>0.839</td>
          <td>51.5</td>
          <td>-0.1</td>
        </tr>
        <tr>
          <th>80-90</th>
          <td>16.29</td>
          <td>1.370</td>
          <td>84.1</td>
          <td>-0.1</td>
        </tr>
        <tr>
          <th>90-100</th>
          <td>16.29</td>
          <td>26.104</td>
          <td>1602.8</td>
          <td>-0.7</td>
        </tr>
        <tr>
          <th>ALL</th>
          <td>162.86</td>
          <td>29.442</td>
          <td>180.8</td>
          <td>-0.3</td>
        </tr>
        <tr>
          <th>90-95</th>
          <td>8.14</td>
          <td>1.159</td>
          <td>142.4</td>
          <td>-0.1</td>
        </tr>
        <tr>
          <th>95-99</th>
          <td>6.51</td>
          <td>2.070</td>
          <td>317.7</td>
          <td>-0.1</td>
        </tr>
        <tr>
          <th>Top 1%</th>
          <td>1.63</td>
          <td>22.875</td>
          <td>14044.6</td>
          <td>-2.2</td>
        </tr>
      </tbody>
    </table>
    </div>


