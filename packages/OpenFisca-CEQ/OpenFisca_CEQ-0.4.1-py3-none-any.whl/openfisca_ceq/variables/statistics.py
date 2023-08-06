import numpy as np


from openfisca_survey_manager.statshelpers import mark_weighted_percentiles
from openfisca_core.model_api import *
from openfisca_ceq.entities import *


class decile_disposable_income_per_capita(Variable):
    value_type = int
    entity = Household
    definition_period = YEAR
    label = "Decile of disposable income per capita"

    def formula(household, period):
        disposable_income = household('disposable_income', period)
        number_of_people_per_household = household('number_of_people_per_household', period)
        weights = (
            household("household_weight", period)
            * household("number_of_people_per_household", period)
            )
        labels = np.arange(1, 11)
        decile, _ = mark_weighted_percentiles(
            disposable_income / number_of_people_per_household,
            labels,
            weights,
            method = 2,
            return_quantiles = True,
            )
        return decile


class decile_market_income_per_capita(Variable):
    value_type = int
    entity = Household
    definition_period = YEAR
    label = "Decile of market income per capita"

    def formula(household, period):
        market_income = household('market_income', period)
        number_of_people_per_household = household('number_of_people_per_household', period)
        weights = (
            household("household_weight", period)
            * household("number_of_people_per_household", period)
            )
        labels = np.arange(1, 11)
        decile, _ = mark_weighted_percentiles(
            market_income / number_of_people_per_household,
            labels,
            weights,
            method = 2,
            return_quantiles = True,
            )
        return decile


class decile_consumable_income_per_capita(Variable):
    value_type = int
    entity = Household
    definition_period = YEAR
    label = "Decile of consumable income per capita"

    def formula(household, period):
        return compute_decile_income_per_capita(
            income = 'consumable_income',
            household = household,
            period = period
            )


class decile_final_income_per_capita(Variable):
    value_type = int
    entity = Household
    definition_period = YEAR
    label = "Decile of final income per capita"

    def formula(household, period):
        return compute_decile_income_per_capita(
            income = 'final_income',
            household = household,
            period = period,
            )


class decile_gross_income_per_capita(Variable):
    value_type = int
    entity = Household
    definition_period = YEAR
    label = "Decile of gross income per capita"

    def formula(household, period):
        return compute_decile_income_per_capita(
            income = 'gross_income',
            household = household,
            period = period,
            )


class decile_market_income_plus_pensions_per_capita(Variable):
    value_type = int
    entity = Household
    definition_period = YEAR
    label = "Decile of market income plus pensions per capita"

    def formula(household, period):
        return compute_decile_income_per_capita(
            income = 'market_income_plus_pensions',
            household = household,
            period = period,
            )


class decile_survey_income_per_capita(Variable):
    value_type = int
    entity = Household
    definition_period = YEAR
    label = "Decile of survey income plus pensions per capita"

    def formula(household, period):
        return compute_decile_income_per_capita(
            income = 'market_income_plus_pensions',
            household = household,
            period = period,
            )


# Helper

def compute_decile_income_per_capita(income, household, period):
    income = household(income, period)
    number_of_people_per_household = household('number_of_people_per_household', period)
    weights = (
        household("household_weight", period)
        * household("number_of_people_per_household", period)
        )
    labels = np.arange(1, 11)
    decile, _ = mark_weighted_percentiles(
        income / number_of_people_per_household,
        labels,
        weights,
        method = 2,
        return_quantiles = True,
        )
    return decile
