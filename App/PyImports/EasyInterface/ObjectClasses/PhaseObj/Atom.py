from typing import Union

from ..Utils.DictTools import PathDict
from ..Utils.BaseClasses import Base

ATOM_DETAILS = {
    'type_symbol': {
        'header': 'Atom',
        'tooltip': 'A code to identify the atom species occupying this site.',
        'url': 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_type_symbol.html',
        'default': (None, '')
    },
    'fract': {
        'header': 'Atom',
        'tooltip': 'Atom-site coordinate as fractions of the unit cell length.',
        'url': 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_fract_.html',
        'default': (None, 'frac')
    },
    'occupancy': {
        'header': 'Occupancy',
        'tooltip': 'The fraction of the atom type present at this site.',
        'url': 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_occupancy.html',
        'default': (1, 'frac')
    },
    'adp_type': {
        'header': 'Type',
        'tooltip': 'A standard code used to describe the type of atomic displacement parameters used for the site.',
        'url': 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_adp_type.html',
        'default': (None, '')
    },
    'U_iso_or_equiv': {
        'header': 'Biso',
        'tooltip': 'Isotropic atomic displacement parameter, or equivalent isotropic atomic displacement parameter, '
                   'B(equiv), in angstroms squared.',
        'url': 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_B_iso_or_equiv.html',
        'default': (None, 'ang^2')
    },
    'scat_length_neutron': {
        'header': 'Neutron Scattering Length',
        'tooltip': 'The bound coherent scattering length in femtometres for the atom type at the isotopic composition '
                   'used for the diffraction experiment.',
        'url': 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_type_scat_length_neutron.html',
        'default': (None, 'fm')
    },
    'ADP': {
        'header': '',
        'tooltip': 'Anisotropic atomic displacement component in angstroms squared.',
        'url': 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_aniso_U_.html',
        'default': (None, 'ang^2')
    },
    'MSP': {
        'header': '',
        'tooltip': '',
        'url': '',
        'default': (None, 'T^-1')
    }
}


