"""
This file is part of Apricopt.

Apricopt is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Apricopt is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Apricopt.  If not, see <http://www.gnu.org/licenses/>.

Copyright (C) 2020 Marco Esposito, Leonardo Picchiami.
"""


from typing import Dict, Set, Tuple, Callable, List

import re
import yaml
import json
import petab
from pandas import DataFrame

from apricopt.model.FastObservable import FastObservable
from apricopt.model.Model import Model
from apricopt.model.Observable import Observable
from apricopt.model.ObservableFunction import getFunction, Identity
from apricopt.model.Parameter import Parameter
from apricopt.simulation.COPASI.COPASIEngine import COPASIEngine
from apricopt.simulation.SimulationEngine import SimulationEngine



def parse_generation_config_file(config_filename: str, sample_n=None,sample_skip=None, sample_start=None,
                                 sample_end=None, dump_filename=None):
    data: dict = parse_config_file(config_filename)

    sim_engine: SimulationEngine
    if data['simulator'].lower() == "copasi":
        sim_engine = COPASIEngine()
    else:
        raise ValueError("At the moment we opnly support COPASI as SBML simulator.")


    if "db_config_filename" in data:
        db_configuration_info = parse_config_file(data["db_config_filename"])
        data['files']['treatments'] = None
    else:
        db_configuration_info = None

    if 'reference_treatments_ids' in data:
        reference_treatments_ids = data['reference_treatments_ids']
    else:
        reference_treatments_ids = None

    if 'exclude_from_initialization' in data['files']:
        f = open(data['files']['exclude_from_initialization'])
        exclude_text = f.read()
        f.close()
        exclude_init = json.loads(exclude_text)
    else: exclude_init = []

    initialization_model, admissibility_model, treatments = \
        initialise_model_with_PEtab_files_generation(data['files'],
                                                     sim_engine,
                                                     data['absolute_tolerance_initialization'],
                                                     data['relative_tolerance_initialization'],
                                                     data['absolute_tolerance_admissibility'],
                                                     data['relative_tolerance_initialization'],
                                                     data['time_step'],
                                                     has_db="db_config_filename" in data)
    init_horizon = float(data['initialization_horizon'])
    adm_horizon = float(data['admissibility_horizon'])
    sample_n_val: int = int(data['sample_n']) if not sample_n else sample_n
    sample_skip_val: int = int(data['sample_skip']) if sample_skip is None else sample_skip
    sample_start_val: int = int(data['sample_start']) if sample_start is None else sample_start
    sample_end_val: int = int(data['sample_end']) if not sample_end else sample_end
    dump_filename_val: str = data['vp_dump_filename'] if not dump_filename else dump_filename
    dump_every: int = data['dump_every']
    random_seed: int = int(data['random_seed'])
    sample_method: str = data['sample_method']

    if sample_method not in ['halton', 'latin hypercube sampling', 'lhs', 'grid']:
        raise ValueError(f"Sampling method {sample_method} unknown or not supported.")

    return initialization_model, admissibility_model, sim_engine, init_horizon, adm_horizon, sample_n_val, sample_skip_val, \
           treatments, dump_filename_val, dump_every, random_seed, sample_method, sample_start_val, sample_end_val, \
           db_configuration_info, reference_treatments_ids, exclude_init




def get_parameter_space(parameter_df: DataFrame) -> Set[Parameter]:
    params: Set[Parameter] = set()
    for param_id, data in parameter_df.iterrows():
        params.add(Parameter(str(param_id), data.parameterName,
                             data.lowerBound, data.upperBound, data.nominalValue,
                             data.distribution, data.mu, data.sigma, data.granularity))
    return params


def get_observable_formula(formula: str) -> Tuple[Callable, List[str]]:
    pattern = re.compile(r"(^[A-Za-z0-9_]+)\(([^(]+)\)$")
    match = pattern.match(formula)
    if not match:
        return Identity, [formula]
    function_name, expressions_str = match.groups()
    obs_function = getFunction(function_name)
    if not obs_function:
        return Identity, [formula]
    expressions: List[str] = [s.strip() for s in expressions_str.split(',')]
    return obs_function, expressions


