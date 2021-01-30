import facs.facs as facs
import facs.measures as measures
from readers import read_age_csv
from readers import read_poly
import numpy as np
from readers import read_building_csv
from readers import read_cases_csv
from readers import read_disease_yml
import sys
import datetime

from os import makedirs, path
import argparse
import csv
from pprint import pprint
"""
Parameter Description:
ci_multiplier: Multiplier set for Case Isolation which represents the ratio of out-of-house interactions for Covid patients relative to the default interaction rate. Default value comes from Imp Report 9.
house ratio: number of households per house placed (higher number adds noise, but reduces runtime
workspace: m2 per employee on average. (10 in an office setting, but we use 12 as some people work in more spacious environments)
household size: average size of each household, specified separately here.
work participation rate: fraction of population in workforce, irrespective of age
"""


'''
First case of coronavirus in Islamabad was 29th Feb, so we are assuming that first day of our simulation if 29th of Feb, (warmup starts from 9th Feb) 
'''
if __name__ == "__main__":

    # Instantiate the parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--location', action="store", default="islamabad")
    parser.add_argument('--transition_scenario', action="store", default="extend-lockdown")
    parser.add_argument('--transition_mode', action="store",
                        type=int, default='1')
    parser.add_argument('--ci_multiplier', action="store",
                        type=float, default='0.625', help="Multiplier set for Case Isolation which represents the ratio of out-of-house interactions for Covid patients relative to the default interaction rate. Default value comes from Imp Report 9.")
    parser.add_argument('--output_dir', action="store", default=".")
    parser.add_argument('--data_dir', action="store", default="covid_data")
    parser.add_argument('-s','--starting_infections', action="store", default="500")
    parser.add_argument('--start_date', action="store", default="3/1/2020")
    parser.add_argument('-q', '--quicktest', action="store_true", help="set house_ratio to 100 to do quicker (but less accurate) runs for populous regions.")
    parser.add_argument('-g', '--generic_outfile', action="store_true", help="Write main output to out.csv instead of a scenario-specific named file.")
    parser.add_argument('--dbg', action="store_true", help="Write additional outputs to help debugging")
    args = parser.parse_args()
    print(args)

    house_ratio = 2
    if args.quicktest:
      house_ratio = 100
    location = args.location
    ci_multiplier = float(args.ci_multiplier)
    transition_scenario = args.transition_scenario.lower()
    transition_mode = args.transition_mode
    output_dir = args.output_dir
    data_dir = args.data_dir

    begin_time = datetime.datetime.now()

    # if simsetting.csv exists -> overwrite the simulation setting parameters
    if path.isfile('simsetting.csv'):
        with open('simsetting.csv', newline='') as csvfile:
            values = csv.reader(csvfile)
            for row in values:
                if len(row) > 0:  # skip empty lines in csv
                    if row[0][0] == "#":
                        pass
                    elif row[0].lower() == "transition_scenario":
                        transition_scenario = str(row[1]).lower()
                    elif row[0].lower() == "transition_mode":
                        transition_mode = int(row[1])


    # transition_day = -1
    # if transition_mode == 1:
    #     transition_day = 77  # 15th of April
    # if transition_mode == 2:
    #     transition_day = 93  # 31st of May
    # if transition_mode == 3:
    #     transition_day = 108  # 15th of June
    # if transition_mode == 4:
    #     transition_day = 123  # 30th of June
    # if transition_mode > 10:
    #     transition_day = transition_mode

    constant = 13
    transition_day = -1
    if transition_mode == 1:
        transition_day = (27-constant) #lockdown on 24th March
    # if transition_mode == 2:
    #     transition_day = 93
    # if transition_mode == 3:
    #     transition_day = 108
    # if transition_mode == 4:
    #     transition_day = 123
    # if transition_mode > 10:
    #     transition_day = transition_mode

    # check the transition scenario argument
    AcceptableTransitionScenario = ['no-measures', 'extend-lockdown',
                                    'open-all', 'open-schools', 'open-shopping',
                                    'open-leisure', 'work50', 'work75',
                                    'work100', 'dynamic-lockdown', 'periodic-lockdown','uk-forecast','smart-lockdown','abbottabad-lockdown']

    if transition_scenario not in AcceptableTransitionScenario:
        print("\nError !\n\tThe input transition scenario, %s , is not VALID" %
              (transition_scenario))
        print("\tThe acceptable inputs are : [%s]" %
              (",".join(AcceptableTransitionScenario)))
        sys.exit()

    # check if output_dir is exists
    if not path.exists(output_dir):
        makedirs(output_dir)

    outfile = "{}/{}-{}-{}.csv".format(output_dir,
                                       location,
                                       transition_scenario,
                                       transition_day)
    if args.generic_outfile:
      outfile = "{}/out.csv".format(output_dir)


    if transition_scenario in ["extend-lockdown","dynamic-lockdown","periodic-lockdown","uk-forecast"]:
        end_time = 253 #starting from 29th Feb till 8th Nov
      # end_time = 730
    elif transition_scenario in ['smart-lockdown','abbottabad-lockdown']:
        end_time = 365
    end_time = 365 # for a full year

    print("Running basic Covid-19 simulation kernel.")
    print("scenario = %s" % (location))
    print("transition_scenario = %s" % (transition_scenario))
    print("transition_mode = %d" % (transition_mode))
    print("transition_day = %d" % (transition_day))
    print("end_time = %d" % (end_time))
    print("output_dir  = %s" % (output_dir))
    print("outfile  = %s" % (outfile))
    print("data_dir  = %s" % (data_dir))

    e = facs.Ecosystem(end_time)

    e.ci_multiplier = ci_multiplier
    e.ages = read_age_csv.read_age_csv("{}/age-distr.csv".format(data_dir), location)

    print("age distribution in system:", e.ages, file=sys.stderr)

    e.disease = read_disease_yml.read_disease_yml(
        "{}/disease_covid19.yml".format(data_dir))

    building_file = "{}/{}_buildings.csv".format(data_dir, location)
    print("Reading Regions.....")
    regions = read_poly.readPolyFiles("{}_poly_files".format(location))
    e.set_regions(regions)
    print("Total Regions read: " + str(len(regions)))
    print("Regions are " + str(list(regions.keys())))
    read_building_csv.read_building_csv(e,
                                        building_file,
                                        "{}/building_types_map.yml".format(data_dir),
                                        house_ratio=house_ratio, workspace=12, office_size=1600, household_size=6.45, work_participation_rate=0.5)

    print("Assigning regions to agents.... ")
    e.assign_region_to_agents()
    print("Done")
    e.test_agents_in_regions()
    # house ratio: number of households per house placed (higher number adds noise, but reduces runtime
    # And then 3 parameters that ONLY affect office placement.
    # workspace: m2 per employee on average. (10 in an office setting, but we use 12 as some people work in more spacious environments)
    # household size: average size of each household, specified separately here.
    # work participation rate: fraction of population in workforce, irrespective of age

    #print("{}/{}_cases.csv".format(data_dir, location))
    # Can only be done after houses are in.
    #read_cases_csv.read_cases_csv(e,
    #                              "{}/{}_cases.csv".format(data_dir, location),
    #                              start_date=args.start_date,
    #                              date_format="%m/%d/%Y")

    starting_num_infections = 500
    if location == "test":
      starting_num_infections = 10
    if location == "i8":
        starting_num_infections = 10
    if location == "abbottabad":
        starting_num_infections = 10
    if location == "islamabad":
        starting_num_infections = 20
    if args.starting_infections:
      starting_num_infections = int(args.starting_infections)

    for i in range(0,10):
      e.add_infections(int(starting_num_infections/10), i-19)
    # e.add_infections(1, -9)
    # e.add_infections(1, -8)

    print("THIS SIMULATIONS HAS {} AGENTS.".format(e.num_agents))
    e.time = -20
    e.print_header(outfile)
    for i in range(0, 20):
        e.evolve(reduce_stochasticity=False)
        print(e.time)
        if args.dbg:
            e.update_and_print_status(outfile,output_dir)
        else:
            e.update_and_print_status(outfile,output_dir=output_dir,silent=True)

    track_trace_limit = 0.2 + transition_mode*0.1



    for t in range(0, end_time):

        if t == transition_day:
            if transition_scenario == "extend-lockdown":
                pass
                # measures.full_lockdown(e)
            elif transition_scenario == "open-all":
                e.remove_all_measures()
            elif transition_scenario == "open-schools":
                e.remove_closure("school")
            elif transition_scenario == "open-shopping":
                e.undo_partial_closure("shopping", 0.8)
            elif transition_scenario == "open-leisure":
                e.remove_closure("leisure")
            elif transition_scenario == "work50":
                measures.work50(e)
            elif transition_scenario == "work75":
                measures.work75(e)
            elif transition_scenario == "work100":
                measures.work100(e)

        if t>24 and transition_scenario == "dynamic-lockdown" and t%7 == 0:
            print("Dynamic lockdown test: {}/100".format(e.num_hospitalised), file=sys.stderr)
            measures.enact_dynamic_lockdown(e, measures.work50, e.num_hospitalised, 100)
        if t>24 and transition_scenario == "periodic-lockdown" and t%30 == 0:
            print("Periodic lockdown with 30 day interval.")
            measures.enact_periodic_lockdown(e, measures.work50)

        # Recording of existing measures
        if transition_scenario in ["uk-forecast"]:
            measures.uk_lockdown_forecast(e, t, transition_mode)
        if transition_scenario in ["smart-lockdown"]:
            measures.smart_lockdown_hard_islamabad(e,t)
        if transition_scenario in ["abbottabad-lockdown"]:
            measures.abbottabad_lockdown(e,t)
        elif transition_scenario not in ["no-measures"]:
            pass
            # measures.uk_lockdown_existing(e, t, track_trace_limit=track_trace_limit)

        # Propagate the model by one time step.
        print(str(t))
        print(e.region_under_lockdown)
        e.evolve()
        e.update_and_print_status(outfile,output_dir)

    # calculate cumulative sums.
    e.add_cum_column(outfile, ["dead", "num hospitalisations today", "infectious", "num infections today"])

    print("Simulation complete.", file=sys.stderr)
    print("Time taken : "+ str(datetime.datetime.now()-begin_time) + " HH:MM:SS:milliseconds")
