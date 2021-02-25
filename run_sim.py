import argparse
import csv
import datetime
import sys
from os import makedirs, path

import facs.facs as facs
import facs.measures as measures
import numpy as np
from readers import read_age_csv
from readers import read_building_csv
from readers import read_cases_csv
from readers import read_disease_yml
from readers import read_poly


def run_simulation(queue, running, location="Islamabad", transition_scenario="extend-lockdown", ci_multiplier="0.625",
                   starting_infections="500", transition_day="30", sim_length="365"):
    queue.put("Simulation running...")
    print("transition_scenario = %s" % transition_scenario)
    print("Location = %s" % location)
    print("transition_day = %s" % transition_day)
    print("ci_multiplier = %s" % ci_multiplier)
    print("starting_infections  = %s" % starting_infections)
    print("sim_length  = %s" % sim_length)
    # Instantiate the parser
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--location', action="store", default="islamabad")
    # parser.add_argument('--transition_scenario', action="store", default="extend-lockdown")
    # parser.add_argument('--transition_mode', action="store",
    #                     type=int, default='1')
    # parser.add_argument('--ci_multiplier', action="store",
    #                     type=float, default='0.625',
    #                     help="Multiplier set for Case Isolation which represents the ratio of out-of-house interactions for Covid patients relative to the default interaction rate. Default value comes from Imp Report 9.")
    # parser.add_argument('--output_dir', action="store", default=".")
    # parser.add_argument('--data_dir', action="store", default="covid_data")
    # parser.add_argument('-s', '--starting_infections', action="store", default="500")
    # parser.add_argument('--start_date', action="store", default="3/1/2020")
    # parser.add_argument('-q', '--quicktest', action="store_true",
    #                     help="set house_ratio to 100 to do quicker (but less accurate) runs for populous regions.")
    # parser.add_argument('-g', '--generic_outfile', action="store_true",
    #                     help="Write main output to out.csv instead of a scenario-specific named file.")
    # parser.add_argument('--dbg', action="store_true", help="Write additional outputs to help debugging")
    # parser.add_argument('--transition_day', action="store", help="Day on which the transition should take place",
    #                     default=30)
    # parser.add_argument('--sim_length', action="store", help="Number of days for which the simulation should run",
    #                     default=365)
    # args = parser.parse_args()
    # print(args)

    house_ratio = 2
    # if args.quicktest:
    #     house_ratio = 100
    # location = args.location
    # ci_multiplier = float(args.ci_multiplier)
    ci_multiplier = float(ci_multiplier)
    # transition_scenario = args.transition_scenario.lower()
    transition_mode = 1
    # output_dir = args.output_dir
    output_dir = "output"
    data_dir = "covid_data"

    transition_day = int(transition_day)
    sim_length = int(sim_length)
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

    # constant = 0  # constant of 0 means simulation start on 26th Feb
    # transition_day = -1
    # if transition_mode == 1:
    #     transition_day = (27-constant) #lockdown on 24th March
    # # if transition_mode == 2:
    # #     transition_day = 93
    # # if transition_mode == 3:
    # #     transition_day = 108
    # # if transition_mode == 4:
    # #     transition_day = 123
    # # if transition_mode > 10:
    # #     transition_day = transition_mode

    # check the transition scenario argument
    AcceptableTransitionScenario = ['no-measures', 'extend-lockdown',
                                    'open-all', 'open-schools', 'open-shopping',
                                    'open-leisure', 'work50', 'work75',
                                    'work100', 'dynamic-lockdown', 'periodic-lockdown', 'uk-forecast', 'smart-lockdown',
                                    'abbottabad-lockdown']

    if transition_scenario not in AcceptableTransitionScenario:
        queue.put("Error! The input transition scenario, %s , is not VALID" %
                  transition_scenario)
        print("\nError !\n\tThe input transition scenario, %s , is not VALID" %
              transition_scenario)
        print("\tThe acceptable inputs are : [%s]" %
              (",".join(AcceptableTransitionScenario)))
        sys.exit()

    # check if output_dir is exists
    if not path.exists(output_dir):
        makedirs(output_dir)

    # outfile = "{}/{}-{}-{}.csv".format(output_dir,
    #                                    location,
    #                                    transition_scenario,
    #                                    transition_day)

    outfile = 'output/output.csv'

    # if args.generic_outfile:
    #     outfile = "{}/out.csv".format(output_dir)

    # if transition_scenario in ["extend-lockdown","dynamic-lockdown","periodic-lockdown","uk-forecast"]:
    #     end_time = 253 #starting from 29th Feb till 8th Nov
    #   # end_time = 730
    # elif transition_scenario in ['smart-lockdown','abbottabad-lockdown']:
    #     end_time = 365
    # end_time = 365 # for a full year
    end_time = sim_length

    print("Running basic Covid-19 simulation kernel.")
    print("scenario = %s" % location)
    print("transition_scenario = %s" % transition_scenario)
    print("transition_mode = %s" % transition_mode)
    print("transition_day = %s" % transition_day)
    print("end_time = %s" % end_time)
    print("output_dir  = %s" % output_dir)
    print("outfile  = %s" % outfile)
    print("data_dir  = %s" % data_dir)

    e = facs.Ecosystem(end_time)

    e.ci_multiplier = ci_multiplier
    e.ages = read_age_csv.read_age_csv("{}/age-distr.csv".format(data_dir), location)

    # queue.put(f"Age distribution in system: {e.ages} {sys.stderr}")
    print("age distribution in system:", e.ages, file=sys.stderr)

    e.disease = read_disease_yml.read_disease_yml(
        "{}/disease_covid19.yml".format(data_dir))

    building_file = "{}/{}_buildings.csv".format(data_dir, location)
    # queue.put("Reading Regions.....")
    print("Reading Regions.....")
    regions = read_poly.readPolyFiles("{}_poly_files".format(location))
    e.set_regions(regions)
    # queue.put("Total Regions read: " + str(len(regions)))
    print("Total Regions read: " + str(len(regions)))
    # queue.put("Regions are " + str(list(regions.keys())))
    print("Regions are " + str(list(regions.keys())))
    read_building_csv.read_building_csv(e,
                                        building_file,
                                        "{}/building_types_map.yml".format(data_dir),
                                        house_ratio=house_ratio, workspace=12, office_size=1600, household_size=6.45,
                                        work_participation_rate=0.5)
    # queue.put("Assigning regions to agents.... ")
    print("Assigning regions to agents.... ")
    e.assign_region_to_agents()
    # queue.put("Done")
    print("Done")
    e.test_agents_in_regions()
    # house ratio: number of households per house placed (higher number adds noise, but reduces runtime
    # And then 3 parameters that ONLY affect office placement.
    # workspace: m2 per employee on average. (10 in an office setting, but we use 12 as some people work in more spacious environments)
    # household size: average size of each household, specified separately here.
    # work participation rate: fraction of population in workforce, irrespective of age

    # print("{}/{}_cases.csv".format(data_dir, location))
    # Can only be done after houses are in.
    # read_cases_csv.read_cases_csv(e,
    #                              "{}/{}_cases.csv".format(data_dir, location),
    #                              start_date="3/1/2020",
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
    if starting_infections:
        starting_num_infections = int(starting_infections)
    # queue.put("Starting infection: " + str(starting_num_infections))
    print("Starting infection: " + str(starting_num_infections))
    for i in range(0, 10):
        e.add_infections(int(starting_num_infections / 10), i - 19)
    # queue.put("THIS SIMULATIONS HAS {} AGENTS.".format(e.num_agents))
    print("THIS SIMULATIONS HAS {} AGENTS.".format(e.num_agents))
    e.time = -20
    e.print_header(outfile)
    for i in range(0, 20):
        e.evolve(reduce_stochasticity=False)
        print(e.time)
        if True:
            e.update_and_print_status(outfile, output_dir)
        else:
            e.update_and_print_status(outfile, output_dir=output_dir, silent=True)

    track_trace_limit = 0.2 + transition_mode * 0.1

    for t in range(0, end_time):

        if t == transition_day:
            if transition_scenario == "extend-lockdown":
                measures.full_lockdown(e)
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

        if t > 24 and transition_scenario == "dynamic-lockdown" and t % 7 == 0:
            print("Dynamic lockdown test: {}/100".format(e.num_hospitalised), file=sys.stderr)
            measures.enact_dynamic_lockdown(e, measures.work50, e.num_hospitalised, 100)
        if t > 24 and transition_scenario == "periodic-lockdown" and t % 30 == 0:
            print("Periodic lockdown with 30 day interval.")
            measures.enact_periodic_lockdown(e, measures.work50)

        # Recording of existing measures
        if transition_scenario in ["uk-forecast"]:
            measures.uk_lockdown_forecast(e, t, transition_mode)
        if transition_scenario in ["smart-lockdown"]:
            # measures.smart_lockdown_hard_islamabad(e,t)
            measures.automatic_smart_lockdown(e, t, 100)
        if transition_scenario in ["abbottabad-lockdown"]:
            measures.abbottabad_lockdown(e, t)
        elif transition_scenario not in ["no-measures"]:
            pass
            # measures.uk_lockdown_existing(e, t, track_trace_limit=track_trace_limit)

        # Propagate the model by one time step.
        print(str(t))
        queue.put(f"Simulation day {t} out of {end_time}")
        print(e.region_under_lockdown)
        e.evolve()
        e.update_and_print_status(outfile, output_dir)

    # calculate cumulative sums.
    e.add_cum_column(outfile, ["dead", "num hospitalisations today", "infectious", "num infections today"])
    queue.put("Simulation complete.")
    print("Simulation complete.", file=sys.stderr)
    queue.put("Time taken : " + str(datetime.datetime.now() - begin_time) + " HH:MM:SS:milliseconds")
    print("Time taken : " + str(datetime.datetime.now() - begin_time) + " HH:MM:SS:milliseconds")
    running = 0
