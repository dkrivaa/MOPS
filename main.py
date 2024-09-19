"""
Run this file to update data from Ministry of Finance data.
At present, data is updated to 23.5.2024
"""


from history import update_annual
from takanot import update_takanot

update_annual()
update_takanot()