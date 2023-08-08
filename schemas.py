from enum import Enum


class CalculationType(str, Enum):
    one_unit = 'Расчет за одну единицу'
    max_units_for_all_articuls = 'Расчет на макс. кол-во единиц на каждый артикул'
    max_units_total = 'Расчет макс. кол-ва суммарно'


