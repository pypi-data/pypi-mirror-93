import logging
import numexpr as ne
import os
import pkg_resources


from openfisca_core.model_api import Enum, not_, select, Variable, YEAR
from openfisca_core.reforms import Reform

from openfisca_ceq import (
    CountryTaxBenefitSystem as CEQTaxBenefitSystem,
    entities,
    )

from openfisca_ceq.tools.data_ceq_correspondence import (
    multi_country_custom_ceq_variables,
    non_ceq_input_by_harmonized_variable,
    )

from openfisca_ceq.tools.data.education_unit_cost import (
    build_unit_cost_by_category_by_country
    )

log = logging.getLogger(__name__)


ceq_variables_directory = os.path.join(
    pkg_resources.get_distribution('openfisca-ceq').location,
    'openfisca_ceq',
    'variables'
    )

assert os.path.exists(ceq_variables_directory)


ceq_variables = CEQTaxBenefitSystem().variables
ceq_input_variables = {
    name
    for name, variable in ceq_variables.items()
    if len(variable.formulas) == 0
    }

ceq_computed_variables = {
    name
    for name, variable in ceq_variables.items()
    if len(variable.formulas) > 0
    }


unit_cost_by_category_by_country = build_unit_cost_by_category_by_country()

MALI_PART_INFORMEL_NON_SALARIE = 1.0


class cadre(Variable):
    value_type = bool
    entity = entities.Person
    definition_period = YEAR
    label = "L'individu est un cadre salarié"


class categorie_cgu(Variable):
    # prod A: revendeurs de ciments et de denrées alimentaires
    # prod B: autres commerçants ou revendeurs (CGU )
    # [CGU comm/prod A < CGU comm/prod B < CGU service] -> 0, 1 ,2
    # NaNs are -1
    value_type = int
    entity = entities.Person
    definition_period = YEAR
    label = "Index de la catgeorie CGU de l'individu"


labor_type_by_index = {
    0: "Inactive",
    1: "Formal public wage worker",
    2: "Formal private wage worker",
    3: "Informal wage worker",
    4: "Informal independent worker",
    5: "Agricultural worker",
    }


class TypesLaborType(Enum):
    __order__ = 'inactive formal_public_wage_worker formal_private_wage_worker informal_wage_worker informal_independent_worker agricultural_worker'
    inactive = "Inactive",
    formal_public_wage_worker = "Formal public wage worker",
    formal_private_wage_worker = "Formal private wage worker",
    informal_wage_worker = "Informal wage worker",
    informal_independent_worker = "Informal independent worker",
    agricultural_worker = "Agricultural worker",


class labor_type(Variable):
    value_type = Enum
    possible_values = TypesLaborType
    default_value = TypesLaborType.inactive
    entity = entities.Household
    definition_period = YEAR
    label = "Activité de la personne de référence du ménage"

    def formula(household, period):
        secteur_activite = household.personne_de_reference('secteur_activite', period)
        # Actif agricole < Salarie/dependant formel < Salarie/dependant informel <Independant
        secteur_public = household.personne_de_reference('secteur_public', period)
        return select(
            [
                secteur_activite == -1,  # Inactif ?
                (secteur_activite == 1) & secteur_public,  # Formal public wage worker
                (secteur_activite == 1) & not_(secteur_public),  # Formal private wage worker
                secteur_activite == 2,  # Informal wage worker
                secteur_activite == 3,  # Informal independent worker
                secteur_activite == 0,  # Agricultural worker
                ],
            [
                0,
                1,
                2,
                3,
                4,
                5,
                ],
            )


class number_of_people_per_household(Variable):
    value_type = int
    entity = entities.Household
    definition_period = YEAR
    label = "Nombre d'individus par ménage"

    def formula(household, period):
        return household.nb_persons()


class revenu_non_salarie_total(Variable):
    value_type = float
    entity = entities.Person
    definition_period = YEAR
    label = "Revenu non salarié total"

    def formula(person, period):
        return person('revenu_informel_non_salarie', period) + person('revenu_non_salarie', period)


class secteur_activite(Variable):
    value_type = int
    entity = entities.Person
    definition_period = YEAR
    label = "Secteur d'activité de l'individu"
    # [Actif agricole < Salarie/dependant formel < Salarie/dependant informel <Independant]


class secteur_formel(Variable):
    value_type = bool
    entity = entities.Person
    definition_period = YEAR
    label = "Secteur formel"


class secteur_public(Variable):
    value_type = bool
    entity = entities.Person
    definition_period = YEAR
    label = "L'individu est un salarié du secteur public"