class Atom(PathDict):
    """
    Storage for details about an atom
    """

    def __init__(self, atom_site_label: str, type_symbol: Base, scat_length_neutron: Base,
                 fract_x: Base, fract_y: Base, fract_z: Base, occupancy, adp_type, U_iso_or_equiv: Base,
                 ADp: 'ADP', MSp: 'MSP'):
        """
        Constructor for an atom
        :param atom_site_label: The unique name of the atom in the phase
        :param type_symbol: The type of atom
        :param scat_length_neutron: Neutron scattering length
        :param fract_x: X position
        :param fract_y: Y position
        :param fract_z: Z position
        :param occupancy: Site occupancy
        :param adp_type: ADP type code
        :param U_iso_or_equiv: Isotropic atomic displacement parameter
        :param ADP: Data store for Atom site anisotropic displacement parameters
        :param MSP: Data store for Atom site magnetic susceptibility parameters
        """
        super().__init__(atom_site_label=atom_site_label, type_symbol=type_symbol,
                         scat_length_neutron=scat_length_neutron, fract_x=fract_x, fract_y=fract_y, fract_z=fract_z,
                         occupancy=occupancy, adp_type=adp_type, U_iso_or_equiv=U_iso_or_equiv, ADP=ADp, MSP=MSp)

        self.setItemByPath(['type_symbol', 'header'], ATOM_DETAILS['type_symbol']['header'])
        self.setItemByPath(['type_symbol', 'tooltip'], ATOM_DETAILS['type_symbol']['tooltip'])
        self.setItemByPath(['type_symbol', 'url'], ATOM_DETAILS['type_symbol']['url'])

        self.setItemByPath(['scat_length_neutron', 'header'], ATOM_DETAILS['scat_length_neutron']['header'])
        self.setItemByPath(['scat_length_neutron', 'tooltip'], ATOM_DETAILS['scat_length_neutron']['tooltip'])
        self.setItemByPath(['scat_length_neutron', 'url'], ATOM_DETAILS['scat_length_neutron']['url'])

        self.setItemByPath(['fract_x', 'header'], 'x')
        self.setItemByPath(['fract_x', 'tooltip'], ATOM_DETAILS['fract']['tooltip'])
        self.setItemByPath(['fract_x', 'url'], ATOM_DETAILS['fract']['url'])

        self.setItemByPath(['fract_y', 'header'], 'y')
        self.setItemByPath(['fract_y', 'tooltip'], ATOM_DETAILS['fract']['tooltip'])
        self.setItemByPath(['fract_y', 'url'], ATOM_DETAILS['fract']['url'])

        self.setItemByPath(['fract_z', 'header'], 'z')
        self.setItemByPath(['fract_z', 'tooltip'], ATOM_DETAILS['fract']['tooltip'])
        self.setItemByPath(['fract_z', 'url'], ATOM_DETAILS['fract']['url'])

        self.setItemByPath(['occupancy', 'header'], ATOM_DETAILS['occupancy']['header'])
        self.setItemByPath(['occupancy', 'tooltip'], ATOM_DETAILS['occupancy']['tooltip'])
        self.setItemByPath(['occupancy', 'url'], ATOM_DETAILS['occupancy']['url'])

        self.setItemByPath(['adp_type', 'header'], ATOM_DETAILS['adp_type']['header'])
        self.setItemByPath(['adp_type', 'tooltip'], ATOM_DETAILS['adp_type']['tooltip'])
        self.setItemByPath(['adp_type', 'url'], ATOM_DETAILS['adp_type']['url'])

        self.setItemByPath(['U_iso_or_equiv', 'header'], ATOM_DETAILS['U_iso_or_equiv']['header'])
        self.setItemByPath(['U_iso_or_equiv', 'tooltip'], ATOM_DETAILS['U_iso_or_equiv']['tooltip'])
        self.setItemByPath(['U_iso_or_equiv', 'url'], ATOM_DETAILS['U_iso_or_equiv']['url'])

    def __repr__(self) -> str:
        return 'Atom {}'.format(self['type_symbol'])

    def __str__(self) -> str:
        return 'Atom {}: x = {}, y = {}, z = {}'.format(self['type_symbol'],
                                                        self['fract_x'], self['fract_y'], self['fract_z'])

    @classmethod
    def default(cls, atom_site_label: str) -> 'Atom':
        """
        Default constructor for an atom given a unique name in the phase
        :param atom_site_label: The atoms unique name in the phase
        :return: Default atom with a given name
        """
        type_symbol = Base(*ATOM_DETAILS['type_symbol']['default'])
        scat_length_neutron = Base(*ATOM_DETAILS['scat_length_neutron']['default'])
        fract_x = Base(*ATOM_DETAILS['fract']['default'])
        fract_y = Base(*ATOM_DETAILS['fract']['default'])
        fract_z = Base(*ATOM_DETAILS['fract']['default'])
        occupancy = Base(*ATOM_DETAILS['occupancy']['default'])
        adp_type = Base(*ATOM_DETAILS['adp_type']['default'])
        U_iso_or_equiv = Base(*ATOM_DETAILS['U_iso_or_equiv']['default'])
        ADp = ADP.default()
        MSp = MSP.default()

        return cls(atom_site_label, type_symbol, scat_length_neutron, fract_x, fract_y, fract_z,
                   occupancy, adp_type, U_iso_or_equiv, ADp, MSp)

    @classmethod
    def fromXYZ(cls, atom_site_label: str, type_symbol: str, x: float, y: float, z: float) -> 'Atom':
        """
        Construct an atom from name, type and position
        :param atom_site_label: The atoms unique name in the phase
        :param type_symbol: The type of atom
        :param x: X position
        :param y: Y position
        :param z: Z position
        :return: Atom with name type and position filled in
        """
        obj = cls.default(atom_site_label)
        obj.setItem('type_symbol', Base(type_symbol, ATOM_DETAILS['type_symbol']['default'][1]))
        obj.setItem('fract_x', Base(x, ATOM_DETAILS['fract']['default'][1]))
        obj.setItem('fract_y', Base(y, ATOM_DETAILS['fract']['default'][1]))
        obj.setItem('fract_z', Base(z, ATOM_DETAILS['fract']['default'][1]))
        return obj

    @classmethod
    def fromPars(cls, atom_site_label: str, type_symbol: str, scat_length_neutron: float,
                 fract_x: float, fract_y: float, fract_z: float, occupancy: float, adp_type: str,
                 U_iso_or_equiv: float, ADp: list = None, MSp: list = None) -> 'Atom':
        """
        Atom constructor from parameters
        :param atom_site_label: The unique name of the atom in the phase
        :param type_symbol: The type of atom
        :param scat_length_neutron: Neutron scattering length
        :param fract_x: X position
        :param fract_y: Y position
        :param fract_z: Z position
        :param occupancy: Site occupancy
        :param adp_type: ADP type code
        :param U_iso_or_equiv: Isotropic atomic displacement parameter
        :return: Fully formed atom data store
        """
        type_symbol = Base(type_symbol, ATOM_DETAILS['type_symbol']['default'][1])
        scat_length_neutron = Base(scat_length_neutron, ATOM_DETAILS['scat_length_neutron']['default'][1])
        occupancy = Base(occupancy, ATOM_DETAILS['occupancy']['default'][1])
        adp_type = Base(adp_type, ATOM_DETAILS['adp_type']['default'][1])
        U_iso_or_equiv = Base(U_iso_or_equiv, ATOM_DETAILS['U_iso_or_equiv']['default'][1])
        fract_x = Base(fract_x, ATOM_DETAILS['fract']['default'][1])
        fract_y = Base(fract_y, ATOM_DETAILS['fract']['default'][1])
        fract_z = Base(fract_z, ATOM_DETAILS['fract']['default'][1])

        if not isinstance(ADp, ADP):
            if ADp is not None:
                ADp = ADP.fromPars(*ADp)
            else:
                ADp = ADP.default()

        if not isinstance(MSp, MSP):
            if MSp is not None:
                MSp = MSP.fromPars(*MSp)
            else:
                MSp = MSP.default()

        return cls(atom_site_label, type_symbol, scat_length_neutron, fract_x, fract_y, fract_z,
                   occupancy, adp_type, U_iso_or_equiv, ADp, MSp)


