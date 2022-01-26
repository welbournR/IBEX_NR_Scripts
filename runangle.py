"""
RunAngle wrappers and classes for running different NR experiments:

RunAngleSL = Solid Liquid
RunAngleAL = Air Liquid
RunAnglePNR = Polarised NR - Air Solid
RunAnglePA = Polarised NR with Analysis - Air Solid

"""

from instrument import initialise_instrument


class RunAngleBase:
    """
    Abstract base class for RunAngle methods
    """

    # This is just a representative example and is not complete
    def __init__(self, col_slits, width_slits, angle, sample, dry_run=False):
        self.instrument = initialise_instrument(dry_run)
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
        