class survey_income(Variable):
    value_type = float
    entity = entities.Household
    definition_period = YEAR
    label = "Revenus produits par l'enquête"

    def formula(household, period):
        return (
            household("autoconsumption", period)  # "rev_i_autoconsommation"
            + household.sum(household.members("other_income", period))  # "rev_i_autres"
            + household.sum(household.members("gifts_sales_durables", period))  # "rev_i_autres_transferts"
            + household("imputed_rent", period)  # "rev_i_loyers_imputes"
            + household("direct_transfers", period)  # "rev_i_transferts_publics"
            + household.sum(household.members("revenu_agricole", period))  # "rev_i_agricoles"
            + household.sum(household.members("autres_revenus_du_capital", period))  # "rev_i_autres_revenus_capital"
            + household.sum(household.members("revenu_informel_non_salarie", period))  # "rev_i_independants_Ntaxe"
            + household.sum(household.members("revenu_non_salarie", period))  # "rev_i_independants_taxe"
            + household.sum(household.members("revenu_locatif", period))  # "rev_i_locatifs"
            + household.sum(household.members("pension_retraite", period))  # "rev_i_pensions"
            + household.sum(household.members("salaire", period))  # "rev_i_salaires_formels"
            + household.sum(household.members("revenu_informel_salarie", period))  # "rev_i_salaires_informels"
            )


class urbain(Variable):
    value_type = bool
    entity = entities.Person
    definition_period = YEAR
    label = "L'individu vit en milieu urbain (par opposition à rural)"


# For matching with original data

class hh_id(Variable):
    value_type = int
    entity = entities.Household
    definition_period = YEAR
    label = "hh_id"


class pers_id(Variable):
    value_type = int
    entity = entities.Person
    definition_period = YEAR
    label = "pers_id"


# Reform

class ceq(Reform):
    name = "CEQ enhanced tax and benefit system"

    def apply(self):
        add_ceq_framework(self)
        assert self.legislation_country is not None
        add_ceq_education_unit_cost(self, self.legislation_country)

# Helpers


def add_ceq_framework(country_tax_benefit_system):
    """Add CEQ framework to a specific country's tax benefit system

    :param country_tax_benefit_system: The country tax-benefit-system
    :type country_tax_benefit_system: TaxBenefitSystem
    :return: The completed tax benefit system
    :rtype: TaxBenefitSystem
    """

    country_entities = country_tax_benefit_system.entities
    entities_by_name = dict((entity.key, entity) for entity in country_entities)
    entities.Person = entities_by_name['person']
    entities.Household = entities_by_name['household']
    country_variables = set(country_tax_benefit_system.variables.keys())

    input_intersection_country = ceq_input_variables.intersection(country_variables)
    if input_intersection_country:
        log.info("Country variables replacing CEQ input variables:\n{}".format(
            " - " + ('\n - ').join(
                list(sorted(input_intersection_country))
                )
            ))
    input_difference_country = ceq_input_variables.difference(country_variables)
    if input_difference_country:
        log.info("Missing CEQ input variables:\n{}".format(
            " - " + ('\n - ').join(
                list(sorted(input_difference_country))
                )
            ))
    computed_intersection_country = ceq_computed_variables.intersection(country_variables)
    if computed_intersection_country:
        log.info("Country variables replacing CEQ computed variables:\n{}".format(
            " - " + ('\n - ').join(
                list(sorted(computed_intersection_country))
                )
            ))

    ignored_variables = country_variables
    assert not country_variables.intersection(ceq_computed_variables), \
        "Some country variables matches computed CEQ variables: {}".format(
            country_variables.intersection(ceq_computed_variables))

    country_tax_benefit_system.add_variables_from_directory(ceq_variables_directory,
        ignored_variables = ignored_variables)

    missing_income_variables = set(non_ceq_input_by_harmonized_variable.values()).difference(
        set(country_tax_benefit_system.variables.keys())
        )
    for missing_income_variable in missing_income_variables:
        definitions_by_name = dict(
            definition_period = YEAR,
            entity = entities_by_name['person'],
            label = missing_income_variable,
            value_type = float,
            )
        country_tax_benefit_system.add_variable(
            type(missing_income_variable, (Variable,), definitions_by_name)
            )

    for variable in multi_country_custom_ceq_variables:
        country_tax_benefit_system.update_variable(variable)

    # if (
    #         hasattr(country_tax_benefit_system, 'legislation_country')
    #         and country_tax_benefit_system.legislation_country == 'mali'
    #         ):

    #     class revenu_non_salarie(Variable):
    #         def formula(person, period):
    #             return (1 - MALI_PART_INFORMEL_NON_SALARIE) * person('revenu_non_salarie_total', period)

    #     class revenu_informel_non_salarie(Variable):
    #         def formula(person, period):
    #             return MALI_PART_INFORMEL_NON_SALARIE * person('revenu_non_salarie_total', period)

    #     country_tax_benefit_system.update_variable(revenu_non_salarie)
    #     country_tax_benefit_system.update_variable(revenu_informel_non_salarie)

    country_tax_benefit_system.replace_variable(revenu_non_salarie_total)
    country_tax_benefit_system.add_variable(cadre)

    if "categorie_cgu" in country_tax_benefit_system.variables:
        country_tax_benefit_system.replace_variable(categorie_cgu)
    else:
        country_tax_benefit_system.add_variable(categorie_cgu)

    country_tax_benefit_system.add_variable(labor_type)
    country_tax_benefit_system.add_variable(secteur_public)
    country_tax_benefit_system.add_variable(secteur_activite)
    country_tax_benefit_system.add_variable(secteur_formel)
    country_tax_benefit_system.add_variable(survey_income)
    country_tax_benefit_system.add_variable(urbain)
    country_tax_benefit_system.add_variable(number_of_people_per_household)
    country_tax_benefit_system.add_variable(hh_id)
    country_tax_benefit_system.add_variable(pers_id)

    return country_tax_benefit_system


