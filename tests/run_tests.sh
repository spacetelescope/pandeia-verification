cd niriss/
python niriss_sensitivity_soss.py &
python niriss_sensitivity_ami.py &
python niriss_sensitivity_wfss.py &
python niriss_sensitivity_imaging.py
cd ../miri/
python miri_sensitivity_imaging.py &
python miri_sensitivity_imaging_extended.py &
python miri_sensitivity_lrs.py &
python miri_sensitivity_mrs.py
python miri_sensitivity_mrs_extended.py &
cd ../nirspec
python nirspec_sensitivity_fs.py &
python nirspec_sensitivity_ifu.py &
python nirspec_sensitivity_msa.py
cd ../nircam
python nircam_sensitivity_lw.py &
python nircam_sensitivity_sw.py &
python nircam_sensitivity_wfgrism.py
cd ../wfirstimager
python wfirstimager_sensitivity_grism.py &
python wfirstimager_sensitivity_imager.py
