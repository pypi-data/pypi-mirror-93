import pandas as pd
from openfisca_core.model_api import Variable, YEAR
from openfisca_ceq.entities import Household


# Conversion depuis les variables listées dans openfisca-ceq/documentation/description_donnees_input.md

# entity ids
model_by_data_id_variable = {
    "hh_id": "household_id",
    "pers_id": "person_id",
    }

model_by_data_role_index_variable = {
    "cov_i_lien_cm": "household_role_index",
    }

# 12 + 1 revenus
initial_revenues_source = set([
    "rev_i_agricoles",
    "rev_i_autoconsommation",
    "rev_i_autres_revenus_capital",
    "rev_i_autres",
    "rev_i_autres_transferts",
    # "rev_i_independants",
    "rev_i_independants_Ntaxe",
    "rev_i_independants_taxe",
    "rev_i_locatifs",
    "rev_i_loyers_imputes",
    "rev_i_pensions",
    "rev_i_salaires_formels",
    "rev_i_salaires_informels",
    "rev_i_transferts_publics",
    ])

ceq_input_by_harmonized_variable = {
    "rev_i_autoconsommation": "autoconsumption",
    "rev_i_autres": "other_income",
    "rev_i_autres_transferts": "gifts_sales_durables",
    "rev_i_loyers_imputes": "imputed_rent",
    }

ceq_intermediate_by_harmonized_variable = {
    "rev_i_transferts_publics": "direct_transfers"
    }

non_ceq_input_by_harmonized_variable = {
    "rev_i_agricoles": "revenu_agricole",
    "rev_i_autres_revenus_capital": "autres_revenus_du_capital",
    "rev_i_independants_Ntaxe": "revenu_informel_non_salarie",
    "rev_i_independants_taxe": "revenu_non_salarie",
    # "rev_i_independants": "revenu_non_salarie_total",
    "rev_i_locatifs": "revenu_locatif",
    "rev_i_pensions": "pension_retraite",
    "rev_i_salaires_formels": "salaire",
    "rev_i_salaires_informels": "revenu_informel_salarie",
    }

household_variables = [
    "rev_i_autoconsommation",
    "rev_i_loyers_imputes",
    "rev_i_transferts_publics",
    ]


assert initial_revenues_source == (set(ceq_input_by_harmonized_variable.keys())
    .union(set(ceq_intermediate_by_harmonized_variable.keys()))
    .union(set(non_ceq_input_by_harmonized_variable.keys()))
    ), initial_revenues_source.difference(set(ceq_input_by_harmonized_variable.keys())
        .union(set(ceq_intermediate_by_harmonized_variable.keys()))
        .union(set(non_ceq_input_by_harmonized_variable.keys()))
        )

other_model_by_harmonized_person_variable = {
    "cov_i_categorie_CGU": "categorie_cgu",
    "cov_i_cadre": "cadre",
    "cov_i_classe_frequente": "eleve_enseignement_niveau",
    # "cov_i_enfant_charge": "nombre_enfants_a_charge",
    "cov_i_secteur_formel_informel": "secteur_formel",
    "cov_i_secteur_activite": "secteur_activite",
    "cov_i_secteur_calage": "secteur_calage",
    "cov_i_secteur_publique_prive": "secteur_public",
    # "cov_i_sexe": "sexe",
    "cov_i_statut_matrimonial": "statut_matrimonial",
    "cov_i_type_ecole": "eleve_enseignement_public",
    "cov_m_urbain_rural": "urbain",
    }

# label define cov_i_statut_matrimonial 1 "Marie" 2 "Celibataire" 3 "Veuf, Divorce" 4 "Non concerne"
# label values cov_i_statut_matrimonial cov_i_statut_matrimonial
# label define cov_i_sexe 1 "femme" 2 "homme"
# label values cov_i_sexe cov_i_sexe
# label define cov_i_lien_cm  1 "Chef du menage" 2 "Conjoint du CM" 3 "Enfant du chef/conjoint du CM" 4 "Pere/mere du CM/conjoint du CM" 5 "Autre parent du CM/conjoint du CM" 6 "Autres personnes non apparentees" 7 "Domestique"
# label values cov_i_lien_cm  cov_i_lien_cm
# label define cov_i_secteur_calage  1 "agriculture" 2 "industrie" 3 "service"
# label values cov_i_secteur_calage  cov_i_secteur_calage


