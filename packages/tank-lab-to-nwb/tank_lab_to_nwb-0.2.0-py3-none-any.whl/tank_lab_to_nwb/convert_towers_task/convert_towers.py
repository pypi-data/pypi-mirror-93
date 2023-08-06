"""Authors: Alessio Buccino, Cody Baker, Szonja Weigl, and Ben Dichter."""
from pathlib import Path
from isodate import duration_isoformat
from datetime import timedelta, datetime

from tank_lab_to_nwb import TowersNWBConverter

# Point to the base folder path for both recording data and Virmen
base_path = Path("D:/Neuropixels/")

# Name the NWBFile and point to the desired save path
nwbfile_path = base_path / "FullTesting.nwb"

# Point to the various files for the conversion
recording_folder = base_path / "ActualData" / "2021_01_15_E105" / "towersTask_g0" / "towersTask_g0_imec0"
raw_data_file = recording_folder / "towersTask_g0_t0.imec0.ap.bin"
raw_data_lfp_file = recording_folder / "towersTask_g0_t0.imec0.lf.bin"
virmen_file_path = base_path / "ActualData" / "behavior" / "PoissonBlocksReboot4_cohort4_NPX_testuser_T25_T_20210115.mat"
spikesorted_file_path = base_path / "Example.nwb"

# Enter Session and Subject information here - uncomment any fields you want to include
session_description = "Enter session description here."
session_start = datetime(1970, 1, 1)  # (Year, Month, Day)

subject_info = dict(
    description="Enter optional subject description here",
    # weight="Enter subject weight here",
    # age=duration_isoformat(timedelta(days=0)),  # Enter the age of the subject in days
    # species="Mus musculus",
    # genotype="Enter subject genotype here",
    # sex="Enter subject sex here"
)

# Set some global conversion options here
stub_test = True



# Run the conversion
source_data = dict(
    SpikeGLXRecording=dict(file_path=str(raw_data_file)),
    SpikeGLXLFP=dict(file_path=str(raw_data_lfp_file)),
    VirmenData=dict(file_path=str(virmen_file_path))
)
conversion_options = dict(
    SpikeGLXRecording=dict(stub_test=stub_test),
    SpikeGLXLFP=dict(stub_test=stub_test)
)
converter = TowersNWBConverter(
    source_data=source_data,
    ttl_source=recording_folder / ".." / "towersTask_g0_t0.nidq.bin"
)
metadata = converter.get_metadata()
metadata['NWBFile'].update(session_description=session_description)
metadata['Subject'].update(subject_info)
converter.run_conversion(
    nwbfile_path=str(nwbfile_path),
    metadata=metadata,
    conversion_options=conversion_options,
    overwrite=True
)
