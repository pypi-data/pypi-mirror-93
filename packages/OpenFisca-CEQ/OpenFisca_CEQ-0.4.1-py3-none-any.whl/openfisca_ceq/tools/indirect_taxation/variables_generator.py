from slugify import slugify
import logging


from openfisca_core.model_api import Variable, YEAR


log = logging.getLogger(__name__)


GLOBAL_YEAR_START = 1994
GLOBAL_YEAR_STOP = 2019


def generate_postes_variables(tax_benefit_system, label_by_code_coicop):
    """Generate COICOP item of consumption (poste de consommation)

    :param TaxBenfitSystem tax_benefit_system: the tax and benefit system to create the items variable for
    :param dict label_by_code_coicop: Coicop item number and item description
    """
    item_variables = list()
    for code_coicop, label in label_by_code_coicop.items():
        class_name = "poste_{}".format(slugify(code_coicop, separator = '_'))
        log.info('Creating variable {} with label {}'.format(class_name, label))
        # Trick to create a class with a dynamic name.
        entity = tax_benefit_system.entities_by_singular()['household']
        tax_benefit_system.add_variable(
            type(class_name, (Variable,), dict(
                definition_period = YEAR,
                entity = entity,
                label = label,
                value_type = float,
                ))
            )
        item_variables.append(class_name)

    generate_total_consumption(tax_benefit_system, item_variables)


def generate_total_consumption(tax_benefit_system, item_variables, consumption_variable_name = 'consumption'):

    def formula(household, period):
        return sum(
            household(variable, period)
            for variable in item_variables
            )

    definitions_by_name = dict(
        definition_period = YEAR,
        value_type = float,
        entity = tax_benefit_system.entities_by_singular()['household'],
        label = "Consommation",
        )
    definitions_by_name.update(dict(formula = formula))
    tax_benefit_system.add_variable(
        type(consumption_variable_name, (Variable,), definitions_by_name)
        )


