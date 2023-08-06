import logging

from openfisca_ceq.tools.indirect_taxation.consumption_items_nomenclature import (
    build_tax_rate_by_code_coicop,
    build_label_by_code_coicop,
    )
from openfisca_ceq.tools.indirect_taxation.variables_generator import (
    generate_ad_valorem_tax_variables,
    generate_depenses_ht_postes_variables,
    generate_fiscal_base_variables,
    generate_postes_variables,
    generate_tariff_base_variables,
    generate_tariff_variables,
    )


log = logging.getLogger(__name__)


indirect_tax_by_country = {
    "cote_d_ivoire": ['tva', 'droits_douane'],
    "mali": ['tva', 'droits_douane'],
    "senegal": ['tva', 'droits_douane'],
    }


def add_coicop_item_to_tax_benefit_system(tax_benefit_system, country):
    filter_expression = "bien_durable == 0"
    label_by_code_coicop = (build_label_by_code_coicop(country, filter_expression = filter_expression)
        .filter(['label_variable'])
        .reset_index()
        .rename(columns = {'deduplicated_code_coicop': "code_coicop"})
        .set_index("code_coicop")
        .to_dict()['label_variable']
        )
    log.debug(label_by_code_coicop)
    log.debug(tax_benefit_system.variables.keys())
    generate_postes_variables(tax_benefit_system, label_by_code_coicop)
    tax_variables = indirect_tax_by_country.get(country)
    if 'droits_douane' in tax_variables and "part_importation" not in tax_variables:
        tax_variables.append("part_importation")
    if "part_importation" in tax_variables:
        fillna = {'part_importation': 0}
    tax_rate_by_code_coicop = build_tax_rate_by_code_coicop(country, tax_variables, fillna = fillna, filter_expression = filter_expression)
    tax_name = 'tva'
    null_rates = ['exonere']
    generate_depenses_ht_postes_variables(
        tax_benefit_system,
        tax_name,
        tax_rate_by_code_coicop,
        null_rates = null_rates,
        )
    generate_fiscal_base_variables(tax_benefit_system, tax_name, tax_rate_by_code_coicop, null_rates)
    generate_tariff_base_variables(tax_benefit_system, 'droits_douane', tax_rate_by_code_coicop, null_rates)
    generate_ad_valorem_tax_variables(tax_benefit_system, tax_name, tax_rate_by_code_coicop, null_rates)
    generate_tariff_variables(tax_benefit_system, 'droits_douane', tax_rate_by_code_coicop, null_rates)
