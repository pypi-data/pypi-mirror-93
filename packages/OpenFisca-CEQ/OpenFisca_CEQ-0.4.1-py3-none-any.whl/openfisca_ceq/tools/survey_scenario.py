import logging
import numpy as np
import pandas as pd
from scipy.optimize import fsolve

from openfisca_core import periods
from openfisca_core.model_api import Variable, where, YEAR

from openfisca_survey_manager.scenarios import AbstractSurveyScenario
from openfisca_ceq.tools.tax_benefit_system_ceq_completion import ceq
from openfisca_ceq.tools.indirect_taxation.tax_benefit_system_indirect_taxation_completion import (
    add_coicop_item_to_tax_benefit_system)
from openfisca_ceq.tools.data.expenditures_loader import load_expenditures
from openfisca_ceq.tools.data.income_loader import build_income_dataframes
from openfisca_ceq.tools.data.income_targets import read_target
from openfisca_ceq.tools.data_ceq_correspondence import (
    ceq_input_by_harmonized_variable,
    ceq_intermediate_by_harmonized_variable,
    data_by_model_weight_variable,
    model_by_data_id_variable,
    non_ceq_input_by_harmonized_variable,
    other_model_by_harmonized_person_variable,
    )

from openfisca_cote_d_ivoire import CountryTaxBenefitSystem as CoteDIvoireTaxBenefitSystem
from openfisca_mali import CountryTaxBenefitSystem as MaliTaxBenefitSystem
from openfisca_senegal import CountryTaxBenefitSystem as SenegalTaxBenefitSystem


log = logging.getLogger(__name__)


tax_benefit_system_class_by_country = dict(
    cote_d_ivoire = CoteDIvoireTaxBenefitSystem,
    mali = MaliTaxBenefitSystem,
    senegal = SenegalTaxBenefitSystem,
    )


