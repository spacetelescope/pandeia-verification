import numpy as np
import glob
import sys

def convert(entry):
    """
    Converts a data structure from bytes to strings
    """
    #print(type(entry),entry)
    if isinstance(entry, bytes):
        return entry.decode('utf-8')
    elif isinstance(entry, dict):
        newdict = {}
        for key,value in entry.items():
            key = convert(key)
            newdict[key] = convert(value)
        return newdict
    elif isinstance(entry, list) or isinstance(entry, np.ndarray):
        for index, dummy in enumerate(entry):
            entry[index] = convert(entry[index])
        return entry
    elif isinstance(entry, tuple):
        outlist = []
        for index, dummy in enumerate(entry):
            outlist.append(convert(entry[index]))
        return tuple(outlist)
    else:
        return entry

def gettext(data,item):
    """
    Text labels. Priority is: Disperser (and order) if it exists, then filter
    if it exists. If neither exist (unlikely), just use aperture.
    """
    if 'disperser' in data['configs'][x]:
        if 'filter' in data['configs'][x]:
            if data['configs'][x]['filter'] == None:
                if 'order' in data:
                    textval = '{} {}'.format(data['configs'][x]['disperser'], data['orders'][x])
                else:
                    textval = '{}'.format(data['configs'][x]['disperser'])
            else:
                textval = '{} {}'.format(data['configs'][x]['disperser'], data['configs'][x]['filter'])
        else:
            textval = '{} {}'.format(data['configs'][x]['aperture'], data['configs'][x]['disperser'])
    else:
        if 'filter' in data['configs'][x]:
            textval = data['configs'][x]['filter']
        else:
            textval = data['configs'][x]['aperture']
    return textval

folder = sys.argv[1]
files = glob.glob('../{}/*_sensitivity.npz'.format(folder))

for file in files:
    data = dict(np.load(file, encoding="bytes"))
    data = convert(data)
    inst,mode,*dummy = file.split("/")[-1].split("_")
    with open("{}_{}.csv".format(inst,mode),"w") as outfile:
        outfile.write("#{} {}\n".format(inst.upper(),mode.upper()))
        outfile.write("# wavelengths in microns\n# Lim_fluxes in microJy\n# sat_limits in Jy\n")
        outfile.write("wave,lim_fluxes,sat_limits\n")
        for x,keys in enumerate(data['configs']):
            text = gettext(data,x)
            outfile.write("#{}\n".format(text))
            if len(data['wavelengths'][x]) == 1:
                outfile.write("{:7.6f},{:7.6f},{:7.6f}\n".format(data['wavelengths'][x][0],data['lim_fluxes'][x][0], data['sat_limits'][x]))
            else:
                for y in range(len(data['wavelengths'][x])):
                    outfile.write("{:7.6f},{:7.6f},{:7.6f}\n".format(data['wavelengths'][x][y],data['lim_fluxes'][x][y], data['sat_limits'][x][y]))
