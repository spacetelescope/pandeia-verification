import os, json
pandeia_data = os.environ["pandeia_refdata"]

INST= "wfi"

with open(f"{pandeia_data}/roman/{INST}/config.json") as configfile:
    config_data = json.load(configfile)

ma_tables = config_data["readout_pattern_config"]

del ma_tables["meta"]
del ma_tables["diagnostic"]

imag_tables = []
spec_tables = []

print("Best 10,000 second setups\n          MA Table         #      nexp\n--------------------")

for ma_table in ma_tables:
    for res, time in enumerate(ma_tables[ma_table]['integration_duration']):
        remainders = 10000/time
        
        if "wim" in ma_tables[ma_table]["observing_mode"]:
            imag_tables.append([ma_table, res+ma_tables[ma_table]['num_pre_science_resultants'], remainders])
        elif "wsm" in ma_tables[ma_table]["observing_mode"]:
            spec_tables.append([ma_table, res+ma_tables[ma_table]['num_pre_science_resultants'], remainders])

print("Imaging:", sorted(imag_tables, key=(lambda a: a[2] % 1))[0])
print("Spec:\t", sorted(spec_tables, key=(lambda a: a[2] % 1))[0])

print("--------------------\n Or for full tables:\n--------------------")

imag_tables = []
spec_tables = []

for ma_table in ma_tables:
    time = ma_tables[ma_table]['integration_duration'][-1]
    remainders = 10000/time
    
    if "wim" in ma_tables[ma_table]["observing_mode"]:
        imag_tables.append([ma_table, -1, remainders])
    elif "wsm" in ma_tables[ma_table]["observing_mode"]:
        spec_tables.append([ma_table, -1, remainders])

print("Imaging:", sorted(imag_tables, key=(lambda a: a[2] % 1))[0])
print("Spec:\t", sorted(spec_tables, key=(lambda a: a[2] % 1))[0])
