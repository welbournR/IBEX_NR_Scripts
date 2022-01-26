"""
RunAngle wrappers and classes for running different NR experiments:

RunAngleSL = Solid Liquid
RunAngleAL = Air Liquid
RunAnglePNR = Polarised NR - Air Solid
RunAnglePA = Polarised NR with Analysis - Air Solid

"""

from instrument import init_instrument


class RunAngleBase:
    """
    Abstract base class for RunAngle methods
    """

    # This is just a representative example and is not complete
    def __init__(self, col_slits, width_slits, angle, sample, dry_run=False):
        self.instrument = init_instrument(dry_run)
        self.col_slits = col_slits

    def transmission(self):
        """
        run a transmission
        """
        pass

    def run_angle(self):
        """
        run an NR measurement at a given angle
        """
        pass


class RunAngle(RunAngleBase):
    """
    Most basic form of NR experiment
    """

    def run_angle(self):
        """
        Run NR experiment at a given angle
        """

        # set the collimation slits
        self.instrument.set_collimation_gaps(self.col_slits)


# TODO: Do we want to set up RunAngle with all the methods generic to all
#  NR measurments and subclass that or just work from the abstract base class?
class RunAngleSL(RunAngleBase):
    """
    Solid-Liquid Experiment Class
    """

    def run_angle(self):
        """
        Run NR experiment for a Solid-Liquid cell at a given angle
        """
        
        pass
        

class RunAnglePNR(RunAngleBase):
    """
    Polarised NR Experiment class
    """
    
    def __init__(self, col_slits, width_slits, angle, sample, pol_frames):
        super().__init__(col_slits, width_slits, angle, sample)

        self.pol_frames = pol_frames

    def refl_init(self):
        """
        Initialises beamline for PNR experiment
        """

        self.instrument.pnr_refl_init(**self.pol_frames)

