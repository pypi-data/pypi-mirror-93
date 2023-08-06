import logging


log = logging.getLogger(__name__)


def compute_total_ht_imports(survey_scenario):
    total_ht_imports_variable = [
        variable
        for variable in survey_scenario.tax_benefit_system.variables
        if 'droits_douane_' in variable
        ]
    log.debug(total_ht_imports_variable)

    return sum(
        survey_scenario.compute_aggregate(variable, period = survey_scenario.year)
        for variable in total_ht_imports_variable
        )


# if __name__ == '__main__':
# from openfisca_ceq.tools.data import year_by_country
# from openfisca_ceq.tools.survey_scenario import build_ceq_survey_scenario
#     country = "senegal"
#     year = year_by_country[country]
#     survey_scenario = build_ceq_survey_scenario(legislation_country = country, year = year)
#     print(compute_total_ht_imports(survey_scenario))
