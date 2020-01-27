from typing import Union

import numpy as np

from ..Utils.DictTools import PathDict
from ..Utils.BaseClasses import Base

EXPERIMENT_DETAILS = {
    'wavelength': {
        'header': 'χ²',
        'tooltip': 'Goodness of fit as estimated by the Pearson''s chi-squared test.',
        'url': 'https://en.wikipedia.org/wiki/Chi-squared_test',
        'default': (0, '')
    },
    'offset': {
        'header': '',
        'tooltip': 'Number of free parameters.',
        'url': '',
        'default': (0, '')
    }
}

RESOLUTION_DETAILS = {
    'UVWXY': {
        'header': '',
        'tooltip': '',
        'url': '',
        'default': (0, '')
    }
}

SCALE_DETAILS = {
    'scale': {
        'header': '',
        'tooltip': '',
        'url': '',
        'default': (1, '')
    }
}

INTENSITY_DETAILS = {
    'intensity': {
        'header': '',
        'tooltip': '',
        'url': '',
        'default': (None, '')
    }
}


class Resolution(PathDict):
    """
    Data store for the resolution parameters
    """
    def __init__(self, u: Base, v: Base, w: Base, x: Base, y: Base):
        """
        Dictionary store for resolution parameters
        :param u: resolution parameter u
        :param v: resolution parameter v
        :param w:  resolution parameter w
        :param x:  resolution parameter x
        :param y:  resolution parameter y
        """
        super().__init__(u=u, v=v, w=w, x=x, y=y)

        self.setItemByPath(['u', 'header'], RESOLUTION_DETAILS['UVWXY']['header'])
        self.setItemByPath(['u', 'tooltip'], RESOLUTION_DETAILS['UVWXY']['tooltip'])
        self.setItemByPath(['u', 'url'], RESOLUTION_DETAILS['UVWXY']['url'])

        self.setItemByPath(['v', 'header'], RESOLUTION_DETAILS['UVWXY']['header'])
        self.setItemByPath(['v', 'tooltip'], RESOLUTION_DETAILS['UVWXY']['tooltip'])
        self.setItemByPath(['v', 'url'], RESOLUTION_DETAILS['UVWXY']['url'])

        self.setItemByPath(['w', 'header'], RESOLUTION_DETAILS['UVWXY']['header'])
        self.setItemByPath(['w', 'tooltip'], RESOLUTION_DETAILS['UVWXY']['tooltip'])
        self.setItemByPath(['w', 'url'], RESOLUTION_DETAILS['UVWXY']['url'])

        self.setItemByPath(['x', 'header'], RESOLUTION_DETAILS['UVWXY']['header'])
        self.setItemByPath(['x', 'tooltip'], RESOLUTION_DETAILS['UVWXY']['tooltip'])
        self.setItemByPath(['x', 'url'], RESOLUTION_DETAILS['UVWXY']['url'])

        self.setItemByPath(['y', 'header'], RESOLUTION_DETAILS['UVWXY']['header'])
        self.setItemByPath(['y', 'tooltip'], RESOLUTION_DETAILS['UVWXY']['tooltip'])
        self.setItemByPath(['y', 'url'], RESOLUTION_DETAILS['UVWXY']['url'])

    @classmethod
    def default(cls) -> 'Resolution':
        """
        Default constructor for the resolution dict
        :return: Default resolution dict
        """
        u = Base(*RESOLUTION_DETAILS['UVWXY']['default'])
        v = Base(*RESOLUTION_DETAILS['UVWXY']['default'])
        w = Base(*RESOLUTION_DETAILS['UVWXY']['default'])
        x = Base(*RESOLUTION_DETAILS['UVWXY']['default'])
        y = Base(*RESOLUTION_DETAILS['UVWXY']['default'])
        return cls(u, v, w, x, y)

    @classmethod
    def fromPars(cls, u: float, v: float, w: float, x: float, y: float) -> 'Resolution':
        """
        Constructor when resolution parameters are known
        :param u: resolution parameter u
        :param v: resolution parameter v
        :param w: resolution parameter w
        :param x: resolution parameter x
        :param y: resolution parameter y
        :return: Resolution dictionary with values set
        """
        u = Base(u, RESOLUTION_DETAILS['UVWXY']['default'][1])
        v = Base(v, RESOLUTION_DETAILS['UVWXY']['default'][1])
        w = Base(w, RESOLUTION_DETAILS['UVWXY']['default'][1])
        x = Base(x, RESOLUTION_DETAILS['UVWXY']['default'][1])
        y = Base(y, RESOLUTION_DETAILS['UVWXY']['default'][1])
        return cls(u, v, w, x, y)

    def __repr__(self) -> str:
        return 'u: {}, v: {}, w: {}, x: {}, y:{}'.format(self['u'].value, self['v'].value, self['w'].value,
                                                         self['x'].value, self['y'].value)