def get_objective(objective_df: DataFrame) -> Observable:
    data = objective_df.iloc[0]

    func, expressions = get_observable_formula(data.observableFormula)

    result = Observable(data.name, data.observableName, expressions, function=func,
                        lower_bound=data.lowerBound, upper_bound=data.upperBound)
    return result


def get_constraints(constraints_df: DataFrame) -> Set[Observable]:
    result: Set[Observable] = set()
    for obj_id, data in constraints_df.iterrows():
        func, expressions = get_observable_formula(data.observableFormula)
        result.add(Observable(str(obj_id), data.observableName, expressions, function=func))

    return result


def get_fast_constraints(constraints_df: DataFrame) -> Set[FastObservable]:
    result: Set[FastObservable] = set()
    for obj_id, data in constraints_df.iterrows():
        func, expressions = get_observable_formula(data.observableFormula)
        result.add(FastObservable(str(obj_id), data.observableName, expressions, function=func))
    return result


def get_conditions(conditions_df: DataFrame) -> Dict[str, Dict[str, float]]:
    cds: Dict[str, Dict[str, float]] = dict()

    for cd_id, params in conditions_df.iterrows():
        cd_id_str = str(cd_id)
        cds[cd_id_str] = dict()
        for name, value in params.items():
            cds[cd_id_str][name] = value
    return cds


def initialise_model_with_PEtab_files_synthesis(files: Dict[str, str], sim_engine: SimulationEngine,
                                                abs_tol, rel_tol, time_step, has_db:bool = False) -> Tuple[Model, Dict[str, Dict[str, float]], Dict[str, Dict[str, float]]]:
    obj_problem = petab.problem.Problem.from_files(sbml_file=files['model'],
                                                   parameter_file=files['parameters'],
                                                   observable_files=files['objective'],
                                                   condition_file=files['virtual_patients'])

    eff_problem = petab.problem.Problem.from_files(sbml_file=files['model'],
                                                   parameter_file=files['parameters'],
                                                   observable_files=files['efficacy'],
                                                   condition_file=files['reference_treatments'])

    constr_problem = petab.problem.Problem.from_files(sbml_file=files['model'],
                                                      parameter_file=files['parameters'],
                                                      observable_files=files['constraints'])

    fast_problem = petab.problem.Problem.from_files(sbml_file=files['model'],
                                                    parameter_file=files['parameters'],
                                                    observable_files=files['fast_constraints'])

    
    

    if 'observed_outputs' in files:
        f = open(files['observed_outputs'])
        observed_outputs_text = f.read()
        f.close()
        observed_outputs = json.loads(observed_outputs_text)
    else:
        observed_outputs = None

    parameter_space: Set[Parameter] = get_parameter_space(obj_problem.parameter_df)
    objective: Observable = get_objective(obj_problem.observable_df)
    efficacy_constraints: Set[Observable] = get_constraints(eff_problem.observable_df)
    treatment_constraints: Set[Observable] = get_constraints(constr_problem.observable_df)
    treatment_fast_constraints: Set[FastObservable] = get_fast_constraints(fast_problem.observable_df)
    #virtual_patients: Dict[str, Dict[str, float]] = get_conditions(obj_problem.condition_df)
    #reference_treatments: Dict[str, Dict[str,float]] = get_conditions(eff_problem.condition_df)
    
    if has_db:
        reference_treatments = None
        virtual_patients = None
    else:
        if files['virtual_patients']:
            virtual_patients: Dict[str, Dict[str, float]] = get_conditions(obj_problem.condition_df)
        else:
            virtual_patients = dict()
            
        if files['reference_treatments']:
            reference_treatments: Dict[str, Dict[str, float]] = get_conditions(eff_problem.condition_df)
        else:
            reference_treatments = dict()

    model: Model = Model(sim_engine, files['model'], abs_tol, rel_tol, time_step, observed_outputs=observed_outputs)
    model.set_parameter_space(parameter_space)
    model.objective = objective
    model.feasibility_constraints = efficacy_constraints
    model.hard_constraints = treatment_constraints
    model.fast_constraints = treatment_fast_constraints
    return model, virtual_patients, reference_treatments