class Atoms(PathDict):
    """
    Container for multiple atoms
    """

    def __init__(self, atoms: Union[Atom, dict, list]):
        """
        Constructor for multiple atoms
        :param atoms: Collection of atoms
        """
        if isinstance(atoms, Atom):
            atoms = {
                atoms['atom_site_label']: atoms,
            }
        if isinstance(atoms, list):
            theseAtoms = dict()
            for atom in atoms:
                theseAtoms[atom['atom_site_label']] = atom
            atoms = theseAtoms

        super().__init__(**atoms)

    def __repr__(self) -> str:
        return '{} Atoms'.format(len(self))


class ADP(PathDict):
    """
    Data store for Atom site anisotropic displacement parameters
    """
    def __init__(self,
                 u_11: Base, u_22: Base, u_33: Base,
                 u_12: Base, u_13: Base, u_23: Base):
        super().__init__(u_11=u_11, u_22=u_22, u_33=u_33,
                         u_12=u_12, u_13=u_13, u_23=u_23)

        self.setItemByPath(['u_11', 'header'], 'U11')
        self.setItemByPath(['u_11', 'tooltip'], ATOM_DETAILS['ADP']['tooltip'])
        self.setItemByPath(['u_11', 'url'], ATOM_DETAILS['ADP']['url'])

        self.setItemByPath(['u_12', 'header'], 'U12')
        self.setItemByPath(['u_12', 'tooltip'], ATOM_DETAILS['ADP']['tooltip'])
        self.setItemByPath(['u_12', 'url'], ATOM_DETAILS['ADP']['url'])

        self.setItemByPath(['u_13', 'header'], 'U13')
        self.setItemByPath(['u_13', 'tooltip'], ATOM_DETAILS['ADP']['tooltip'])
        self.setItemByPath(['u_13', 'url'], ATOM_DETAILS['ADP']['url'])

        self.setItemByPath(['u_22', 'header'], 'U22')
        self.setItemByPath(['u_22', 'tooltip'], ATOM_DETAILS['ADP']['tooltip'])
        self.setItemByPath(['u_22', 'url'], ATOM_DETAILS['ADP']['url'])

        self.setItemByPath(['u_23', 'header'], 'U23')
        self.setItemByPath(['u_23', 'tooltip'], ATOM_DETAILS['ADP']['tooltip'])
        self.setItemByPath(['u_23', 'url'], ATOM_DETAILS['ADP']['url'])

        self.setItemByPath(['u_33', 'header'], 'U33')
        self.setItemByPath(['u_33', 'tooltip'], ATOM_DETAILS['ADP']['tooltip'])
        self.setItemByPath(['u_33', 'url'], ATOM_DETAILS['ADP']['url'])

    @classmethod
    def default(cls) -> 'ADP':
        u_11 = Base(*ATOM_DETAILS['ADP']['default'])
        u_12 = Base(*ATOM_DETAILS['ADP']['default'])
        u_13 = Base(*ATOM_DETAILS['ADP']['default'])

        u_22 = Base(*ATOM_DETAILS['ADP']['default'])
        u_23 = Base(*ATOM_DETAILS['ADP']['default'])

        u_33 = Base(*ATOM_DETAILS['ADP']['default'])

        return cls(u_11, u_22, u_33, u_12, u_13, u_23)

    @classmethod
    def fromPars(cls, u_11: float, u_12: float, u_13: float, u_22: float, u_23: float, u_33: float) -> 'ADP':
        u_11 = Base(u_11, ATOM_DETAILS['ADP']['default'][1])
        u_12 = Base(u_12, ATOM_DETAILS['ADP']['default'][1])
        u_13 = Base(u_13, ATOM_DETAILS['ADP']['default'][1])

        u_22 = Base(u_22, ATOM_DETAILS['ADP']['default'][1])
        u_23 = Base(u_23, ATOM_DETAILS['ADP']['default'][1])

        u_33 = Base(u_33, ATOM_DETAILS['ADP']['default'][1])

        return cls(u_11, u_22, u_33, u_12, u_13, u_23)

    def isEmpty(self) -> bool:
        val = False
        if self['u_33'].value is None:
            val = True
        return val