person_variables = list(
    initial_revenues_source
    .union(set(other_model_by_harmonized_person_variable.keys()))
    .difference(set(household_variables))
    )

variables_by_entity = {
    "person": person_variables,
    "household": household_variables,
    }


# weights

data_by_model_weight_variable = {
    "household_weight": "pond_m",
    "person_weight": "pond_i",
    }


class all_income_excluding_transfers(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Earned and Unearned Incomes of All Possible Sources and Excluding Government Transfers"

    def formula(household, period):
        income_variables = [
            "autres_revenus_du_capital_brut",
            "revenu_agricole",
            "revenu_informel_non_salarie",
            "revenu_informel_salarie",
            "revenu_foncier_brut",
            "revenu_non_salarie_brut",
            "salaire_super_brut",
            ]
        return household.sum(
            sum(
                household.members(variable, period)
                for variable in income_variables
                )
            )


class customs_duties(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Customs Duties"

    def formula(household, period):
        return household('droits_douane', period)


class employee_contributions_health(Variable):
    def formula(household, period):
        return household.sum(household.members("sante_salarie", period))


class employee_contributions_pensions(Variable):
    def formula(household, period):
        return household.sum(household.members("retraite_salarie", period))


class employer_contributions_health(Variable):
    def formula(household, period):
        return household.sum(household.members("sante_employeur", period))


class employer_contributions_pensions(Variable):
    def formula(household, period):
        return household.sum(household.members("retraite_employeur", period))


class employer_other_contributions(Variable):
    def formula(household, period):
        return (
            household.sum(household.members("famille", period))
            + household.sum(household.members("accidents_du_travail", period))
            )


class nontaxable_income(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "All nontaxable source of income"

    def formula(household, period):
        income_variables = [
            "revenu_agricole",
            "revenu_informel_non_salarie",
            "revenu_informel_salarie",
            # TODO
            ]
        return household.sum(
            sum(
                household.members(variable, period)
                for variable in income_variables
                )
            )


class pensions(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Old-age contributory pensions"

    def formula(household, period):
        return household.sum(household.members("pension_retraite_brut", period))


class personal_income_tax(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Personal Income Tax"

    def formula(household, period):
        return household("impot_revenu", period)


class social_security_contributions(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Social security contributions"

    def formula(household, period):
        contribution_variables = [
            "employee_contributions_health",
            "employee_contributions_pensions",
            "employer_contributions_health",
            "employer_contributions_pensions",
            "employer_other_contributions",
            # TODO
            ]
        return sum(
            household(variable, period)
            for variable in contribution_variables
            )


class value_added_tax(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = " Value added tax (VAT)"

    def formula(household, period):
        return household('tva', period)


multi_country_custom_ceq_variables = [
    all_income_excluding_transfers,
    customs_duties,
    employee_contributions_health,
    employee_contributions_pensions,
    employer_contributions_health,
    employer_contributions_pensions,
    employer_other_contributions,
    nontaxable_income,
    pensions,
    personal_income_tax,
    social_security_contributions,
    value_added_tax,
    ]


def build_markdow_correspondance_table():
    model_by_harmonized_variable = dict()
    for updates in [
        model_by_data_id_variable,
        model_by_data_role_index_variable,
        ceq_input_by_harmonized_variable,
        ceq_intermediate_by_harmonized_variable,
        non_ceq_input_by_harmonized_variable,
        other_model_by_harmonized_person_variable,
            ]:

        model_by_harmonized_variable.update(updates)

    df = (
        pd.DataFrame.from_dict(
            model_by_harmonized_variable,
            orient = 'index',
            columns = ["Model variable"],
            )
        .sort_index()
        )
    df.index.rename("Harmonized variable", inplace = True)
    print(df.to_markdown())  # noqa


if __name__ == "__main__":
    build_markdow_correspondance_table()
