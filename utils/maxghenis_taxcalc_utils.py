from __future__ import print_function  # Necessary only if using Python 2.7.
from taxcalc import *
# On Python 3.6 use "import urllib.request as url_lib".
import urllib as url_lib

# Folders where reforms live.
TAXCALC_GITHUB_BASE_URL = ('https://raw.githubusercontent.com/'
                           'open-source-economics/Tax-Calculator/master/'
                           'taxcalc/reforms/')

MAXGHENIS_GITHUB_BASE_URL = ('https://raw.githubusercontent.com/'
                             'MaxGhenis/taxcalc-notebooks/reforms/')

def read_reform_from_taxcalc_github(reform_name):
  return url_lib.urlopen(TAXCALC_GITHUB_BASE_URL + reform1_name).read()

def read_reform_from_maxghenis_github(reform_name):
  return url_lib.urlopen(TAXCALC_GITHUB_BASE_URL + reform1_name).read()
