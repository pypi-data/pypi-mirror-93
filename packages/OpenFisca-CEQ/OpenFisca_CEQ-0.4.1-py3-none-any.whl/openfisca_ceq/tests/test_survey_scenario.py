import logging
import pandas as pd
import pytest


from openfisca_ceq.tools.data import year_by_country
from openfisca_ceq.tools.survey_scenario import build_ceq_survey_scenario


log = logging.getLogger(__name__)


@pytest.mark.parametrize("country, year", list(year_by_country.items()))
def test(country, year):
    survey_scenario = build_ceq_survey_scenario(legislation_country = country, year = year)
    assert survey_scenario is not None
    assert not survey_scenario.tax_benefit_system.variables['eleve_enseignement_niveau'].is_neutralized


if __name__ == '__main__':
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)
    from openfisca_ceq.tools.data_ceq_correspondence import (
        ceq_input_by_harmonized_variable,
        ceq_intermediate_by_harmonized_variable,
        non_ceq_input_by_harmonized_variable,
        )

    country = "senegal"
    year = year_by_country[country]
    survey_scenario = build_ceq_survey_scenario(legislation_country = country, year = year, adjust_indirect_taxation = True)
    assert not survey_scenario.tax_benefit_system.variables['eleve_enseignement_niveau'].is_neutralized
    ceq_by_harmonized_variable = dict()
    ceq_by_harmonized_variable.update(ceq_input_by_harmonized_variable)
    ceq_by_harmonized_variable.update(ceq_intermediate_by_harmonized_variable)
    ceq_by_harmonized_variable.update(non_ceq_input_by_harmonized_variable)

    data = [
        (harmonized_variable, openfisca_variable, survey_scenario.compute_aggregate(openfisca_variable, period = year) / 1e9)
        for harmonized_variable, openfisca_variable in ceq_by_harmonized_variable.items()
        ]
    log.info(pd.DataFrame(data, columns = ["harmonized", "openfisca", "aggregate"]))
    # BIM

    # for variable in variables:
    #     log.info(
    #         "{variable}: {aggregate} billions FCFA".format(
    #             variable = variable,
    #             aggregate = int(round(survey_scenario.compute_aggregate(variable, period = survey_scenario.year) / 1e9))
    #             )
    #         )

    from openfisca_ceq.tools.indirect_taxation.tax_benefit_system_indirect_taxation_completion import indirect_tax_by_country

    indirect_tax_variables = [
        variable
        for tax in indirect_tax_by_country[country]
        for variable in survey_scenario.tax_benefit_system.variables.keys()
        if tax in variable
        ]
    log.info(indirect_tax_variables)

    log.info(
        pd.DataFrame(
            index = indirect_tax_variables,
            columns = ['aggregate'],
            data = [
                survey_scenario.compute_aggregate(variable, period = year) / 1e9
                for variable in indirect_tax_variables
                ]
            )
        )

    log.info(survey_scenario.compute_aggregate("salaire_super_brut", period = year) / 1e9)
