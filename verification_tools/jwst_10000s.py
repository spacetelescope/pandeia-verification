from pandeia.engine.exposure import ExposureSpec_MultiAccum
from pandeia.engine.data_util import InstrumentConfiguration
from pandeia.engine.calc_utils import build_default_calc
from pandeia.engine.perform_calculation import perform_calculation
import os, json
import sys
pandeia_data = os.environ["pandeia_refdata"]

INST = sys.argv[1]
MODE = sys.argv[2]

def find_10000(exposure_spec):
    length = []
    for ngroup in range(10,100):
        for nint in range(1, 100):
            for nexp in range(1,100):
                exposure_spec.ngroup = ngroup
                exposure_spec.nint = nint
                exposure_spec.nexp = nexp
                exposure_spec.get_times()
                length.append({"exptime": exposure_spec.total_exposure_time, "ngroup": ngroup, "nint": nint, "nexp": nexp})
    sorted_length = sorted(length, key=lambda a: abs(a["exptime"] - 10000.0))

    print("Best 10,000 second setups\n-------------------------")
    for i in range(10):
        print(sorted_length[i])
    print("\n\n")


with open(f"{pandeia_data}/jwst/{INST}/config.json") as configfile:
    config_data = json.load(configfile)

calc = build_default_calc("jwst", INST, MODE)

report = perform_calculation(calc, dict_report=False)
instrument = report.signal.current_instrument

insconf = InstrumentConfiguration("jwst", INST)
insconf.set_mode(MODE)
for aperture in insconf.apertures:
    insconf.set_aperture(aperture)
    for subarray in insconf.subarrays:
        insconf.set_element("subarray", subarray)
        for readout_pattern in insconf.readout_patterns:
            # now set up the exposure spec
            input_detector = calc["configuration"]["detector"]
            input_detector["readout_pattern"] = readout_pattern
            input_detector["subarray"] = subarray
            detector_name = config_data["aperture_config"][aperture]["detector"]
            instrument.instrument["aperture"] = aperture
            instrument.instrument["readout_pattern"] = readout_pattern
            instrument.instrument["subarray"] = subarray
            detector_config = instrument.read_detector_pars()
            config = {"input_detector": input_detector, "subarray": config_data["subarray_config"], 
                      "readout_pattern_config": config_data["readout_pattern_config"], 
                      "detector_config": detector_config}

            print(f"-------------------------\nJWST {INST} {MODE} {aperture} {subarray} {readout_pattern}\n-------------------------")
            exposure_spec = ExposureSpec_MultiAccum(config)
            find_10000(exposure_spec)