def generate_depenses_ht_postes_variables(tax_benefit_system, tax_name, tax_rate_by_code_coicop, null_rates = []):
    """Create depenses_ht_poste_code_coicop variables for every code_coicop
    assuming no code coicop dies and resucitates over time

    :param tax_benefit_system: the tax benefit system that will host the generated variables
    :type tax_benefit_system: TaxBenefitSystem
    :param tax_name: The name of the proportional ad valorem tax
    :type tax_name: str
    :param tax_rate_by_code_coicop: The tax rates for every COICOP code
    :type tax_rate_by_code_coicop: DataFrame
    :param null_rates: The values of the tax rates corresponding to exemption, defaults to []
    :type null_rates: list, optional
    """
    # Almost identical to openfisca-france-indirect-taxation eponymous function
    reference_rates = sorted(tax_rate_by_code_coicop[tax_name].unique())

    functions_by_name_by_poste = dict()
    postes_coicop_all = set()

    for tax_rate in reference_rates:
        functions_by_name = dict()

        time_varying_rates = 'start' in tax_rate_by_code_coicop.columns
        if time_varying_rates:
            start_years = reference_rates.start.fillna(GLOBAL_YEAR_START).unique()
            stop_years = reference_rates.start.fillna(GLOBAL_YEAR_STOP).unique()  # last year
            years_range = sorted(list(set(start_years + stop_years)))
            year_stop_by_year_start = zip(years_range[:-1], years_range[1:])
        else:
            year_stop_by_year_start = {GLOBAL_YEAR_START: GLOBAL_YEAR_STOP}

        for year_start, year_stop in year_stop_by_year_start.items():
            filter_expression = '({} == @tax_rate)'.format(tax_name)
            if time_varying_rates:
                filter_expression += 'and (start <= @year_start) and (stop >= @year_stop)'
            postes_coicop = sorted(
                tax_rate_by_code_coicop.query(filter_expression)['code_coicop'].astype(str)
                )

            log.debug('Creating fiscal category {} - {} (starting in {} and ending in {}) pre-tax expenses for the following products {}'.format(
                tax_name, tax_rate, year_start, year_stop, postes_coicop))

            for poste_coicop in postes_coicop:
                selection = (tax_rate_by_code_coicop
                    .query(filter_expression)
                    .query("code_coicop == @poste_coicop")
                    )
                assert len(selection) == 1, selection
                tariff = selection['droits_douane'].astype(str)
                imported_share = selection['part_importation'].astype(float)
                dated_func_ht_hd = depenses_ht_hd_postes_function_creator(
                    poste_coicop,
                    tax_rate,
                    tariff = tariff.values[0],
                    imported_share = imported_share.values[0],
                    year_start = year_start,
                    null_rates = null_rates,
                    )
                dated_func_ht = depenses_ht_postes_function_creator(
                    poste_coicop,
                    tariff = tariff.values[0],
                    imported_share = imported_share.values[0],
                    year_start = year_start,
                    null_rates = null_rates,
                    )
                dated_func_ht_hd_sd = depenses_ht_hd_sd_postes_function_creator(
                    poste_coicop,
                    tax_rate,
                    tariff = tariff.values[0],
                    imported_share = imported_share.values[0],
                    year_start = year_start,
                    null_rates = null_rates,
                    )
                dated_function_name = "formula_{year_start}".format(year_start = year_start)

                if poste_coicop not in functions_by_name_by_poste:
                    functions_by_name_by_poste[poste_coicop + "_ht_hd_sd"] = dict()
                    functions_by_name_by_poste[poste_coicop + "_ht_hd"] = dict()
                    functions_by_name_by_poste[poste_coicop + "_ht"] = dict()

                functions_by_name_by_poste[poste_coicop + "_ht_hd_sd"][dated_function_name] = dated_func_ht_hd_sd
                functions_by_name_by_poste[poste_coicop + "_ht_hd"][dated_function_name] = dated_func_ht_hd
                functions_by_name_by_poste[poste_coicop + "_ht"][dated_function_name] = dated_func_ht

            postes_coicop_all = set.union(set(postes_coicop), postes_coicop_all)

    assert (
        set(
            key.replace("_ht_hd_sd", "").replace("_ht_hd", "").replace("_ht", "")
            for key in functions_by_name_by_poste.keys()
            ) == postes_coicop_all
        )

    for poste, functions_by_name in list(functions_by_name_by_poste.items()):
        if poste.endswith("_ht_hd_sd"):
            class_name = 'depenses_ht_hd_sd_poste_{}'.format(
                slugify(poste.replace("_ht_hd_sd", ""), separator = '_')
                )
            definitions_by_name = dict(
                definition_period = YEAR,
                value_type = float,
                entity = tax_benefit_system.entities_by_singular()['household'],
                label = "Dépenses hors taxe et hors douane du poste_{} soumis à douane".format(poste),
                )
        if poste.endswith("_ht_hd"):
            class_name = 'depenses_ht_hd_poste_{}'.format(
                slugify(poste.replace("_ht_hd", ""), separator = '_')
                )
            definitions_by_name = dict(
                definition_period = YEAR,
                value_type = float,
                entity = tax_benefit_system.entities_by_singular()['household'],
                label = "Dépenses hors taxe et hors douane du poste_{}".format(poste),
                )
        if poste.endswith("_ht"):
            class_name = 'depenses_ht_poste_{}'.format(
                slugify(poste.replace("_ht", ""), separator = '_')
                )
            definitions_by_name = dict(
                definition_period = YEAR,
                value_type = float,
                entity = tax_benefit_system.entities_by_singular()['household'],
                label = "Dépenses hors taxe du poste_{}".format(poste),
                )

        definitions_by_name.update(functions_by_name)
        tax_benefit_system.add_variable(
            type(class_name, (Variable,), definitions_by_name)
            )
        del definitions_by_name