def add_ceq_education_unit_cost(country_tax_benefit_system, legislation_country):

    entities_by_name = dict(
        (entity.key, entity)
        for entity in country_tax_benefit_system.entities
        )

    definitions_by_name = dict(
        definition_period = YEAR,
        entity = entities_by_name['person'],
        label = "Niveau d'enseignement de l'élève ou de l'étudiant",
        value_type = float,
        )
    country_tax_benefit_system.add_variable(
        type("eleve_enseignement_niveau", (Variable,), definitions_by_name)
        )
    del definitions_by_name
    definitions_by_name = dict(
        definition_period = YEAR,
        entity = entities_by_name['person'],
        label = "L'élève ou de l'étudiant fréquente l'enseignement public",
        value_type = float,
        default_value = 1.0,
        )
    country_tax_benefit_system.add_variable(
        type("eleve_enseignement_public", (Variable,), definitions_by_name)
        )

    enseignement_niveau_by_variable_name = {
        'pre_school': 0,
        'primary_education': 1,
        'secondary_education': 2,
        'tertiary_education': 3,
        }

    for variable_name, enseignement_niveau in enseignement_niveau_by_variable_name.items():

        def unit_cost_function_creator(cost, enseignement_niveau):
            def func(entity, period_arg):
                eleve_enseignement_niveau = entity('eleve_enseignement_niveau', period_arg)  # noqa F841
                eleve_enseignement_public = entity('eleve_enseignement_public', period_arg)  # noqa F841
                expression = "(eleve_enseignement_niveau == {enseignement_niveau}) * eleve_enseignement_public * {cost}".format(
                    enseignement_niveau = enseignement_niveau,
                    cost = cost,
                    )
                return ne.evaluate(str(expression))

            func.__name__ = "formula"
            return func

        cost = unit_cost_by_category_by_country[legislation_country]
        definitions_by_name = dict(
            definition_period = YEAR,
            entity = entities_by_name['person'],
            formula = unit_cost_function_creator(cost[variable_name], enseignement_niveau),
            label = variable_name,
            value_type = float,
            )
        country_tax_benefit_system.add_variable(
            type(variable_name + '_person', (Variable,), definitions_by_name)
            )

        def household_education_formula_creator(person_variable_name):
            def func(household, period_arg):
                return household.sum(household.members(person_variable_name, period_arg))
            func.__name__ = "formula"
            return func

        country_tax_benefit_system.update_variable(
            type(variable_name, (Variable,), dict(formula = household_education_formula_creator(variable_name + "_person")))
            )


def get_all_neutralized_variables(survey_scenario, period, variables):
    """List all neutralized and de-facto neutralized variables from scenario from a particular list

    :param survey_scenario: The survey scenario to extract the variables from
    :type survey_scenario: SurveyScenario
    :param period: period to compute to check the variables for
    :type period: Period
    :param variables: variables list to check
    :type variables: list
    :return: By design and de facto neutralized variables lists
    :rtype: list, list
    """
    assert variables is not None
    df_by_entity = survey_scenario.create_data_frame_by_entity(
        variables = variables,
        period = period,
        )
    by_design_neutralized_variables_by_entity = dict()
    de_facto_neutralized_variables_by_entity = dict()

    for entity, df in df_by_entity.items():
        by_design_neutralized_variables = list()
        de_facto_neutralized_variables = list()
        for column in df:
            variable = survey_scenario.tax_benefit_system.variables.get(column)
            if variable is None:
                continue
            if variable.is_neutralized:
                by_design_neutralized_variables.append(column)
            elif (df[column] == variable.default_value).all():
                de_facto_neutralized_variables.append(column)

        by_design_neutralized_variables_by_entity[entity] = by_design_neutralized_variables
        de_facto_neutralized_variables_by_entity[entity] = de_facto_neutralized_variables

    return by_design_neutralized_variables_by_entity, de_facto_neutralized_variables_by_entity