class MSP(PathDict):
    """
    Data store for Atom site magnetic susceptibility parameters
    """
    def __init__(self, MSPtype: Base,
                 chi_11: Base, chi_22: Base, chi_33: Base,
                 chi_12: Base, chi_13: Base, chi_23: Base):
        super().__init__(type=MSPtype, chi_11=chi_11, chi_22=chi_22, chi_33=chi_33,
                         chi_12=chi_12, chi_13=chi_13, chi_23=chi_23)

        self.setItemByPath(['type', 'header'], 'Type')

        self.setItemByPath(['chi_11', 'header'], 'U11')
        self.setItemByPath(['chi_11', 'tooltip'], ATOM_DETAILS['MSP']['tooltip'])
        self.setItemByPath(['chi_11', 'url'], ATOM_DETAILS['MSP']['url'])

        self.setItemByPath(['chi_12', 'header'], 'U12')
        self.setItemByPath(['chi_12', 'tooltip'], ATOM_DETAILS['MSP']['tooltip'])
        self.setItemByPath(['chi_12', 'url'], ATOM_DETAILS['MSP']['url'])

        self.setItemByPath(['chi_13', 'header'], 'U13')
        self.setItemByPath(['chi_13', 'tooltip'], ATOM_DETAILS['MSP']['tooltip'])
        self.setItemByPath(['chi_13', 'url'], ATOM_DETAILS['MSP']['url'])

        self.setItemByPath(['chi_22', 'header'], 'U22')
        self.setItemByPath(['chi_22', 'tooltip'], ATOM_DETAILS['MSP']['tooltip'])
        self.setItemByPath(['chi_22', 'url'], ATOM_DETAILS['MSP']['url'])

        self.setItemByPath(['chi_23', 'header'], 'U23')
        self.setItemByPath(['chi_23', 'tooltip'], ATOM_DETAILS['MSP']['tooltip'])
        self.setItemByPath(['chi_23', 'url'], ATOM_DETAILS['MSP']['url'])

        self.setItemByPath(['chi_33', 'header'], 'U33')
        self.setItemByPath(['chi_33', 'tooltip'], ATOM_DETAILS['MSP']['tooltip'])
        self.setItemByPath(['chi_33', 'url'], ATOM_DETAILS['MSP']['url'])

    @classmethod
    def default(cls) -> 'MSP':
        MSPtype = Base(None, '')

        chi_11 = Base(*ATOM_DETAILS['MSP']['default'])
        chi_12 = Base(*ATOM_DETAILS['MSP']['default'])
        chi_13 = Base(*ATOM_DETAILS['MSP']['default'])

        chi_21 = Base(*ATOM_DETAILS['MSP']['default'])
        chi_22 = Base(*ATOM_DETAILS['MSP']['default'])
        chi_23 = Base(*ATOM_DETAILS['MSP']['default'])

        chi_31 = Base(*ATOM_DETAILS['MSP']['default'])
        chi_32 = Base(*ATOM_DETAILS['MSP']['default'])
        chi_33 = Base(*ATOM_DETAILS['MSP']['default'])

        return cls(MSPtype, chi_11, chi_22, chi_33, chi_12, chi_13, chi_33)

    @classmethod
    def fromPars(cls, MSPtype: str, chi_11: float, chi_22: float, chi_33: float, chi_12: float, chi_13: float,
                 chi_23: float) -> 'MSP':
        MSPtype = Base(MSPtype, '')

        chi_11 = Base(chi_11, ATOM_DETAILS['MSP']['default'][1])
        chi_12 = Base(chi_12, ATOM_DETAILS['MSP']['default'][1])
        chi_13 = Base(chi_13, ATOM_DETAILS['MSP']['default'][1])

        chi_22 = Base(chi_22, ATOM_DETAILS['MSP']['default'][1])
        chi_23 = Base(chi_23, ATOM_DETAILS['MSP']['default'][1])

        chi_33 = Base(chi_33, ATOM_DETAILS['MSP']['default'][1])

        return cls(MSPtype, chi_11, chi_22, chi_33, chi_12, chi_13, chi_23)

    def isEmpty(self) -> bool:
        val = False
        if self['chi_11'].value is None:
            val = True
        return val
