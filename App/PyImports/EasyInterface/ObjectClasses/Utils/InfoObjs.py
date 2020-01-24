from .DictTools import PathDict
from .BaseClasses import Base
from datetime import datetime

APP_INFO = {
     'name': 'easyDiffraction',
     'version': '0.3.9',
     'url': 'http://easydiffraction.org'
}

CALCULATOR_INFO = {
    'name': 'CrysPy',
    'version': '0.1.13',
    'url': 'https://github.com/ikibalin/cryspy'
}

INFO_DETAILS = {
    'chi_squared': {
        'header': 'χ²',
        'tooltip': 'Goodness of fit as estimated by the Pearson''s chi-squared test.',
        'url': 'https://en.wikipedia.org/wiki/Chi-squared_test',
        'default': (0, '')
    },
    'n_res': {
        'header': '',
        'tooltip': 'Number of free parameters.',
        'url': '',
        'default': (0, '')
    }
}


class Info(PathDict):
    def __init__(self, phase_ids: list, experiment_ids: list, modified_datetime: str, refinement_datetime: str,
                 chi_squared: Base, n_res: Base):
        super().__init__(phase_ids=phase_ids, experiment_ids=experiment_ids, modified_datetime=modified_datetime,
                         refinement_datetime=refinement_datetime, chi_squared=chi_squared, n_res=n_res)

        self.setItemByPath(['chi_squared', 'header'], INFO_DETAILS['chi_squared']['header'])
        self.setItemByPath(['chi_squared', 'tooltip'], INFO_DETAILS['chi_squared']['tooltip'])
        self.setItemByPath(['chi_squared', 'url'], INFO_DETAILS['chi_squared']['url'])

        self.setItemByPath(['n_res', 'header'], INFO_DETAILS['n_res']['header'])
        self.setItemByPath(['n_res', 'tooltip'], INFO_DETAILS['n_res']['tooltip'])
        self.setItemByPath(['n_res', 'url'], INFO_DETAILS['n_res']['url'])

    @classmethod
    def default(cls) -> 'Info':
        phase_ids = []
        experiment_ids = []
        modified_datetime = str(datetime.now())
        refinement_datetime = ''
        chi_squared = Base(*INFO_DETAILS['chi_squared']['default'])
        n_res = Base(*INFO_DETAILS['n_res']['default'])
        return cls(phase_ids, experiment_ids, modified_datetime, refinement_datetime, chi_squared, n_res)


class _progInfo(PathDict):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return '{} - {}'.format(self['name'], self['version'])

    @classmethod
    def default(cls):
        return cls()


class Calculator(_progInfo):
    def __init__(self):
        super().__init__(**CALCULATOR_INFO)


class App(_progInfo):
    def __init__(self):
        super().__init__(**APP_INFO)
