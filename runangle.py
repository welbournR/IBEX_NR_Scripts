"""
RunAngle wrappers and classes for running different NR experiments:

RunAngleSL = Solid Liquid
RunAngleAL = Air Liquid
RunAnglePNR = Polarised NR - Air Solid
RunAnglePA = Polarised NR with Analysis - Air Solid

"""
import warnings

from refl_instrument import init_instrument


class RunAngleBase:
    """
    Abstract base class for RunAngle methods
    """

    # This is just a representative example and is not complete
    def __init__(self, sample, width_slits=None,
                 resolution=None, footprint=None,
                 col_slits=None, lowest_angle=None,
                 angles=None, measurement_times=None,
                 dry_run=False, instrument=None):

        self.instrument = init_instrument(dry_run, manual_instrument_override=instrument)
        # TODO: make this optional - i.e. if not supplied it should work this out from
        #  the resolution calculator
        self.col_slits = col_slits
        # TODO: if these tend to be the same for most measurements on a given
        #  instrument, we should define defaults within the instrument class
        #  so these do not always have to be defined by the user.
        self.width_slits = width_slits
        self.sample = sample

        # TODO: how best should we handle optional arguments?
        #  For now let's just make them class attributes,
        #  regardless of NoneType or not
        self.resolution = resolution
        self.footprint = footprint

        self.lowest_angle = lowest_angle
        self.angles = angles
        self.measurement_times = measurement_times
        # TODO: It might be worth, as part of the instantiation of the class,
        #  outputting a measurement settings file - so the user has a record
        #  of what they set the script to do.
        #  This could be updated when calling run_angle() if settings are modified here.

    def transmission(self, angle=None, measurment_time=None):
        """
        run a transmission with slits based on measurement resolution, footprint
        and measurement angle
        """
        pass

    def run_angle(self, angle, measurement_time):
        """
        run an NR measurement at a given angle
        """
        pass

    def run_all_angles(self):
        """
        If defined on instantiation, this method will call run_angle for a list
        of angles and measurement times
        """

        pass

    def set_measurement_time(self):
        """
        Sets measurment time, based on user definition, or scaling
        based on angle and scale factor
        """

        # if self.measurement_times is not None:
        pass

    def _calculate_measurement_time(self, angle, scale_factor=1):
        """
        This method calculates how long to count each angle for based
        on the count time for the lowest angle and scales based on a user defined
        scale factor and angle:
        measurement_time = lowest_angle_count_time * (angle * scale_factor)

        This is to be used in run_all_angles() helper method
        """
        pass

    def _scale_slit(self, angle, slit, slit_value, minimum_opening, maximum_opening):
        """
        Scale collimation a slit gap or blade based on an incident angle,
        or the lowest angle used for a given set of collimation slit

        :slit_value: is a float value representing a slit gap or blade position

        """

        slit_scale = angle/self.lowest_angle

        scaled_slit = slit_value * slit_scale

        if minimum_opening < scaled_slit < maximum_opening:
            return scaled_slit
        elif scaled_slit < minimum_opening:
            warnings.warn(f"Scaled slit value of {slit}={scaled_slit} is smaller than beamline minimum value\n"
                          f"Setting {slit}={minimum_opening}")
            return minimum_opening
        elif scaled_slit > maximum_opening:
            warnings.warn(f"Scaled slit value of {slit}={scaled_slit} is larger than beamline maximum value\n"
                          f"Setting {slit}={maximum_opening}")
            return maximum_opening

    def calculate_collimation_slits(self, angle):
        """
        Returns the collimation slits based on resolution, footprint and sample length
        along the beam, or if self.col_slits and self.lowest_angle are defined,
        it calculates slits based on a basic scaling of the slits at the lowest angle
        with respect to the angle being measured.
        """
        constants = self.instrument.inst_constants

        slit_settings = {}

        if (self.col_slits is not None) and (self.lowest_angle is not None):
            for slit in self.instrument.slit_aliases.keys():
                # find the max and min limits on the slit openings
                maximum_opening = self.instrument.max_slit_gaps[slit]
                minimum_opening = self.instrument.min_slit_gaps[slit]

                # check to see if we want to scale the slits
                # TODO: this option should be able to be overwritten if required.
                #  We should be calling a class attribute rather than class global.
                if not self.instrument.DEFAULT_DISABLE_SLIT_SCALE_SETTINGS[slit]:
                    if hasattr(self.col_slits[slit], "__len__"):
                        slit_list = []
                        for slit_value in self.col_slits[slit]:
                            # divide max/min by 2 as this is to set the slit blade not the gap
                            slit_list.append(self._scale_slit(angle, slit, slit_value,
                                                              minimum_opening/2, maximum_opening/2))
                        slit_settings[slit] = slit_list
                    else:
                        slit_settings[slit] = self._scale_slit(angle, slit, self.col_slits[slit],
                                                               minimum_opening, maximum_opening)

        if self.footprint is None:
            footprint = self.sample.footprint
        if self.resolution is None:
            resolution = self.sample.resolution
        # TODO: add sample_length to sample class
        # sample_length = self.sample.sample_length
        # TODO: finish writing slit calculator
        # TODO: for sample_length inclusion, use an inequality - i.e.
        #  if footprint > sample_length:
        #      work out S1 using S1Sample and desired resolution
        #  S2 in this case can just be used to set the overilluminated footprint
        #  and should have no effect on the resolution.
        # TODO: work out default and override behaviour for the non-collimation defining slits
        #  e.g. S3 and S4 are XXX % larger than required for desired footprint and resolution.
        #  Additionally, how do we get the
        # TODO: should return at least first two collimation slits e.g. S1 S2
        # TODO: how to deal with other slits that should not be defining the collimation?
        # TODO: how do we specify which slits are our collimation pair?
        #  Generally this will be S1, S2. But for some beamlines with additional slits,
        #  this may be a different selection. We would also need to marry this up with the
        #  slit positions relative to each other and the sample.
        return slit_settings

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

    def run_angle(self, angle, measurement_time):
        """
        Run NR experiment at a given angle
        """
        if self.col_slits is not None:
            run_angle_slits = self.col_slits
        else:
            # TODO: Implement resolution calculation method
            run_angle_slits = self.calculate_collimation_slits()
        # set the collimation slits
        self.instrument.set_collimation_gaps(run_angle_slits)

    def transmission(self, angle=None, measurement_time=None):
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

    def run_angle(self, angle, measurement_time):
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
    
    def __init__(self, pol_frames, sample, width_slits=None,
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

