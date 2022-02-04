"""
RunAngle wrappers and classes for running different NR experiments:

RunAngleSL = Solid Liquid
RunAngleAL = Air Liquid
RunAnglePNR = Polarised NR - Air Solid
RunAnglePA = Polarised NR with Analysis - Air Solid

"""

from refl_instrument import init_instrument


class RunAngleBase:
    """
    Abstract base class for RunAngle methods
    """

    # This is just a representative example and is not complete
    def __init__(self, sample, width_slits,
                 resolution=None, footprint=None,
                 col_slits=None, lowest_angle=None,
                 dry_run=False, instrument=None):

        self.instrument = init_instrument(dry_run, manual_instrument_override=instrument)
        # TODO: make this optional - i.e. if not supplied it should work this out from
        #  the resolution calculator
        self.col_slits = col_slits
        self.width_slits = width_slits
        self.sample = sample

    def transmission(self, angle=None):
        """
        run a transmission with slits based on measurement resolution, footprint
        and measurement angle
        """
        pass

    def run_angle(self, angle):
        """
        run an NR measurement at a given angle
        """
        pass

    def _scale_slits(self, angle):
        """
        Scale collimation slits based on an incident angle
        and/or a resolution or the lowest angle used for a
        given set of collimation slits
        """
        pass

    def calculate_collimation_slits(self):
        """
        Calculates the collimation slits based on resolution, footprint and sample length
        along the beam.
        """
        constants = self.instrument.inst_constants
        pass

    def _divergence_calc(self, a1, a2, x):
        """
        Calculates the angular divergence from a pair of
        slits/appatures for a given distance
        """
        pass


class RunAngle(RunAngleBase):
    """
    Most basic form of NR experiment
    """

    def run_angle(self, angle):
        """
        Run NR experiment at a given angle
        """
        if self.col_slits is not None:
            run_angle_slits = self.col_slits
        else:
            # TODO: Implement resolution calculation method
            # run_angle_slits = self.calculate_collimation_slits()
            pass
        # set the collimation slits
        self.instrument.set_collimation_gaps(self.col_slits)

    def transmission(self, angle=None):
        """
        Run NR transmission with slits based on measurement resolution, footprint
        and measurement angle. If no angle is given, default to collimation slits,
        which should be defined for the lowest angle.
        """

        if angle is None:
            transmission_slits = self.col_slits

        # for demo purposes print something to check the work flow

        print("Running Transmission")


# TODO: Do we want to set up RunAngle with all the methods generic to all
#  NR measurments and subclass that or just work from the abstract base class?
class RunAngleSL(RunAngleBase):
    """
    Solid-Liquid Experiment Class
    """

    def run_angle(self, angle):
        """
        Run NR experiment for a Solid-Liquid cell at a given angle
        """
        
        pass
        

# TODO: add a hasattr check on PolarisedInstrument methods
#  It should fail if trying to be used on a non-polarised instrument
class RunAnglePNR(RunAngleBase):
    """
    Polarised NR Experiment class
    """
    
    def __init__(self, pol_frames, sample, width_slits,
                 resolution=None, footprint=None,
                 col_slits=None, lowest_angle=None,
                 dry_run=False, instrument=None):
        # below grabs the __init__ method from RunAngleBase
        super().__init__(sample, width_slits,
                         resolution, footprint,
                         col_slits, lowest_angle,
                         dry_run, instrument)
        self.pol_frames = pol_frames

    def refl_init(self):
        """
        Initialises beamline for PNR experiment
        """

        self.instrument.pnr_refl_init(**self.pol_frames)

