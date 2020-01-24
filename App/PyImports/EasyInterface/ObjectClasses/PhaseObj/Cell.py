from ..Utils.DictTools import PathDict
from ..Utils.BaseClasses import Base

CELL_DETAILS = {
    'length': {
        'header': '',
        'tooltip': 'Unit-cell length of the selected structure in angstroms.',
        'url': 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Icell_length_.html',
        'default': (3, 'ang')
    },
    'angle': {
        'header': '',
        'tooltip': 'Unit-cell angle of the selected structure in degrees.',
        'url': 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Icell_angle_.html',
        'default': (90, 'deg')
    }
}


class Cell(PathDict):
    """
    Container for crysolagraphic unit cell parameters
    """

    def __init__(self, length_a: Base, length_b: Base, length_c: Base,
                 angle_alpha: Base, angle_beta: Base, angle_gamma: Base):
        """
        Constructor for the crystolographic unit cell
        :param length_a: Unit cell length a
        :param length_b: Unit cell length b
        :param length_c:  Unit cell length c
        :param angle_alpha: Unit cell angle alpha
        :param angle_beta:  Unit cell angle beta
        :param angle_gamma:  Unit cell angle gamma
        """

        super().__init__(length_a=length_a, length_b=length_b, length_c=length_c,
                         angle_alpha=angle_alpha, angle_beta=angle_beta, angle_gamma=angle_gamma)

        self.setItemByPath(['length_a', 'header'], 'a (Å)')
        self.setItemByPath(['length_a', 'tooltip'], CELL_DETAILS['length']['tooltip'])
        self.setItemByPath(['length_a', 'url'], CELL_DETAILS['length']['url'])

        self.setItemByPath(['length_b', 'header'], 'b (Å)')
        self.setItemByPath(['length_b', 'tooltip'], CELL_DETAILS['length']['tooltip'])
        self.setItemByPath(['length_b', 'url'], CELL_DETAILS['length']['url'])

        self.setItemByPath(['length_c', 'header'], 'c (Å)')
        self.setItemByPath(['length_c', 'tooltip'], CELL_DETAILS['length']['tooltip'])
        self.setItemByPath(['length_c', 'url'], CELL_DETAILS['length']['url'])

        self.setItemByPath(['angle_alpha', 'header'], 'alpha (°)')
        self.setItemByPath(['angle_alpha', 'tooltip'], CELL_DETAILS['angle']['tooltip'])
        self.setItemByPath(['angle_alpha', 'url'], CELL_DETAILS['angle']['url'])

        self.setItemByPath(['angle_beta', 'header'], 'beta (°)')
        self.setItemByPath(['angle_beta', 'tooltip'], CELL_DETAILS['angle']['tooltip'])
        self.setItemByPath(['angle_beta', 'url'], CELL_DETAILS['angle']['url'])

        self.setItemByPath(['angle_gamma', 'header'], 'gamma (°)')
        self.setItemByPath(['angle_gamma', 'tooltip'], CELL_DETAILS['angle']['tooltip'])
        self.setItemByPath(['angle_gamma', 'url'], CELL_DETAILS['angle']['url'])

    @classmethod
    def default(cls) -> 'Cell':
        """
        Default constructor for a crystolographic unit cell
        :return: Default crystolographic unit cell container
        """
        length_a = Base(*CELL_DETAILS['length']['default'])
        length_b = Base(*CELL_DETAILS['length']['default'])
        length_c = Base(*CELL_DETAILS['length']['default'])
        angle_alpha = Base(*CELL_DETAILS['angle']['default'])
        angle_beta = Base(*CELL_DETAILS['angle']['default'])
        angle_gamma = Base(*CELL_DETAILS['angle']['default'])
        return cls(length_a, length_b, length_c, angle_alpha, angle_beta, angle_gamma)

    @classmethod
    def fromPars(cls, length_a: float, length_b: float, length_c: float,
                 angle_alpha: float, angle_beta: float, angle_gamma: float) -> 'Cell':
        """
        Constructor of a crystolographic unit cell when parameters are known
        :param length_a: Unit cell length a
        :param length_b: Unit cell length b
        :param length_c:  Unit cell length c
        :param angle_alpha: Unit cell angle alpha
        :param angle_beta:  Unit cell angle beta
        :param angle_gamma:  Unit cell angle gamma
        :return:
        """
        length_a = Base(length_a, CELL_DETAILS['length']['default'][1])
        length_b = Base(length_b, CELL_DETAILS['length']['default'][1])
        length_c = Base(length_c, CELL_DETAILS['length']['default'][1])
        angle_alpha = Base(angle_alpha, CELL_DETAILS['angle']['default'][1])
        angle_beta = Base(angle_beta, CELL_DETAILS['angle']['default'][1])
        angle_gamma = Base(angle_gamma, CELL_DETAILS['angle']['default'][1])

        return cls(length_a=length_a, length_b=length_b, length_c=length_c,
                   angle_alpha=angle_alpha, angle_beta=angle_beta, angle_gamma=angle_gamma)

    def __repr__(self) -> str:
        return 'Cell: (a:{}, b:{}, c:{}, alpha:{}, beta:{}, gamma:{}) '.format(self['length_a'], self['length_b'],
                                                                               self['length_c'],
                                                                               self['angle_alpha'], self['angle_beta'],
                                                                               self['angle_gamma'])