class Background(PathDict):
    """
    Data store for the background data parameters
    """
    def __init__(self, ttheta: float, intensity: Base):
        """
        Background dictionary
        :param ttheta: Two Theta angle in degrees
        :param intensity: Intensity data store
        :return: Background data object
        """
        super().__init__(ttheta=ttheta, intensity=intensity)
        self.setItemByPath(['intensity', 'header'], INTENSITY_DETAILS['intensity']['header'])
        self.setItemByPath(['intensity', 'tooltip'], INTENSITY_DETAILS['intensity']['tooltip'])
        self.setItemByPath(['intensity', 'url'], INTENSITY_DETAILS['intensity']['url'])

    @classmethod
    def default(cls) -> 'Background':
        """
        Default constructor for a background point
        :return: Default background data object
        """
        ttheta = 0
        intensity = Base(*INTENSITY_DETAILS['intensity']['default'])
        return cls(ttheta, intensity)

    @classmethod
    def fromPars(cls, ttheta: float, intensity: float) -> 'Background':
        """
        Constructor for background when two theta and intensity are known
        :param ttheta: Two Theta angle in degrees
        :param intensity: Value for intensity
        :return: Background data dict
        """
        intensity = Base(intensity, INTENSITY_DETAILS['intensity']['default'][1])
        return cls(ttheta, intensity)

    def __repr__(self) -> str:
        return ''.format(self['ttheta'], self['intensity'].value)


class Backgrounds(PathDict):
    """
    Store for a collection of background points
    """
    def __init__(self, backgrounds: Union[Background, dict, list]):
        """
        Constructor for Background data points
        :param backgrounds: Background parameters formed from Background dicts
        """
        if isinstance(backgrounds, Background):
            backgrounds = {
                str(backgrounds['ttheta']): backgrounds,
            }
        if isinstance(backgrounds, list):
            theseBackgrounds = dict()
            for background in backgrounds:
                theseBackgrounds[str(background['ttheta'])] = background
            backgrounds = theseBackgrounds
        super().__init__(**backgrounds)

    def __repr__(self):
        return '{} Backgrounds'.format(len(self))


class MeasuredPattern(PathDict):
    """
    Storage container for measured patterns
    """
    def __init__(self, x: list, y_obs: list, sy_obs: list, y_obs_up: Union[list, None], sy_obs_up: Union[list, None],
                 y_obs_down: Union[list, None], sy_obs_down: Union[list, None]):
        """
        Constructor for a measured pattern
        :param x: Generally a two theta value
        :param y_obs: Observed intensity
        :param sy_obs: Observed Error
        :param y_obs_up: Polarised UP intensity. None if non-polarised
        :param sy_obs_up: Polarised UP intensity error. None if non-polarised
        :param y_obs_down: Polarised DOWN intensity. None if non-polarised
        :param sy_obs_down: Polarised DOWN intensity error. None if non-polarised
        """
        super().__init__(x=x, y_obs=y_obs, sy_obs=sy_obs, y_obs_up=y_obs_up, sy_obs_up=sy_obs_up, y_obs_down=y_obs_down,
                         sy_obs_down=sy_obs_down)

    @property
    def isPolarised(self) -> bool:
        """
        Is the measured data of a polarised type?
        :return: True if it is from a polarised measurement, false otherwise
        """
        if self['y_obs_up'] is None:
            return False
        else:
            return True

    @property
    def y_obs_upper(self) -> list:
        """
        Upper data confidence bound
        :return: value of upper confidence bound
        """
        return (np.array(self['y_obs']) + np.array(self['sy_obs'])).tolist()

    @property
    def y_obs_lower(self) -> list:
        """
        Lower data confidence bound
        :return: value of lower confidence bound
        """
        return (np.array(self['y_obs']) - np.array(self['sy_obs'])).tolist()

    @classmethod
    def default(cls, polarised: bool = False):
        """
        Default constructor for measured data container
        :param polarised: Should the container be initialised as a polarised data container?
        :return: Empty data container
        """
        x = []
        y_obs = []
        sy_obs = []
        y_obs_up = None
        sy_obs_up = None
        y_obs_down = None
        sy_obs_down = None
        if polarised:
            y_obs_up = []
            sy_obs_up = []
            y_obs_down = []
            sy_obs_down = []
        return cls(x, y_obs, sy_obs, y_obs_up, sy_obs_up, y_obs_down, sy_obs_down)


