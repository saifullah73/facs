# FACS: Flu And Coronavirus Simulator

Full documentation can be found at: http://facs.readthedocs.io

## How to run the code
To run a simple simulation of a basic test dataset, type:
`python3 run.py --location=test --transition_scenario=extend-lockdown --transition_mode=1 --output_dir=.`

To run a simulation of the Borough of Brent, type:
`python3 run.py --location=brent --transition_scenario=extend-lockdown --transition_mode=1 --output_dir=.`

To run a simulation of the Islamabad, type:
`python3 run.py --location=islamabad --transition_scenario=smart-lockdown --transition_mode=1 --output_dir=output`  

To run a simulation of the Abbottabad, type:
`python3 run.py --location=abbottabad --transition_scenario=abbottabad-lockdown --transition_mode=1 --output_dir=output`

To run a simulation of Brunel University London, type:
`python3 run_campus.py --location=brunel --transition_scenario=extend-lockdown --transition_mode=1 --output_dir=.`

Outputs are written as CSV files in the output\_dir. E.g. for the test run you will get:
covid\_out\_infections.csv
test-extend-lockdown-62.csv

There is a hardcoded lockdown in run.py which is representative for the UK. This can be disabled by selecting the transition scenario "no-measures".

We also included a simple plotting script. This can be called e.g. as follows:
`python3 PlotSEIR.py test-extend-lockdown-62.csv test`

## Advanced usage

### Running with a specific data directory
Flacs can be run with a different input data directory as follows:
`python3 run.py --location=brent --transition_scenario=extend-lockdown --transition_mode=1 --output_dir=. --data_dir=/home/derek/covid19-postprocess/flacs_input_private`

### Performing quick tests
Quick tests can be triggered with the '-q' flag. This sets the house ratio to 100 (default is 2), which means that households will be less well distributed.
However, as a number of calculations are performed on the house level (not the household level), this setting speeds up the code by up to an order of magnitude.
`python3 run.py -q --location=brent --transition_scenario=extend-lockdown --transition_mode=1 --output_dir=.`

