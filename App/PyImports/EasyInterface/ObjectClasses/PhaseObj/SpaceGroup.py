from typing import Callable

from ..Utils.DictTools import PathDict
from ..Utils.BaseClasses import Base


SG_DETAILS = {
    'crystal_system': {
        'header': 'Crystal system',
        'tooltip': 'The name of the system of geometric crystal classes of space groups (crystal system) to which the space group belongs.',
        'url': 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Ispace_group_crystal_system.html',
        'default': ('', '')
    },
    'space_group_name_HM_alt': {
        'header': 'Symbol',
        'tooltip': 'The Hermann-Mauguin symbol of space group.',
        'url': 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Ispace_group_name_H-M_alt.html',
        'default': ('', '')
    },
    'space_group_IT_number': {
        'header': 'Number',
        'tooltip': 'The number as assigned in International Tables for Crystallography Vol. A.',
        'url': 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Ispace_group_crystal_system.html',
        'default': (0, '')
    },
    'origin_choice': {
        'header': 'Setting',
        'tooltip': '',
        'url': '',
        'default': ('', '')
    }
}


class SpaceGroup(PathDict):
    def __init__(self, crystal_system: Base, space_group_name_HM_alt: Base, space_group_IT_number: Base, origin_choice: Base):
        super().__init__(crystal_system=crystal_system, space_group_name_HM_alt=space_group_name_HM_alt,
                         space_group_IT_number=space_group_IT_number, origin_choice=origin_choice)

        self.setItemByPath(['crystal_system', 'header'], SG_DETAILS['crystal_system']['header'])
        self.setItemByPath(['crystal_system', 'tooltip'], SG_DETAILS['crystal_system']['tooltip'])
        self.setItemByPath(['crystal_system', 'url'], SG_DETAILS['crystal_system']['url'])

        self.setItemByPath(['space_group_name_HM_alt', 'header'], SG_DETAILS['space_group_name_HM_alt']['header'])
        self.setItemByPath(['space_group_name_HM_alt', 'tooltip'], SG_DETAILS['space_group_name_HM_alt']['tooltip'])
        self.setItemByPath(['space_group_name_HM_alt', 'url'], SG_DETAILS['space_group_name_HM_alt']['url'])

        self.setItemByPath(['space_group_IT_number', 'header'], SG_DETAILS['space_group_IT_number']['header'])
        self.setItemByPath(['space_group_IT_number', 'tooltip'], SG_DETAILS['space_group_IT_number']['tooltip'])
        self.setItemByPath(['space_group_IT_number', 'url'], SG_DETAILS['space_group_IT_number']['url'])

        self.setItemByPath(['origin_choice', 'header'], SG_DETAILS['origin_choice']['header'])
        self.setItemByPath(['origin_choice', 'tooltip'], SG_DETAILS['origin_choice']['tooltip'])
        self.setItemByPath(['origin_choice', 'url'], SG_DETAILS['origin_choice']['url'])

    def __repr__(self) -> str:
        return 'SpaceGroup: {} {} '.format(self['space_group_name_HM_alt'], self['origin_choice'])

    @classmethod
    def default(cls) -> 'SpaceGroup':
        crystal_system = Base(*SG_DETAILS['crystal_system']['default'])
        space_group_name_HM_alt = Base(*SG_DETAILS['space_group_name_HM_alt']['default'])
        space_group_IT_number = Base(*SG_DETAILS['space_group_IT_number']['default'])
        origin_choice = Base(*SG_DETAILS['origin_choice']['default'])
        return cls(crystal_system, space_group_name_HM_alt, space_group_IT_number, origin_choice)

    @classmethod
    def fromPars(cls, crystal_system: str, space_group_name_HM_alt: str, space_group_IT_number: int,
                 origin_choice: str) -> 'SpaceGroup':
        crystal_system = Base(crystal_system, SG_DETAILS['crystal_system']['default'][1])
        space_group_name_HM_alt = Base(space_group_name_HM_alt, SG_DETAILS['space_group_name_HM_alt']['default'][1])
        space_group_IT_number = Base(space_group_IT_number, SG_DETAILS['space_group_IT_number']['default'][1])
        origin_choice = Base(origin_choice, SG_DETAILS['origin_choice']['default'][1])

        return cls(crystal_system=crystal_system, space_group_name_HM_alt=space_group_name_HM_alt,
                   space_group_IT_number=space_group_IT_number, origin_choice=origin_choice)
