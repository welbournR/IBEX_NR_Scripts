"""
Example user run_angle script using new architecture.
Also demonstrates different methods to create the script for discussion
"""

import runangle as ra
import sample as samp

# TODO: make a check_script() or something similar function.
#  Idea here is to run this before running your script and it saves out
#  to some text file, a list of all of the measurement settings for
#  each run_angle() and transmission call - this would include:
#  Angles, slits settings etc.
# create a sample object
# we can create this either by directly writing the kwargs into the call:
sample_1 = samp.SampleGenerator(
                                translation=0,
                                height2_offset=0,
                                phi_offset=0,
                                psi_offset=0,
                                height_offset=0,
                                resolution=0.03,
                                footprint=50,
                                title="Block 1",
                                subtitle="Sample 1"
                                )

# or by defining a dict and loading that into the call:
sample_2_info = dict(
                     translation=0,
                     height2_offset=0,
                     phi_offset=0,
                     psi_offset=0,
                     height_offset=0,
                     resolution=0.03,
                     footprint=50,
                     title="Block 2",
                     subtitle="Sample 2"
                     )
sample_2 = samp.SampleGenerator(**sample_2_info)

# define some slit settings - for now we will directly pass them just for demo purposes
# but this should be delt with by the resolution calculator
# TODO: we should decide if we want to pass the slit settings as a list or dict
#  at the moment it expects a list, in order, of S1, S2, S3 etc.
col_slits = dict(S1=0.5, S2=0.25, S3=5)
width_slits = [40, 30, 30]
# TODO: we need to decide how we want RunAngle to be used
# run a measurement - this can just be set at the start of the script
sample_1_measure = ra.RunAngle(col_slits=col_slits, width_slits=width_slits, sample=sample_1)
# if we want to remove the "." we can hook a name to the method
run_sample_1 = sample_1_measure.run_angle
sample_1_transmission = sample_1_measure.transmission


# create function so IBEX knows when to start the script
def run_script():
    # transmission - currently no optional arguments just for demo purposes
    sample_1_transmission(angle=0.5, measurement_time=5)
    # theta = 0.5
    run_sample_1(angle=0.5, measurement_time=5)
