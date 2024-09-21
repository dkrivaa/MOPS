"""
Run this file to update data from Ministry of Finance data on wix site (MOPS).
At present, data is updated to 23.5.2024
"""

from history import update_annual, update_annual_special
from takanot import update_takanot, update_takanot_special

# update_annual()
update_annual_special()
# update_takanot()
# update_takanot_special()