def depenses_ht_hd_postes_function_creator(
        poste_coicop, tax_rate, tariff = None, imported_share = None, year_start = None, null_rates = []
        ):
    """Create a function for the pre-tax pre-customs duties expense of a particular poste COICOP

    :param poste_coicop: Poste COICOP
    :type poste_coicop: str
    :param parameters: Legislation parameters tree
    :type parameters: ParameterNodetax_rate_by_code_coicop
    :param tax_rate: The name of the applied tax rate
    :type tax_rate: str
    :param tariff: The name of the applied tariff
    :type tariff: str
    :param imported_share: The imported part of the good
    :type imported_share: float
    :param year_start: Starting year
    :type year_start: int, optional
    :param null_rates: The values of the tax rates corresponding to exemption, defaults to []
    :type null_rates: list, optional
    :return: pre-tax expense of a particular poste COICOP
    :rtype: function
    """
    # Almost identical to openfisca-france-indirect-taxation eponymous function
    assert tax_rate is not None
    assert imported_share is None or isinstance(imported_share, float), \
        "imported_share = {} should be None or a float".format(imported_share)

    def func(entity, period_arg, parameters, tax_rate = tax_rate, tariff = tariff, imported_share = imported_share):
        impots_indirects = parameters(period_arg.start).prelevements_obligatoires.impots_indirects
        if (tax_rate is None) or (tax_rate in null_rates):
            tax_rate_ = 0
        else:
            tax_rate_ = impots_indirects.tva[tax_rate]

        depenses_ttc = entity('poste_' + slugify(poste_coicop, separator = '_'), period_arg)
        depenses_ht = depenses_ttc / (1 + tax_rate_)

        if tariff:
            assert imported_share is not None
            tariff_rate = impots_indirects.droits_douane[tariff]
            assert 1 >= tariff_rate >= 0
            # depenses_ht = depenses_ht_hd * (1 - imported_share) + depenses_ht_hd * imported_share * (1 + tariff_rate)
            return (
                depenses_ht / (1 + imported_share * tariff_rate)
                )
        else:
            return depenses_ht

    func.__name__ = "formula_{year_start}".format(year_start = year_start)
    return func


def depenses_ht_hd_sd_postes_function_creator(
        poste_coicop, tax_rate, tariff = None, imported_share = None, year_start = None, null_rates = []
        ):
    """Create a function for the pre-tax expense of a particular poste COICOP

    :param poste_coicop: Poste COICOP
    :type poste_coicop: str
    :param parameters: Legislation parameters tree
    :type parameters: ParameterNodetax_rate_by_code_coicop
    :param tax_rate: The name of the applied tax rate
    :type tax_rate: str
    :param tariff: The name of the applied tariff
    :type tariff: str
    :param imported_share: The imported part of the good
    :type imported_share: float
    :param year_start: Starting year
    :type year_start: int, optional
    :param null_rates: The values of the tax rates corresponding to exemption, defaults to []
    :type null_rates: list, optional
    :return: pre-tax expense of a particular poste COICOP
    :rtype: function
    """
    # Almost identical to openfisca-france-indirect-taxation eponymous function
    assert tax_rate is not None

    def func(entity, period_arg, parameters, tax_rate = tax_rate, tariff = tariff, imported_share = imported_share):
        impots_indirects = parameters(period_arg.start).prelevements_obligatoires.impots_indirects
        if (tax_rate is None) or (tax_rate in null_rates):
            tax_rate_ = 0
        else:
            tax_rate_ = impots_indirects.tva[tax_rate]

        depenses_ttc = entity('poste_' + slugify(poste_coicop, separator = '_'), period_arg)
        depenses_ht = depenses_ttc / (1 + tax_rate_)

        if tariff:
            assert imported_share is not None
            tariff_rate = impots_indirects.droits_douane[tariff]
            assert 1 >= tariff_rate >= 0
            # depenses_ht_hd_sd = imported_share * depenses_ht_hd = imported_share * depenses_ht / (1 + imported_share * tariff_rate)
            return depenses_ht * imported_share / (1 + imported_share * tariff_rate)
        else:
            return depenses_ht

    func.__name__ = "formula_{year_start}".format(year_start = year_start)
    return func