def initialise_model_with_PEtab_files_generation(files: Dict[str, str], sim_engine: SimulationEngine,
                                                 abs_tol_init, rel_tol_init,
                                                 abs_tol_adm, rel_tol_adm,
                                                 time_step, has_db:bool= False) \
        -> Tuple[Model, Model, Dict[str, Dict[str, float]]]:

    init_problem = petab.problem.Problem.from_files(sbml_file=files['initialization_model'],
                                                    parameter_file=files['parameters'],
                                                    observable_files=files['initialization_constraints'])
    adm_problem = petab.problem.Problem.from_files(sbml_file=files['admissibility_model'],
                                                   parameter_file=files['treatment_parameters'],
                                                   observable_files=files['admissibility_constraints'],
                                                   condition_file=files['treatments'])

    resp_problem = petab.problem.Problem.from_files(sbml_file=files['admissibility_model'],
                                                    parameter_file=files['treatment_parameters'],
                                                    observable_files=files['response_constraints'], )

    resp_value_problem = petab.problem.Problem.from_files(sbml_file=files['admissibility_model'],
                                                    parameter_file=files['treatment_parameters'],
                                                    observable_files=files['response_value'], )

    parameter_space: Set[Parameter] = get_parameter_space(init_problem.parameter_df)

    if has_db:
        treatments = None
    else:
        if files['treatments']:
            treatments: Dict[str, Dict[str, float]] = get_conditions(adm_problem.condition_df)
        else:
            treatments = dict()

    if 'observed_outputs_initialization' in files:
        f = open(files['observed_outputs_initialization'])
        observed_outputs_init_text = f.read()
        f.close()
        observed_outputs_initialization = json.loads(observed_outputs_init_text)
    else:
        observed_outputs_initialization = None

    if 'observed_outputs_admissibility' in files:
        f = open(files['observed_outputs_admissibility'])
        observed_outputs_adm_text = f.read()
        f.close()
        observed_outputs_admissibility = json.loads(observed_outputs_adm_text)
    else:
        observed_outputs_admissibility = None


    admissibility_constraints: Set[Observable] = get_constraints(adm_problem.observable_df)
    initialization_constraints: Set[Observable] = get_constraints(init_problem.observable_df)
    response_constraints: Set[Observable] = get_constraints(resp_problem.observable_df)
    treatment_results: Set[Observable] = get_constraints(resp_value_problem.observable_df)

    initialization_model: Model = Model(sim_engine, files['initialization_model'], abs_tol_init, rel_tol_init,
                                        time_step, observed_outputs=observed_outputs_initialization)
    initialization_model.set_parameter_space(parameter_space)
    initialization_model.admissibility_constraints = admissibility_constraints
    initialization_model.initialization_constraints = initialization_constraints

    admissibility_model: Model = Model(sim_engine, files['admissibility_model'], abs_tol_adm, rel_tol_adm,
                                       time_step, observed_outputs=observed_outputs_admissibility)
    admissibility_model.set_parameter_space(parameter_space)
    admissibility_model.admissibility_constraints = admissibility_constraints
    admissibility_model.response_constraints = response_constraints
    admissibility_model.treatment_results = treatment_results

    return initialization_model, admissibility_model, treatments


def get_db_configuration_info(db_config_filename: str) -> dict:
    # TODO fill in
    return dict()



def parse_config_file(config_filename: str) -> dict:
    f = open(config_filename)
    data: dict = yaml.load(f, Loader=yaml.FullLoader)
    f.close()
    return data
