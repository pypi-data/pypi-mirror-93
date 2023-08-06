import logging
import pandas as pd


from openfisca_ceq.tools.data import config_parser
# from openfisca_ceq.tools.indirect_taxation.consumption_items_nomenclature import country_code_by_country
from openfisca_ceq.tools.survey_scenario import build_ceq_survey_scenario
from openfisca_ceq.tools.data import year_by_country
from openfisca_ceq.tools.results.imports import compute_total_ht_imports


log = logging.getLogger(__name__)


variable_by_index = {
    'Total tax revenue': '',
    'Direct taxes': 'direct_taxes',
    'Personal Income Taxes': 'personal_income_tax',
    'Social Security Contributions': 'social_security_contributions',
    'Corporate Income Tax': 'corporate_income_tax',
    'Other Direct Taxes': 'other_direct_taxes',
    'Indirect taxes': 'indirect_taxes',
    'VAT': 'value_added_tax',
    'Import Taxes': 'customs_duties',
    'Excise taxes': 'excise_taxes',
    'on Oil Derivates': '',
    'on alcohol, tabac and other non-oil derivatives': '',
    'Other Indirect Taxes': '',
    }


country_label_by_country = {
    "mali": "Mali",
    "senegal": "Senegal",
    "cote_d_ivoire": "Cote d'Ivoire",
    }

detailed_taxes_by_country = {
    "senegal": [
        "contribution_globale_fonciere",
        "contribution_globale_unique",
        "droit_progressif_pension_retraite",
        "droit_progressif_salaire",
        "droit_progressif",
        "droit_proportionnel_autres_revenus",
        "droit_proportionnel_salaire",
        "droit_proportionnel",
        "impot_revenus",
        # "contribution_forfaitaire_charge_employeur",
        ],
    "mali": ["impot_traitement_salaire"],
    "cote_d_ivoire": [
        "impot_general_revenu",
        "impot_revenu_creances",
        "impot_revenu_foncier"
        ],
    }


def build_simulated_results(survey_scenario, index, add_country_details = False):
    simulated_amounts = pd.Series(
        index = index,
        dtype = float
        )
    for index_, variable in variable_by_index.items():
        if variable in survey_scenario.tax_benefit_system.variables:
            simulated_amounts[index_] = (
                survey_scenario.compute_aggregate(variable, period = survey_scenario.year) / 1e9
                )

    if add_country_details:
        for variable in detailed_taxes_by_country[survey_scenario.legislation_country]:
            simulated_amounts[variable] = survey_scenario.compute_aggregate(variable, period = survey_scenario.year) / 1e9

        simulated_amounts["total_ht_imports"] = compute_total_ht_imports(survey_scenario) / 1e9

    return simulated_amounts


def read_tax_target(country = None, add_country_details = False):

    results = None

    for country_, year in year_by_country.items():
        if country and country != country_:
            continue
        survey_scenario = build_ceq_survey_scenario(legislation_country = country_, year = year)
        inflated_survey_scenario = build_ceq_survey_scenario(legislation_country = country_, year = year, inflate = True)
        result = build_country_result(survey_scenario, inflated_survey_scenario, add_country_details)
        results = result if results is None else pd.concat([results, result], axis = 1)

    return results.round(1)


def build_country_result(survey_scenario, inflated_survey_scenario, add_country_details = False):
    targets_file = config_parser.get("ceq", "targets_file")
    target = pd.read_excel(
        targets_file,
        sheet_name = "tableau_16",
        header = [0, 1],
        index_col = 0,
        )
    extraction = target.xs('Millions FCFA', level=1, axis=1)
    country = survey_scenario.legislation_country
    country_label = country_label_by_country[country]
    result = pd.DataFrame(columns = pd.MultiIndex(
        levels = [[country_label], ["actual", "direct", "inflated"]],
        codes = [[0, 0, 0], [0, 1, 2]],
        ))
    result[country_label, "actual"] = extraction[country_label].copy()

    simulated_amounts = build_simulated_results(survey_scenario, result.index, add_country_details)
    result = result.reindex(simulated_amounts.index)
    result[country_label, "direct"] = simulated_amounts

    simulated_amounts = build_simulated_results(inflated_survey_scenario, result.index, add_country_details)
    result[country_label, "inflated"] = simulated_amounts

    return result.round(1)


# if __name__ == '__main__':
#     print(read_tax_target())
