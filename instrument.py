"""
Instrument specific classes where methods unique to that beamline can be defined,
which can then be used by RunAngle - for example:
set_s3 method can be called but will work differently for say POLREF or INTER
"""
from genie_python import genie as g


# Create an abstract base instrument class
class InstrumentBase:
    """
    Abstract Base class for instrument specific methods.
    """

    def __init__(self, dry_run):
        # TODO: is there any other things we need to pull in upon instantiating
        #  the instrument class?
        self.dry_run = dry_run

    def set_collimation_gaps(self, gap_settings):
        """
        Sets the slit gaps in the collimated direction - i.e. in the direction of Qz
        """
        pass

    def set_beamwidth_gaps(self):
        """
        Sets the slit gaps in the beam width direction - i.e. perpendicular to Qz
        """
        pass

    def r_cset(self, block, block_value):
        """
        Sets any block taking into account the dry_run status
        """
        print(f"{block} set to: {block_value}")
        if not self.dry_run:
            g.cset(block, block_value)


# Base instrument class including methods that can be shared between all beamlines
class Instrument(InstrumentBase):
    """
    Base Instrument class that should include methods that can be shared
    between all beamlines
    e.g. this could be slit calculators, setting software periods etc.
    """

    def set_collimation_gaps(self, gap_settings):
        """
        Sets slits in the collimated direction
        """

        for i, gap in enumerate(gap_settings):
            self.r_cset(f"S{i+1}VG", gap)


class PolrefInstrument(Instrument):
    """
    POLREF Instrument class with methods specific to driving
    the POLREF beamline
    """

    def __init__(self, dry_run):
        super().__init__(dry_run)

        self.vmode = self.is_in_vmode()

    @staticmethod
    def is_in_vmode():

        # TODO: below is for demonstration purposes only
        #  would need to actually pull in the config name
        if g.cget("MODE") == "Vertical":
            return True
        else:
            return False

    def set_collimation_gaps(self, gap_settings):

        for i, gap in enumerate(gap_settings):
            if self.vmode:
                self.r_cset(f"S{i + 1}HG", gap)
            else:
                self.r_cset(f"S{i + 1}VG", gap)