def depenses_ht_postes_function_creator(
        poste_coicop, tariff = None, imported_share = None, year_start = None, null_rates = []
        ):
    """Create a function for the pre-tax expense of a particular poste COICOP

    :param poste_coicop: Poste COICOP
    :type poste_coicop: str
    :param parameters: Legislation parameters tree
    :type parameters: ParameterNodetax_rate_by_code_coicop
    :param year_start: Starting year
    :type year_start: int, optional
    :param null_rates: The values of the tax rates corresponding to exemption, defaults to []
    :type null_rates: list, optional
    :return: pre-tax expense of a particular poste COICOP
    :rtype: function
    """
    def func(entity, period_arg, parameters, tariff = tariff, imported_share = imported_share):
        depenses_ht_hd = entity('depenses_ht_hd_poste_' + slugify(poste_coicop, separator = '_'), period_arg)

        if tariff:
            assert imported_share is not None
            impots_indirects = parameters(period_arg.start).prelevements_obligatoires.impots_indirects
            tariff_rate = impots_indirects.droits_douane[tariff]
            assert 1 >= tariff_rate >= 0
            return depenses_ht_hd * (1 + imported_share * tariff_rate)
        else:
            return depenses_ht_hd

    func.__name__ = "formula_{year_start}".format(year_start = year_start)
    return func


def depenses_ht_categorie_function_creator(postes_coicop, year_start = None):
    if len(postes_coicop) != 0:
        def func(entity, period_arg):
            return sum(entity(
                'depenses_ht_poste_' + slugify(poste, separator = '_'), period_arg)
                for poste in postes_coicop
                )

        func.__name__ = "formula_{year_start}".format(year_start = year_start)
        return func

    else:  # To deal with Reform emptying some fiscal categories
        def func(entity, period_arg):
            return 0

    func.__name__ = "formula_{year_start}".format(year_start = year_start)
    return func


def depenses_ht_hd_sd_categorie_function_creator(postes_coicop, year_start = None):
    if len(postes_coicop) != 0:
        def func(entity, period_arg):
            return sum(entity(
                'depenses_ht_hd_sd_poste_' + slugify(poste, separator = '_'), period_arg)
                for poste in postes_coicop
                )

        func.__name__ = "formula_{year_start}".format(year_start = year_start)
        return func

    else:  # To deal with Reform emptying some fiscal categories
        def func(entity, period_arg):
            return 0

    func.__name__ = "formula_{year_start}".format(year_start = year_start)
    return func


