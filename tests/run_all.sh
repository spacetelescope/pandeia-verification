#!/bin/bash
# https://stackoverflow.com/questions/18622907/only-mkdir-if-it-does-not-exist
mkdir -p ../logs
mkdir -p ../outputs
cd niriss/
python niriss_sensitivity_soss.py > ../../logs/niriss_soss.log &
python niriss_sensitivity_wfss.py > ../../logs/niriss_wfss.log &
cd ../miri/
python miri_sensitivity_mrs.py > ../../logs/miri_mrs.log &
cd ../nirspec
python nirspec_sensitivity_ifu.py > ../../logs/nirspec_ifu.log &
cd ../niriss/
python niriss_sensitivity_ami.py > ../../logs/niriss_ami.log
python niriss_sensitivity_imaging.py > ../../logs/niriss_imaging.log
cd ../miri/
python miri_sensitivity_imaging.py > ../../logs/miri_imaging.log
python miri_sensitivity_imaging_extended.py > ../../logs/miri_imaging_extended.log
python miri_sensitivity_mrs_extended.py > ../../logs/miri_mrs_extended.log 
python miri_sensitivity_lrs.py > ../../logs/miri_lrs.log
cd ../nirspec
python nirspec_sensitivity_fs.py > ../../logs/nirspec_fs.log
python nirspec_sensitivity_msa.py > ../../logs/nirspec_msa.log
cd ../nircam
python nircam_sensitivity_lw.py > ../../logs/nircam_lw.log
python nircam_sensitivity_sw.py > ../../logs/nircam_sw.log
python nircam_sensitivity_wfgrism.py > ../../logs/nircam_wfgrism.log
cd ../wfi
python wfi_sensitivity_spectroscopy.py > ../../logs/wfi_spectroscopy.log
python wfi_sensitivity_imaging.py > ../../logs/wfi_imaging.log
