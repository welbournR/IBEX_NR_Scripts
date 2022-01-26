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


class InterInstrument(Instrument):
    """
    INTER Instrument class with methods specific to driving
    the INTER beamline
    """


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

    def flipper(self, state, flipper_settings=None):
        """
        Sets flipper to desired settings and state
        """

        # TODO: don't want these hard coded here. We should pull them from a local
        #  file on the POLREF instrument - maybe placed in "inst" scripts
        #  Look to open a .json with values placed in it.
        default_ops = dict(amp_p=3.5,
                           comp_p=1.023,
                           const_p=0.0298,
                           dt_p=-3250,
                           file_p=None,
                           amp_a=3.5,
                           comp_a=1.234,
                           const_a=0.042,
                           dt_a=-3250,
                           file_a=None)

        if flipper_settings is not None:
            for k in default_ops.keys():
                default_ops[k] = flipper_settings.get(k, default_ops[k])
        else:
            flipper_settings = default_ops

        self.r_cset(b.Polariser_Amp, flipper_settings["amp_p"])

        # see polref base_routines for setting flipper state
        # below is just for representation
        self.r_cset(b.Flipper_State, state)

    def hardperiods_pnr(self, uframes=1, dframes=1):
        """
        Set the hardware periods for pnr mode
        Args:
            uframes: Pol flipper off frame count
            dframes: Pol flipper on frame count
        """

        pass

    def pnr_refl_init(self, uframes=None, dframes=None):
        """
        Initialises POLREF for PNR experiment
        """

        self.flipper("dd")
        self.hardperiods_pnr(uframes, dframes)
        pass


# TODO: Include a better way of passing multiple variables
#  which could be RunAngle type specific, to the instrument
#  instantiaion. **kwargs may be best in conjunction
#  with hasattr statements
def init_instrument(dry_run):
    """
    Grabs instrument from IBEX (using the config?)
    and instantiates correct instrument class.

    If instrument is unknown (or we do not have a class written for it yet)
    it will default to generic Instrument class
    """

    # below grabs the instrument name from the pv so IN:POLREF: would return POLREF
    instrument_name = g.my_pv_prefix.split(":")[1]

    # TODO: the if statement below can be done more cleanly
    #  - need to look into this
    if instrument_name == "INTER":
        instrument = InterInstrument(dry_run=dry_run)
    elif instrument_name == "POLREF":
        instrument = PolrefInstrument(dry_run=dry_run)
    else:
        instrument = Instrument(dry_run=dry_run)

    return instrument