def generate_fiscal_base_variables(tax_benefit_system, tax_name, tax_rate_by_code_coicop, null_rates = []):
    reference_rates = sorted(tax_rate_by_code_coicop[tax_name].unique())
    time_varying_rates = 'start' in tax_rate_by_code_coicop.columns
    for tax_rate in reference_rates:
        functions_by_name = dict()
        if time_varying_rates:
            start_years = reference_rates.start.fillna(GLOBAL_YEAR_START).unique()
            stop_years = reference_rates.start.fillna(GLOBAL_YEAR_STOP).unique()  # last year
            years_range = sorted(list(set(start_years + stop_years)))
            year_stop_by_year_start = zip(years_range[:-1], years_range[1:])
        else:
            year_stop_by_year_start = {GLOBAL_YEAR_START: GLOBAL_YEAR_STOP}

        for year_start, year_stop in year_stop_by_year_start.items():
            filter_expression = '({} == @tax_rate)'.format(tax_name)
            if time_varying_rates:
                filter_expression += 'and (start <= @yyear_start) and (stop >= @yyear_stop)'
            postes_coicop = sorted(
                tax_rate_by_code_coicop.query(filter_expression)['code_coicop'].astype(str)
                )

            log.debug('Creating fiscal category {} - {} (starting in {} and ending in {}) aggregate expenses with the following products {}'.format(
                tax_name, tax_rate, year_start, year_stop, postes_coicop))

            dated_func = depenses_ht_categorie_function_creator(
                postes_coicop,
                year_start = year_start,
                )
            dated_function_name = "formula_{year_start}".format(year_start = year_start)
            functions_by_name[dated_function_name] = dated_func

        class_name = 'depenses_ht_{}_{}'.format(tax_name, tax_rate)
        definitions_by_name = dict(
            value_type = float,
            entity = tax_benefit_system.entities_by_singular()['household'],
            label = "Dépenses hors taxes {} - {}".format(tax_name, tax_rate),
            definition_period = YEAR,
            )
        definitions_by_name.update(functions_by_name)
        tax_benefit_system.add_variable(
            type(class_name, (Variable,), definitions_by_name)
            )

        del definitions_by_name, functions_by_name


def generate_tariff_base_variables(tax_benefit_system, tariff_name, tax_rate_by_code_coicop, null_rates = []):
    reference_rates = sorted(tax_rate_by_code_coicop[tariff_name].unique())
    time_varying_rates = 'start' in tax_rate_by_code_coicop.columns
    for tariff_rate in reference_rates:
        functions_by_name = dict()
        if time_varying_rates:
            start_years = reference_rates.start.fillna(GLOBAL_YEAR_START).unique()
            stop_years = reference_rates.start.fillna(GLOBAL_YEAR_STOP).unique()  # last year
            years_range = sorted(list(set(start_years + stop_years)))
            year_stop_by_year_start = zip(years_range[:-1], years_range[1:])
        else:
            year_stop_by_year_start = {GLOBAL_YEAR_START: GLOBAL_YEAR_STOP}

        for year_start, year_stop in year_stop_by_year_start.items():
            filter_expression = '({} == @tariff_rate)'.format(tariff_name)
            if time_varying_rates:
                filter_expression += 'and (start <= @yyear_start) and (stop >= @yyear_stop)'
            postes_coicop = sorted(
                tax_rate_by_code_coicop.query(filter_expression)['code_coicop'].astype(str)
                )

            log.debug('Creating tariff category {} - {} (starting in {} and ending in {}) aggregate expenses with the following products {}'.format(
                tariff_name, tariff_rate, year_start, year_stop, postes_coicop))

            dated_func = depenses_ht_hd_sd_categorie_function_creator(
                postes_coicop,
                year_start = year_start,
                )
            dated_function_name = "formula_{year_start}".format(year_start = year_start)
            functions_by_name[dated_function_name] = dated_func

        class_name = 'depenses_ht_hd_sd_{}_{}'.format(tariff_name, tariff_rate)
        definitions_by_name = dict(
            value_type = float,
            entity = tax_benefit_system.entities_by_singular()['household'],
            label = "Dépenses hors taxes hors douane {} - {}".format(tariff_name, tariff_rate),
            definition_period = YEAR,
            )
        definitions_by_name.update(functions_by_name)
        tax_benefit_system.add_variable(
            type(class_name, (Variable,), definitions_by_name)
            )

        del definitions_by_name, functions_by_name


def create_tax_formula(tax_name, tax_rate):
    def func(entity, period_arg, parameters):
        pre_tax_expenses = entity('depenses_ht_{}_{}'.format(tax_name, tax_rate), period_arg)
        rate = parameters(period_arg).prelevements_obligatoires.impots_indirects.tva[tax_rate]
        return pre_tax_expenses * rate

    func.__name__ = "formula_{year_start}".format(year_start = GLOBAL_YEAR_START)
    return func


