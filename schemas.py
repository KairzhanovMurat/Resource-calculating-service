from enum import Enum


class CalculationType(str, Enum):
    one_unit = 'one_unit'
    max_units_for_all_articuls = 'max_units_for_all_articuls'
    max_units_total = 'max_units_total'


