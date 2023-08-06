import logging
import pandas as pd


from openfisca_ceq.tools.data import config_parser
from openfisca_ceq.tools.indirect_taxation.consumption_items_nomenclature import country_code_by_country
from openfisca_ceq.tools.data import year_by_country


log = logging.getLogger(__name__)


GROSS_VALUE_ADDED = "VA Totale (LCU)"
HOUSEHOLD_CONSUMPTION = "Conso finale ménages (LCU)"


def read_target(country, variable):
    assert variable in ["gross_value_added", "consumption"]
    target_variable = GROSS_VALUE_ADDED if variable == "gross_value_added" else HOUSEHOLD_CONSUMPTION
    code_country = country_code_by_country[country]
    year = year_by_country[country]
    targets_file = config_parser.get("ceq", "targets_file")

    target = (pd.read_excel(targets_file, sheet_name = "calage")
        .query("iso == @code_country")
        .query("year == @year")
        .query("DESC_3 == @target_variable")
        ["montant"]
        .copy()
        )
    assert len(target) == 1, target
    target = target.values[0] * 1e9
    del code_country, target_variable, year
    log.info("{} target for {} is {} Billion CFA".format(
        variable, country, target / 1e9))
    return target


# if __name__ == "__main__":
#     country = "senegal"
#     for variable in ["gross_value_added", "consumption"]:
#         print(read_target(country, variable))
