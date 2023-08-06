import logging
import numpy as np
from numpy.testing import assert_allclose
from pprint import pformat
import pytest
import sys

from openfisca_ceq.tools.data import year_by_country
from openfisca_ceq.tools.survey_scenario import build_ceq_survey_scenario
from openfisca_ceq.tools.data.income_targets import read_target


log = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO, stream = sys.stdout)


@pytest.mark.parametrize("country", ["mali", "cote_d_ivoire", "senegal"])
def test_calibration(country):
    data_country = country
    year = year_by_country[country]
    log.info("Testing calibration on {} for year {}".format(country, year))
    survey_scenario = build_ceq_survey_scenario(legislation_country = country, year = year)

    gross_value_added_target = read_target(data_country, "gross_value_added")
    consumption_target = read_target(data_country, "consumption")

    log.info("VA brut: {}".format(
        gross_value_added_target / 1e9)
        )
    log.info("Salaire brut before calibration: {}".format(
        survey_scenario.compute_aggregate("salaire_brut", period = year) / 1e9)
        )
    log.info("Salaire super brut before calibration: {}".format(
        survey_scenario.compute_aggregate("salaire_super_brut", period = year) / 1e9)
        )

    income_variables = [
        'autoconsumption',
        'other_income',
        'gifts_sales_durables',
        'imputed_rent',
        'revenu_agricole',
        'autres_revenus_du_capital_brut',
        'revenu_informel_non_salarie',
        'revenu_informel_salarie',
        'revenu_non_salarie_brut',
        'revenu_foncier_brut',
        'pension_retraite_brut',
        'salaire_super_brut',
        ]

    target_variable_by_input_variable = {
        "salaire_brut": "salaire_super_brut"
        }

    share_by_variable, target_by_variable = survey_scenario.inflate_variables_sum_to_target(
        target_variables = income_variables,
        target = gross_value_added_target,
        period = year,
        target_variable_by_input_variable = target_variable_by_input_variable
        )

    log.info(pformat(share_by_variable))
    log.info(pformat(target_by_variable))

    for income_variable in income_variables:
        log.info("{} : {}".format(
            income_variable,
            survey_scenario.compute_aggregate(
                income_variable,
                period = year,
                )
            ))

    assert_allclose(
        sum(
            survey_scenario.compute_aggregate(
                income_variable,
                period = year,
                )
            for income_variable in income_variables
            if not np.isnan(
                survey_scenario.compute_aggregate(
                    income_variable,
                    period = year,
                    )
                )
            ),
        gross_value_added_target
        )

    assert_allclose(
        survey_scenario.compute_aggregate("salaire_super_brut", period = year),
        gross_value_added_target * share_by_variable["salaire_super_brut"],
        )

    log.info("Salaire brut after calibration: {}".format(
        survey_scenario.compute_aggregate("salaire_brut", period = year) / 1e9)
        )
    log.info("Salaire super brut after calibration: {}".format(
        survey_scenario.compute_aggregate("salaire_super_brut", period = year) / 1e9)
        )
    consumption_variables = [
        _variable
        for _variable in survey_scenario.tax_benefit_system.variables
        if _variable.startswith("poste_")
        ]

    share_by_variable, target_by_variable = survey_scenario.inflate_variables_sum_to_target(
        target_variables = consumption_variables,
        target = consumption_target,
        period = year,
        )

    log.debug(share_by_variable)
    log.debug(target_by_variable)
    log.info(survey_scenario.compute_aggregate("consumption", period = year))

    assert_allclose(
        survey_scenario.compute_aggregate("consumption", period = year),
        consumption_target,
        )

    # survey_scenario = build_ceq_survey_scenario(legislation_country = country, year = year,
    #     income_variables = income_variables, inflate = True)
    # assert_allclose(
    #     sum(
    #         survey_scenario.compute_aggregate(
    #             income_variable,
    #             period = year,
    #             )
    #         for income_variable in income_variables
    #         if not np.isnan(
    #             survey_scenario.compute_aggregate(
    #                 income_variable,
    #                 period = year,
    #                 )
    #             )
    #         ),
    #     gross_value_added_target
    #     )