class CEQSurveyScenario(AbstractSurveyScenario):
    weight_variable_by_entity = dict(
        household = 'household_weight',
        person = 'person_weight',
        )
    legislation_country = None
    data_country = None
    varying_variable = None

    def __init__(self, tax_benefit_system = None, baseline_tax_benefit_system = None, year = None,
            data = None, use_marginal_tax_rate = False, varying_variable = None, variation_factor = 0.03):
        super(CEQSurveyScenario, self).__init__()
        assert year is not None
        self.year = year

        assert tax_benefit_system is not None
        self.set_tax_benefit_systems(
            tax_benefit_system = tax_benefit_system,
            baseline_tax_benefit_system = baseline_tax_benefit_system,
            )

        if use_marginal_tax_rate:
            assert varying_variable is not None
            assert varying_variable in self.tax_benefit_system.variables
            self.variation_factor = variation_factor
            self.varying_variable = varying_variable

        if data is None:
            return

        if 'input_data_frame_by_entity_by_period' in data:
            period = periods.period(year)
            dataframe_variables = set()
            for entity_dataframe in data['input_data_frame_by_entity_by_period'][period].values():
                if not isinstance(entity_dataframe, pd.DataFrame):
                    continue
                dataframe_variables = dataframe_variables.union(set(entity_dataframe.columns))
            self.used_as_input_variables = list(
                set(tax_benefit_system.variables.keys()).intersection(dataframe_variables)
                )

        elif 'input_data_frame' in data:
            input_data_frame = data.get('input_data_frame')
            self.used_as_input_variables = list(
                set(tax_benefit_system.variables.keys()).intersection(
                    set(input_data_frame.columns)
                    )
                )

        self.init_from_data(data = data, use_marginal_tax_rate = use_marginal_tax_rate)

    def inflate_to_match_gross_valued_added_and_consumption(self):
        country = self.data_country
        gross_value_added_target = read_target(country, "gross_value_added")
        consumption_target = read_target(country, "consumption")
        self.income_variables = income_variables = [
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
        self.inflate_variables_sum_to_target(
            target_variables = income_variables,
            target = gross_value_added_target,
            period = self.year,
            target_variable_by_input_variable = target_variable_by_input_variable
            )
        consumption_variables = [
            _variable
            for _variable in self.tax_benefit_system.variables
            if _variable.startswith("poste_")
            ]
        self.inflate_variables_sum_to_target(
            target_variables = consumption_variables,
            target = consumption_target,
            period = self.year,
            )

    def inflate_variables_sum_to_target(self, target_variables, target, period,
            target_variable_by_input_variable = dict()):

        for target_variable in target_variables:
            assert target_variable in self.tax_benefit_system.variables

        aggregate_by_variable = dict(
            (
                target_variable,
                self.compute_aggregate(
                    target_variable,
                    period = period,
                    missing_variable_default_value = 0,
                    )
                )
            for target_variable in target_variables
            )
        for _variable, _aggregate in aggregate_by_variable.items():
            if np.isnan(aggregate_by_variable[target_variable]):
                aggregate_by_variable[target_variable] = 0

        total = sum(aggregate_by_variable.values())
        assert total != 0
        share_by_variable = dict(
            (target_variable, aggregate_by_variable[target_variable] / total)
            for target_variable in target_variables
            )
        for _variable, share in share_by_variable.items():
            assert not np.isnan(share), "NaN ({}) share for variable {}".format(share, _variable)

        for input_variable, target_variable in target_variable_by_input_variable.items():
            self.reach_target(
                target_variable,
                share_by_variable[target_variable] * target,
                input_variable,
                period
                )

        target_by_variable = dict(
            (target_variable, share_by_variable[target_variable] * target)
            for target_variable in target_variables
            if (
                target_variable not in target_variable_by_input_variable.values()
                and share_by_variable[target_variable] != 0
                )
            )

        self.inflate(target_by_variable = target_by_variable, period = period)

        return share_by_variable, target_by_variable

    def reach_target(self, variable, target, input_variable, period, inflator_first_guess = 1.1):
        initial_input_array = self.simulation.calculate_add(input_variable, period = period)

        def compute_error(inflator):
            input_array = inflator * initial_input_array
            self.simulation.delete_arrays(variable, period = period)  # delete existing arrays
            self.simulation.delete_arrays(input_variable, period = period)  # delete existing arrays
            self.simulation.set_input(input_variable, period, input_array)  # insert inflated array

            aggregate = self.compute_aggregate(variable, period = period)
            error = aggregate - target
            return error

        result = fsolve(compute_error, inflator_first_guess)

        log.info("Inflate {} by {} to have aggregate of {} == {}".format(
            input_variable, result, variable, target
            ))
        self.simulation.delete_arrays(variable, period = period)
        self.simulation.delete_arrays(input_variable, period = period)
        self.simulation.set_input(input_variable, period, result * initial_input_array)


def build_ceq_data(country, year = None):
    household_expenditures = load_expenditures(country)
    person, household_income = build_income_dataframes(country)

    households_missing_in_income = set(household_expenditures.hh_id).difference(
        set(household_income.hh_id))
    if households_missing_in_income:
        log.debug("Households missing in income: \n {}".format(households_missing_in_income))
    households_missing_in_expenditures = set(household_income.hh_id).difference(set(household_expenditures.hh_id))
    if households_missing_in_expenditures:
        log.debug("Households missing in expenditures: \n {}".format(households_missing_in_expenditures))

    household = household_income.merge(household_expenditures, on = "hh_id", how = "left")
    log.info(
        "{}: keeping only {} households from income data but {} are present in expenditures data".format(
            country, len(household_income.hh_id.unique()), len(household_expenditures.hh_id.unique())
            )
        )

    assert person.cov_i_lien_cm.dtype == pd.CategoricalDtype(
        categories = [
            'Chef du menage',
            'Conjoint du CM',
            'Enfant du chef/conjoint du CM',
            'Pere/mere du CM/conjoint du CM',
            'Autre parent du CM/conjoint du CM',
            'Autres personnes non apparentees',
            'Domestique'
            ],
        ordered = True
        )

    person.rename(columns = {"cov_i_lien_cm": "household_role_index"}, inplace = True)

    # assert (person.household_role_index.cat.codes != -1).all(), \
    #     "{}: there are {} NaN household_role_index".format(
    #             country,
    #             (person.household_role_index.cat.codes == -1).sum(),
    #             )

    if (person.household_role_index.cat.codes == -1).any():
        person = person.loc[person.household_role_index.cat.codes != -1].copy()

    assert (person.household_role_index.cat.codes != -1).all()
    person.household_role_index = person.household_role_index.cat.codes.clip(0, 3)

    if country == "mali":
        person.loc[
            (person.hh_id == "098105") & (person.household_role_index == 0),
            "household_role_index"
            ] = (0, 1)

        one_personne_de_reference = (person
            .query("household_role_index == 0")
            .groupby("hh_id")['household_role_index']
            .count() == 1)

        problematic_hh_id = one_personne_de_reference.loc[~one_personne_de_reference].index.tolist()
        assert one_personne_de_reference.all(), "Problem with households: {}".format(
            person.loc[person.hh_id.isin(problematic_hh_id), ["household_role_index", "hh_id"]]
            )

        if country == "mali":
            hh_id_with_missing_personne_de_reference = set(household.hh_id).difference(
                set(
                    person.loc[person.household_role_index == 0, 'hh_id'].unique()
                    )
                )
            person = person.loc[~person.hh_id.isin(hh_id_with_missing_personne_de_reference)].copy()
            household = household.loc[~household.hh_id.isin(hh_id_with_missing_personne_de_reference)].copy()

    # else:
    #     assert person.household_role_index.min() == 1
    #     person.household_role_index = (person.household_role_index - 1).clip(0, 3).astype(int)

    assert (person.household_role_index == 0).sum() == len(household), (
        "Only {} personne de reference for {} households".format(
            (person.household_role_index == 0).sum(), len(household)),
        "Household without personne de reference are: {}".format(
            set(household.hh_id).difference(
                set(
                    person.loc[person.household_role_index == 0, 'hh_id'].unique()
                    )
                )
            )
        )

    assert (person.household_role_index == 0).sum() == len(person.hh_id.unique()), (
        "Only {} personne de reference for {} unique households IDs".format(
            (person.household_role_index == 0).sum(), len(person.hh_id.unique())
            )
        )

    model_by_data_weight_variable = {v: k for k, v in data_by_model_weight_variable.items()}

    model_variable_by_person_variable = dict()
    variables = [
        ceq_input_by_harmonized_variable,
        ceq_intermediate_by_harmonized_variable,
        model_by_data_id_variable,
        non_ceq_input_by_harmonized_variable,
        model_by_data_weight_variable,
        other_model_by_harmonized_person_variable,
        ]
    for item in variables:
        model_variable_by_person_variable.update(item)

    household.rename(columns = model_variable_by_person_variable, inplace = True)
    person.rename(columns = model_variable_by_person_variable, inplace = True)

    # for original_variable, openfisca_variable in other_model_by_harmonized_person_variable.items():
    #     if openfisca_variable in person.columns:
    #         print(original_variable)
    #         print(person[openfisca_variable].value_counts(dropna = False))
    #         print(person[openfisca_variable].dtype)
    #         try:
    #             person[openfisca_variable].cat
    #         except Exception:
    #             pass
    #     else:
    #         print("{} not available for {}".format(original_variable, country))

    assert person.cadre.dtype == pd.CategoricalDtype(
        categories = ['non-cadre', 'cadre'],
        ordered = True
        )
    person.cadre = person.cadre == 'cadre'

    assert person.categorie_cgu.dtype == pd.CategoricalDtype(
        categories = ['CGU comm/prod A', 'CGU comm/prod B', 'CGU service'],
        ordered = True
        )
    person.categorie_cgu = person.categorie_cgu.cat.codes  # int

    assert person.eleve_enseignement_niveau.dtype == pd.CategoricalDtype(
        categories = [
            'Maternelle', 'Primaire', 'Secondaire', 'Superieur'],
        ordered = True,
        )
    person.eleve_enseignement_niveau = person.eleve_enseignement_niveau.cat.codes

    if country == 'mali':  # Variable absente pour le Mali
        person['eleve_enseignement_public'] = True
    else:
        assert person.eleve_enseignement_public.dtype == pd.CategoricalDtype(
            categories = ['public', 'prive'],
            ordered = True
            )
        person.eleve_enseignement_public = person.eleve_enseignement_public == 'public'

    assert person.secteur_activite.dtype == pd.CategoricalDtype(
        categories = [
            'Actif agricole',
            'Salarie/dependant formel',
            'Salarie/dependant informel',
            'Independant',
            ],
        ordered = True
        )
    person.secteur_activite = person.secteur_activite.cat.codes

    assert person.secteur_formel.dtype == pd.CategoricalDtype(
        categories = ['formel', 'informel'],
        ordered = True
        )
    person.secteur_formel = person.secteur_formel == 'formel'

    assert person.secteur_public.dtype == pd.CategoricalDtype(
        categories = ['public', 'prive'],
        ordered = True
        )
    person.secteur_public = person.secteur_public == 'public'

    assert (
        person.statut_matrimonial.dtype == pd.CategoricalDtype(
            categories = ['Marie', 'Celibataire', 'Veuf, Divorce', 'Non concerne'],
            ordered = True
            )
        or person.statut_matrimonial.dtype == pd.CategoricalDtype(
            categories = ['Marie', 'Celibataire', 'Veuf, Divorce'],
            ordered = True
            )  # Needed only for CIV
        )
    person.statut_matrimonial = person.statut_matrimonial.cat.codes

    assert person.urbain.dtype == pd.CategoricalDtype(
        categories = ['urbain', 'rural'],
        ordered = True)
    person.urbain = person.urbain == 'urbain'

    assert 'person_weight' in person
    assert 'household_weight' in household
    person['pers_id'] = person.person_id.astype(int)
    household['hh_id'] = household.household_id.astype(int)
    person.person_id = (person.person_id.rank() - 1).astype(int)
    person.household_id = (person.household_id.rank() - 1).astype(int)
    household.household_id = (household.household_id.rank() - 1).astype(int)
    input_data_frame_by_entity = dict(household = household, person = person)
    input_data_frame_by_entity_by_period = {periods.period(year): input_data_frame_by_entity}
    data = dict(input_data_frame_by_entity_by_period = input_data_frame_by_entity_by_period)
    return data


def build_ceq_survey_scenario(legislation_country, year = None, data_country = None,
        inflate = False, adjust_indirect_taxation = False):

    if data_country is None:
        data_country = legislation_country

    CountryTaxBenefitSystem = tax_benefit_system_class_by_country[legislation_country]
    CountryTaxBenefitSystem.legislation_country = legislation_country
    tax_benefit_system = ceq(CountryTaxBenefitSystem(coicop = False))
    add_coicop_item_to_tax_benefit_system(tax_benefit_system, legislation_country)
    if adjust_indirect_taxation:
        from openfisca_ceq.entities import Household

        class consumable_income(Variable):
            value_type = float
            entity = Household
            definition_period = YEAR
            label = "Consumable income"

            def formula(household, period):
                disposable_income = household('disposable_income', period)
                consumption = household('consumption', period)
                indirect_subsidies = household('indirect_subsidies', period)
                indirect_taxes = household('indirect_taxes', period)
                return where(
                    consumption > 0,
                    disposable_income * (1 - (indirect_taxes - indirect_subsidies) / consumption),
                    disposable_income,
                    )

        tax_benefit_system.update_variable(consumable_income)

    data = build_ceq_data(data_country, year)

    scenario = CEQSurveyScenario(
        tax_benefit_system = tax_benefit_system,
        year = year,
        data = data,
        )

    scenario.legislation_country = legislation_country
    scenario.data_country = data_country
    if not inflate:
        return scenario

    scenario.inflate_to_match_gross_valued_added_and_consumption()

    return scenario