def create_tariff_formula(tariff_name, tariff_rate):
    def func(entity, period_arg, parameters):
        pre_tax_expenses = entity('depenses_ht_hd_sd_{}_{}'.format(tariff_name, tariff_rate), period_arg)
        rate = parameters(period_arg).prelevements_obligatoires.impots_indirects[tariff_name][tariff_rate]
        return pre_tax_expenses * rate

    func.__name__ = "formula_{year_start}".format(year_start = GLOBAL_YEAR_START)
    return func


def generate_ad_valorem_tax_variables(tax_benefit_system, tax_name, tax_rate_by_code_coicop, null_rates = []):
    reference_rates = sorted(tax_rate_by_code_coicop[tax_name].unique())
    ad_valorem_tax_components = list()
    for tax_rate in reference_rates:
        if tax_rate in null_rates:
            continue

        log.debug('Creating tax amount {} - {}'.format(tax_name, tax_rate))

        class_name = '{}_{}'.format(tax_name, tax_rate)

        definitions_by_name = dict(
            value_type = float,
            entity = tax_benefit_system.entities_by_singular()['household'],
            label = "{} - {}".format(tax_name, tax_rate),
            definition_period = YEAR,
            )

        definitions_by_name.update({"formula": create_tax_formula(tax_name, tax_rate)})
        tax_benefit_system.add_variable(
            type(class_name, (Variable,), definitions_by_name)
            )

        ad_valorem_tax_components += [class_name]

    class_name = tax_name

    def ad_valorem_tax_total_func(entity, period_arg):
        return sum(
            entity(class_name, period_arg)
            for class_name in ad_valorem_tax_components
            )

    ad_valorem_tax_total_func.__name__ = "formula_{year_start}".format(year_start = GLOBAL_YEAR_START)
    definitions_by_name = dict(
        value_type = float,
        entity = tax_benefit_system.entities_by_singular()['household'],
        label = "{} - total".format(tax_name),
        definition_period = YEAR,
        )
    definitions_by_name.update(
        {ad_valorem_tax_total_func.__name__: ad_valorem_tax_total_func}
        )

    tax_benefit_system.add_variable(
        type(class_name, (Variable,), definitions_by_name)
        )


def generate_tariff_variables(tax_benefit_system, tariff_name, tax_rate_by_code_coicop, null_rates = []):
    reference_rates = sorted(tax_rate_by_code_coicop[tariff_name].unique())
    tariff_components = list()
    for tariff_rate in reference_rates:
        if tariff_rate in null_rates:
            continue

        log.debug('Creating tariff amount {} - {}'.format(tariff_name, tariff_rate))

        class_name = '{}_{}'.format(tariff_name, tariff_rate)

        definitions_by_name = dict(
            value_type = float,
            entity = tax_benefit_system.entities_by_singular()['household'],
            label = "{} - {}".format(tariff_name, tariff_rate),
            definition_period = YEAR,
            )

        definitions_by_name.update({"formula": create_tariff_formula(
            tariff_name, tariff_rate)})
        tax_benefit_system.add_variable(
            type(class_name, (Variable,), definitions_by_name)
            )

        tariff_components += [class_name]

    class_name = tariff_name

    def tariff_total_func(entity, period_arg):
        return sum(
            entity(class_name, period_arg)
            for class_name in tariff_components
            )

    tariff_total_func.__name__ = "formula_{year_start}".format(year_start = GLOBAL_YEAR_START)
    definitions_by_name = dict(
        value_type = float,
        entity = tax_benefit_system.entities_by_singular()['household'],
        label = "{} - total".format(tariff_name),
        definition_period = YEAR,
        )
    definitions_by_name.update(
        {tariff_total_func.__name__: tariff_total_func}
        )

    tax_benefit_system.add_variable(
        type(class_name, (Variable,), definitions_by_name)
        )