class ExperimentPhase(PathDict):
    """
    Storage container for the ExperiemntalPhase details
    """
    def __init__(self, scale: Base):
        """
        Constructor for the Experimental phase container
        :param scale: phase scale as data object
        """
        super().__init__(scale=scale)
        self.setItemByPath(['scale', 'header'], SCALE_DETAILS['scale']['header'])
        self.setItemByPath(['scale', 'tooltip'], SCALE_DETAILS['scale']['tooltip'])
        self.setItemByPath(['scale', 'url'], SCALE_DETAILS['scale']['url'])

    @classmethod
    def default(cls) -> 'ExperimentPhase':
        """
        Default experimental phase data container
        :return: Default experimental phase data container
        """
        scale = Base(*SCALE_DETAILS['scale']['default'])
        return cls(scale)

    @classmethod
    def fromPars(cls, scale: float) -> 'ExperimentPhase':
        """
        Parameter initialised experimental phase data container
        :return: Set experimental phase data container
        """
        scale = Base(scale, SCALE_DETAILS['scale']['default'][1])
        return cls(scale)


class Experiment(PathDict):
    """
    Experimental details data container
    """
    def __init__(self, name: str, wavelength: Base, offset: Base, phase: ExperimentPhase, background: Backgrounds,
                 resolution: Resolution, measured_pattern: MeasuredPattern):
        """
        Constructor for experimental data container
        :param name: The name of the experimental data
        :param wavelength: What wavelength was the experiment taken at
        :param offset: The experimental offset
        :param phase: The experimental phase scale
        :param background: Description of the background
        :param resolution: Description of the resolution
        :param measured_pattern: What was actually measured
        """
        super().__init__(name=name, wavelength=wavelength, offset=offset, phase=phase, background=background,
                         resolution=resolution, measured_pattern=measured_pattern)

    @classmethod
    def default(cls, name: str) -> 'Experiment':
        """
        Default constructor for an Experiment
        :param name: What the experiment should be called
        :return: Default empty experiment
        """
        wavelength = Base(*EXPERIMENT_DETAILS['wavelength']['default'])
        offset = Base(*EXPERIMENT_DETAILS['offset']['default'])
        phase = ExperimentPhase.default()
        backgrounds = Backgrounds(Background.default())
        resolution = Resolution.default()
        measured_pattern = MeasuredPattern.default()
        return cls(name, wavelength, offset, phase, backgrounds, resolution, measured_pattern)

    @classmethod
    def fromPars(cls, name: str, wavelength: float, offset: float, scale: float, background: Backgrounds, resolution: Resolution,
                 measured_pattern: MeasuredPattern) -> 'Experiment':
        """
        Constructor of experiment from parameters
        :param name: What the experiment should be called
        :param wavelength: Experimental wavelength
        :param offset: Experimental offset
        :param scale: Scale parameter
        :param background: Background model
        :param resolution: Resolution model
        :param measured_pattern: The Measured data
        :return: Experiemnt from parameters
        """
        wavelength = Base(wavelength, EXPERIMENT_DETAILS['wavelength']['default'][1])
        offset = Base(offset, EXPERIMENT_DETAILS['offset']['default'][1])
        phase = ExperimentPhase.fromPars(scale)
        return cls(name, wavelength, offset, phase, background, resolution, measured_pattern)


class Experiments(PathDict):
    """
    Container for multiple experiments
    """
    def __init__(self, experiments: Union[Experiment, dict, list]):
        """
        Constructor for holding multiple experiments
        :param experiments: A collection of experimental dicts
        """
        if isinstance(experiments, Experiment):
            experiments = {
                experiments['name']: experiments,
            }
        if isinstance(experiments, list):
            theseExperiments = dict()
            for experiment in experiments:
                theseExperiments[experiment['name']] = experiment
            experiments = theseExperiments
        super().__init__(**experiments)

    def __repr__(self) -> str:
        return '{} Experiments'.format(len(self))
