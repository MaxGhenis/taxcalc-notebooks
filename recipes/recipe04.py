from taxcalc import *
import pandas as pd
import behresp

# use publicly-available CPS input file
recs = Records.cps_constructor()

# specify Calculator object for static analysis of current-law policy
pol = Policy()
calc1 = Calculator(policy=pol, records=recs)

cyr = 2020

# calculate current-law tax liabilities for cyr
calc1.advance_to_year(cyr)
calc1.calc_all()

# calculate marginal tax rate wrt cash charitable giving
(_, _, mtr1) = calc1.mtr('e19800', calc_all_already_called=True,
                         wrt_full_compensation=False)

# specify Calculator object for static analysis of reform policy
pol.implement_reform(Policy.read_json_reform('reformB.json'))
calc2 = Calculator(policy=pol, records=recs)

# calculate reform tax liabilities for cyr
calc2.advance_to_year(cyr)
calc2.calc_all()

# calculate marginal tax rate wrt cash charitable giving
(_, _, mtr2) = calc2.mtr('e19800', calc_all_already_called=True,
                         wrt_full_compensation=False)

# extract variables needed for quantity_response function
# (note the aftertax price is 1+mtr because mtr wrt charity is non-positive)
vdf = calc1.dataframe(['s006', 'e19800', 'e00200'])
vdf['price1'] = 1.0 + mtr1
vdf['price2'] = 1.0 + mtr2
vdf['atinc1'] = calc1.array('aftertax_income')
vdf['atinc2'] = calc2.array('aftertax_income')

# group filing units into earnings groups with different response elasticities
# (note earnings groups are just an example based on no empirical results)
EARNINGS_BINS = [-9e99, 50e3, 9e99]  # two groups: below and above $50,000
vdf['table_row'] = pd.cut(vdf.e00200, EARNINGS_BINS, right=False).astype(str)

vdf['price_elasticity'] = np.where(vdf.e00200 < EARNINGS_BINS[1],
                                   -0.1, -0.4)
vdf['income_elasticity'] = 0.1

# Calculate response based on features of each filing unit.
vdf['response'] = behresp.quantity_response(vdf.e19800,
                                            vdf.price_elasticity,
                                            vdf.price1,
                                            vdf.price2,
                                            vdf.income_elasticity,
                                            vdf.atinc1,
                                            vdf.atinc2)

# Add weighted totals.
# Can also use microdf as mdf.add_weighted_totals(vdf, ['response', 'e19800'])
vdf['e19800_b'] = vdf.s006 * vdf.e19800 / 1e9
vdf['response_b'] = vdf.s006 * vdf.response / 1e9
vdf['funits_m'] = vdf.s006 / 1e6

SUM_VARS = ['funits_m', 'e19800_b', 'response_b']
# Sum weighted total columns for each income group.
grouped = vdf.groupby('table_row')[SUM_VARS].sum()
# Add a total row and make the index a column for printing.
grouped.loc['TOTAL'] = grouped.sum()
grouped.reset_index(inplace=True)

# Calculate percent response and drop unnecessary total.
grouped['pct_response'] = 100 * grouped.response_b / grouped.e19800_b
grouped.drop('e19800_b', axis=1, inplace=True)

# Rename columns for printing.
grouped.columns = ['Earnings Group', 'Num(#M)', 'Resp($B)', 'Resp(%)']

print('Response in Charitable Giving by Earnings Group')
print(grouped.round(3).to_string(index=False))
