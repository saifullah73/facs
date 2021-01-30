import sys

def full_lockdown(e):
  e.remove_all_measures()
  e.add_closure("school", 0)
  e.add_closure("leisure", 0)
  e.add_partial_closure("shopping", 0.8)
  # mimicking a 75% reduction in social contacts.
  e.add_social_distance_imp9()
  e.add_work_from_home()
  e.add_case_isolation()
  e.add_household_isolation()
  #remove later
  # e.track_trace_multiplier = 0.8


def abbottabad_lockdown(e,t):
  # e.hospital_protection_factor = 0.4
  # e.track_trace_multiplier = 0.8
  # if t == 16:  # 13th March
  #   # school underlockdown, first major response to covid
  #   e.remove_all_measures()
  #   e.add_closure("school", 0)
  #   e.add_case_isolation()
  #   e.add_household_isolation()
  # if t == 27: #24th March
  #   work50(e)
  # if t ==73:# remove full lockdown enacted on 24th March
  #   work75(e)
  # if t == 95: # pakistan ramps up testing
  #   e.hospital_protection_factor = 0.2
  #   e.track_trace_multiplier = 0.5
  # if t == 112:
  #   e.add_region_under_lockdown("Kehal", 1, 14)
  #   e.add_region_under_lockdown("PMA.Kakul",1,14)
  #   e.add_region_under_lockdown("Jhangi.Syedan",1,14)
  # if t == 202: # 15th September
  #   work100(e) # #school reopen
  # if t == 274:
  #   e.add_closure("school", 0) # schools closed on november 24th

  # track_trace_multiplier was 0.8

  constant = 13
  e.hospital_protection_factor = 0.4
  e.track_trace_multiplier = 0.8
  if t == (16-constant):  # 13th March
    # school underlockdown, first major response to covid
    e.remove_all_measures()
    e.add_closure("school", 0)
    e.add_case_isolation()
    e.add_household_isolation()
  if t == (27-constant): #24th March
    work50(e)
  if t == (73-constant):# remove full lockdown enacted on 24th March
    work75(e)
  if t == (95 - constant): # pakistan ramps up testing
    e.hospital_protection_factor = 0.2
    e.track_trace_multiplier = 0.5
  if t == (112 - constant):
    e.add_region_under_lockdown("Kehal", 1, 14)
    e.add_region_under_lockdown("PMA.Kakul",1,14)
    e.add_region_under_lockdown("Jhangi.Syedan",1,14)
  if t == (202 - constant): # 15th September
    work100(e) # #school reopen
  if t == (274 - constant):
    e.add_closure("school", 0) # schools closed on november 24th

def automatic_smart_lockdown(e,t,threshold,days = 7):
  for region,cases in e.cases_in_regions_today.items():
    if cases >= threshold:
      strength = round(1 - (0.3/(((cases - threshold)/threshold) + 1)),2)
      print(region + " under lockdown-strength= "+str(strength)+" days= "+str(days))
      e.add_region_under_lockdown(region,1,days)


# First case recorded in Pakistan on Feburary 26th, and we start our simulation from here (20 days for warmup are performed prior)
def smart_lockdown_hard_islamabad(e,t):
  e.hospital_protection_factor = 0.4
  e.track_trace_multiplier = 0.5
  if t == 16: # 13th March
    #school underlockdown, first major response to covid
    e.remove_all_measures()
    e.add_closure("school", 0)
    e.add_case_isolation()
    e.add_household_isolation()
  if t == 27: #24th March
    full_lockdown(e)
  if t == 35: # 1st April
    #I8 under lockdown for a week
    e.add_region_under_lockdown("I8.1",1,7)
    e.add_region_under_lockdown("I8.2", 1,7)
    e.add_region_under_lockdown("I8.3", 1,7)
    e.add_region_under_lockdown("I8.4", 1,7)
    #I10 under lockdown for a week
    e.add_region_under_lockdown("I10.1", 1,7)
    e.add_region_under_lockdown("I10.2", 1,7)
    e.add_region_under_lockdown("I10.3", 1,7)
    e.add_region_under_lockdown("I10.4", 1,7)
    # G9 under lockdown for a week
    e.add_region_under_lockdown("G9.1", 1, 7)
    e.add_region_under_lockdown("G9.2", 1, 7)
    e.add_region_under_lockdown("G9.3", 1, 7)
    e.add_region_under_lockdown("G9.4", 1, 7)
    e.add_region_under_lockdown("G9.Markaz", 1, 7)
  if t ==73 :# remove full lockdown enacted on 24th March
    work50(e)
  if t == 95: # pakistan ramps up testing
    e.hospital_protection_factor = 0.2
  if t == 111: # 16th June
    # I8 under lockdown for a week
    e.add_region_under_lockdown("I8.1", 1, 7)
    e.add_region_under_lockdown("I8.2", 1, 7)
    e.add_region_under_lockdown("I8.3", 1, 7)
    e.add_region_under_lockdown("I8.4", 1, 7)
    # I10 under lockdown for a week
    e.add_region_under_lockdown("I10.1", 1, 7)
    e.add_region_under_lockdown("I10.2", 1, 7)
    e.add_region_under_lockdown("I10.3", 1, 7)
    e.add_region_under_lockdown("I10.4", 1, 7)
    # G9 under lockdown for a week
    e.add_region_under_lockdown("G9.1", 1, 7)
    e.add_region_under_lockdown("G9.2", 1, 7)
    e.add_region_under_lockdown("G9.3", 1, 7)
    e.add_region_under_lockdown("G9.4", 1, 7)
    e.add_region_under_lockdown("G9.Markaz", 1, 7)
  if t == 117: # 22nd June
    e.add_region_under_lockdown("GhauriTown.Phase1", 1, 7)
    e.add_region_under_lockdown("GhauriTown.Phase2", 1, 7)
    e.add_region_under_lockdown("GhauriTown.Phase3", 1, 7)
    e.add_region_under_lockdown("GhauriTown.Phase4A", 1, 7)
    e.add_region_under_lockdown("GhauriTown.Phase4B", 1, 7)
    e.add_region_under_lockdown("GhauriTown.Phase5", 1, 7)
    e.add_region_under_lockdown("GhauriTown.Phase5B", 1, 7)
    e.add_region_under_lockdown("GhauriTown.Phase7", 1, 7)
    e.add_region_under_lockdown("GhauriTown.VIPBlock", 1, 7)
  if t == 118: #23rd June
    e.add_region_under_lockdown("I8.3", 1, 7)
    e.add_region_under_lockdown("I8.4", 1, 7)
    e.add_region_under_lockdown("I10.2", 1, 7)
    # where is I10 markaz
  if t == 121: # 26th June
    e.add_region_under_lockdown("GhauriTown.Phase4A", 1, 7)
    e.add_region_under_lockdown("GhauriTown.Phase5", 1, 7)
  if t == 202: # 15th September
    work75(e) # school reopen
    pass # ripah medical college under lockdown
  if t == 226: # 9th Oct
    e.add_region_under_lockdown("G10.4", 0.5, 7)
    e.add_region_under_lockdown("I8.2", 0.3, 7)
    e.add_region_under_lockdown("G11.2",0.1,7)
  if t ==231: # 14th Oct
    pass
    # school at F-6/2 closed
  if t == 240: # 23rd Oct
    pass
    #Fazaia medical college closed
  if t==243: #26th Oct
    e.add_region_under_lockdown("F11.3", 0.1, 7)
    e.add_region_under_lockdown("F11.2", 0.1, 7)
    e.add_region_under_lockdown("I8.2", 0.1, 7)
    e.add_region_under_lockdown("I8.3", 0.1, 7)
    e.add_region_under_lockdown("I8.4", 0.1, 7)
    e.add_region_under_lockdown("I10.2", 0.1, 7)
    e.add_region_under_lockdown("G11.2", 0.1, 7)
    e.add_region_under_lockdown("G6.2", 0.1, 7)
  if t == 245: #28th Oct
    pass #Quaid e azam university closed
  if t == 257: # 9th November
    e.add_region_under_lockdown("I8.3", 1, 7)
    e.add_region_under_lockdown("I8.4", 1, 7)
    e.add_region_under_lockdown("G10.4",1,7)
    e.add_region_under_lockdown("G6.2",1,7)
  if t == 274:
    e.add_closure("school", 0) # schools closed on november 24th


'''
Explaination: Define parameters
'''

def uk_lockdown(e, phase=1, transition_fraction=1.0, keyworker_fraction=0.18, track_trace_limit=0.5, compliance=0.0):
  """
  Code which reflects EXISTING UK lockdown measures.
  compliance = a static modified on the (social distancing) compliance rate. Should be in range -10% to +10%.
  """
  e.remove_all_measures()
  transition_fraction = max(0.0, min(1.0, transition_fraction))
  keyworker_fraction = max(0.0, min(1.0, keyworker_fraction))

  track_trace_limit = 1.0 - track_trace_limit

  if phase == 1: # Enacted March 16th
    e.add_partial_closure("leisure", 0.5)
    e.add_social_distance(compliance=transition_fraction*0.75, mask_uptake=transition_fraction*0.05)
    # light work from home instruction, with ascending compliance to 60%.
    e.add_work_from_home(0.65*transition_fraction)
  if phase == 2: # Enacted March 23rd
    '''Explaination! : What does exclude_people means?'''
    e.add_partial_closure("school", 1.0 - keyworker_fraction, exclude_people=True)
    e.add_closure("leisure", 0)
    e.add_partial_closure("shopping", 0.6 + (transition_fraction * 0.2))
    e.add_social_distance(compliance=0.65 + compliance + (transition_fraction * 0.1), mask_uptake=0.05, mask_uptake_shopping=0.1)
    e.add_work_from_home(0.9 - keyworker_fraction + (transition_fraction * 0.1)) # www.ifs.org.uk/publications/14763 (18% are key worker in London)
  if phase == 3: # Enacted April 22nd
    e.add_partial_closure("school", 1.0 - keyworker_fraction, exclude_people=True)
    e.add_closure("leisure", 0)
    e.add_partial_closure("shopping", 0.8)
    e.add_social_distance(compliance=0.8 + compliance, mask_uptake=0.15, mask_uptake_shopping=0.2)
    e.add_work_from_home(1.0 - keyworker_fraction) # www.ifs.org.uk/publications/14763 (18% are key worker in London)
  if phase == 4: # Enacted May 13th
    e.add_partial_closure("school", 1.0 - keyworker_fraction, exclude_people=True)
    e.add_closure("leisure", 0)
    e.add_partial_closure("shopping", 0.6)
    e.add_social_distance(compliance=0.7 + compliance, mask_uptake=0.2, mask_uptake_shopping=0.3)
    e.add_work_from_home(0.7)
    e.ci_multiplier *= 0.7 # Assumption: additional directives for those with anosmia to stay home improves compliance by 30%.
  if phase == 5: # Enacted June 1st
    e.add_partial_closure("school", (1.0 - keyworker_fraction) / 2.0, exclude_people=True)
    e.add_closure("leisure", 0)
    e.add_partial_closure("shopping", 0.6)
    e.add_social_distance(compliance=0.7 + compliance, mask_uptake=0.2, mask_uptake_shopping=0.3)
    e.add_work_from_home(0.7)
    e.track_trace_multiplier = 0.8 # 80% of cases escape track and trace.
  if phase == 6: # Enacted June 15th
    e.add_partial_closure("school", (1.0 - keyworker_fraction) / 2.0, exclude_people=True)
    e.add_closure("leisure", 0)
    e.add_partial_closure("shopping", 0.2)
    e.add_social_distance(compliance=0.7 + compliance, mask_uptake=0.2, mask_uptake_shopping=0.3)
    e.add_work_from_home(0.65)
    e.traffic_multiplier = 0.125 # https://data.london.gov.uk/dataset/coronavirus-covid-19-mobility-report
    e.enforce_masks_on_transport = True
    e.track_trace_multiplier = track_trace_limit # 50% of cases escape track and trace.
  if phase == 7: # Enacted July 4th
    e.add_partial_closure("school", (1.0 - keyworker_fraction) / 2.0, exclude_people=True)
    e.add_partial_closure("leisure", 0.8)
    e.add_partial_closure("shopping", 0.1)
    e.add_social_distance(compliance=0.7 + compliance, mask_uptake=0.2, mask_uptake_shopping=0.3)
    e.add_work_from_home(0.5)
    e.traffic_multiplier = 0.2 # https://data.london.gov.uk/dataset/coronavirus-covid-19-mobility-report
    e.track_trace_multiplier = track_trace_limit # 50% of cases escape track and trace.
  if phase == 8: # Enacted July 15th
    e.add_partial_closure("school", 0.8) # Assuming some kids go to summer camps, but 80% of school-like activities are not taking place due to holidays.
    e.add_partial_closure("leisure", 0.3)
    e.add_social_distance(compliance=0.7 + compliance, mask_uptake=0.2, mask_uptake_shopping=0.8)
    e.add_work_from_home(0.5)
    e.track_trace_multiplier = track_trace_limit # 50% of cases escape track and trace.
  if phase == 9: # Enacted Sept 1st
    e.add_social_distance(compliance=0.7 + compliance, mask_uptake=0.2, mask_uptake_shopping=0.8)
    e.add_work_from_home(0.3)
    e.traffic_multiplier = 0.25 # https:///data.london.gov.uk/dataset/coronavirus-covid-19-mobility-report (estimate)
    e.track_trace_multiplier = track_trace_limit # 50% of cases escape track and trace.
  if phase == 10: # Enacted Sept 22nd
    e.add_social_distance(compliance=0.7 + compliance, mask_uptake=0.2, mask_uptake_shopping=0.8)
    e.add_work_from_home(0.5) # Work from home directive reinstated by government.
    e.traffic_multiplier = 0.25 # https://data.london.gov.uk/dataset/coronavirus-covid-19-mobility-report (estimate)
    e.track_trace_multiplier = track_trace_limit # 50% of cases escape track and trace.


  # mimicking a 75% reduction in social contacts.
  #e.add_social_distance_imp9()

  e.add_case_isolation()
  e.add_household_isolation()


def update_hospital_protection_factor_uk(e, t):
  if t == 10:
    e.hospital_protection_factor = 0.4
  if t == 20:
    e.hospital_protection_factor = 0.37
  if t == 30: # start of testing ramp up in early april.
    e.hospital_protection_factor = 0.34
  if t == 40:
    e.hospital_protection_factor = 0.29
  if t == 50:
    e.hospital_protection_factor = 0.23
  if t == 60: # testing ramped up considerably by the end of April.
    e.hospital_protection_factor = 0.16
  if t == 80:
    e.hospital_protection_factor = 0.12
  if t == 100:
    e.hospital_protection_factor = 0.10
  if t == 120:
    e.hospital_protection_factor = 0.08


def uk_lockdown_scenarios(e, t, step, vaccine=100, track_trace_multiplier = 0.5):
  pass

  """
  e.remove_all_measures()

  if step == 2: # June 1st, planned school opening
    e.add_partial_closure("school", 0.5) #school times halved
    e.add_partial_closure("school", 0.75, exclude_people=True) #25% of students go.
    e.add_closure("leisure", 0)
    e.add_partial_closure("shopping", 0.6)
    e.add_social_distance(compliance=0.7, mask_uptake=0.2)
    e.add_work_from_home(0.7)

  if step == 3: # 70% of students go to  school, first leisure locs open
    e.add_partial_closure("school", 0.5)
    e.add_partial_closure("school", 0.3, exclude_people=True) #70% of students go.
    e.add_partial_closure("leisure", 0.75)
    e.add_partial_closure("shopping", 0.4)
    e.add_social_distance(compliance=0.7, mask_uptake=0.3)
    e.add_work_from_home(0.4)

  if step == 4: # all schools open
    e.add_partial_closure("school", 0.5)
    e.add_partial_closure("leisure", 0.5)
    e.add_partial_closure("shopping", 0.2)
    e.add_social_distance(compliance=0.7, mask_uptake=0.3)
    e.add_work_from_home(0.3)

  if step == 5: # track and trace in place.
    e.add_partial_closure("school", 0.5)
    e.add_partial_closure("leisure", 0.5)
    e.add_social_distance(compliance=0.7, mask_uptake=0.3)
    e.add_work_from_home(0.25)
    # Assumption: track and trace will render case isolation twice as effective.
    e.ci_multiplier *= track_trace_multiplier

  if step == 6: # vaccine in place. Schools fully open.
    e.add_social_distance(compliance=0.7, mask_uptake=0.3)
    e.add_work_from_home(0.25)
    e.vaccinations_available += vaccine

  if step == 7: # 50% vaccination coverage.
    e.add_social_distance(compliance=0.7, mask_uptake=0.3)
    e.add_work_from_home(0.25)
    e.vaccinations_available += vaccine*10

  e.add_case_isolation()
  e.add_household_isolation()
  """
'''
Explaination: Define function
'''
def uk_lockdown_existing(e, t, track_trace_limit=0.5):
  update_hospital_protection_factor_uk(e,t)

  # traffic multiplier = relative reduction in travel minutes^2 / relative reduction service minutes
  # Traffic: Mar 10: 90% (estimate), Mar 16: 60%, Mar 20: 20%, Mar 28: 10%
  # Service: Mar 20: 80%, Mar 28: 50%
  if t > 10 and t <= 15:
    e.traffic_multiplier = ((0.9 - (0.06*(t-10)))**2) / 1.0
  if t > 15 and t <= 20:
    e.traffic_multiplier = ((0.6 - (0.08*(t-15)))**2) / 0.8
  if t > 20 and t <= 28:
    e.traffic_multiplier = ((0.2 - (0.0125*(t-20)))**2) / 0.5

  # Recording of existing measures
  if t > 10 and t <= 20:  # 16th of March (range 11-21)
    uk_lockdown(e, phase=1, transition_fraction=((t-10)*1.0)/100.0)
  if t > 22 and t <= 32:  # 23rd of March, t=22
    uk_lockdown(e, phase=2, transition_fraction=((t-22)*1.0)/100.0)
  if t == 52:  # 22nd of April
    uk_lockdown(e, phase=3)
  if t == 73: # 13th of May
    uk_lockdown(e, phase=4, track_trace_limit=track_trace_limit)
  if t == 92: # June 1st
    uk_lockdown(e, phase=5, track_trace_limit=track_trace_limit)
  if t == 106: # June 15th
    uk_lockdown(e, phase=6, track_trace_limit=track_trace_limit)
  if t == 125:  # July 4th
    uk_lockdown(e, phase=7, track_trace_limit=track_trace_limit)
  if t == 136:  # July 15th
    uk_lockdown(e, phase=8, track_trace_limit=track_trace_limit)
  if t == 184:  # Sept 1st
    uk_lockdown(e, phase=9, track_trace_limit=track_trace_limit)
  if t == 206:  # Sept 22nd
    uk_lockdown(e, phase=10, track_trace_limit=track_trace_limit)


def uk_lockdown_forecast(e, t, mode = 0):

  # 0 = default
  # 1 = 1 month delay
  # 2 = september 3 month delay
  # 3 = increased track and trace
  # 4 = reduced track and trace
  # 5 = 50% vaccine
  # 6 = 25% vaccine
  # 7 = no vaccine
  # 8 = temporary immunity


  delay = 0
  if mode == 1:
    delay += 30

  delay3 = 0
  if mode == 2:
    delay3 = 92

  track_trace_multiplier = 0.5
  if mode == 3:
    track_trace_multiplier = 0.25
  if mode == 4:
    track_trace_multiplier = 0.75

  vaccine = 100
  if mode == 5:
    vaccine = 50
  if mode == 6:
    vaccine = 25
  if mode == 7:
    vaccine = 0


  if t<150:
    uk_lockdown_existing(e, t)
  else:
    if t == 92+delay: # June 1st
      uk_lockdown_scenarios(e, t, 2)
    if t == 122+delay+delay3: # July 1st
      uk_lockdown_scenarios(e, t, 3)
    if t == 184+delay+delay3: # September 1st
      uk_lockdown_scenarios(e, t, 4)
    if t == 306+delay+delay3: # January 1st 2021
      uk_lockdown_scenarios(e, t, 5, track_trace_multiplier=track_trace_multiplier)
    if t == 365+delay+delay3: # March 1st 2021
      uk_lockdown_scenarios(e, t, 6, vaccine=vaccine)
    if t == 487+delay+delay3: # July 1st 2021
      uk_lockdown_scenarios(e, t, 7, vaccine=vaccine)

def work50(e):
  e.remove_all_measures()
  e.add_closure("school", 0)
  e.add_closure("leisure", 0)
  e.add_partial_closure("shopping", 0.4)
  # mimicking a 75% reduction in social contacts.
  e.add_social_distance_imp9()
  # light work from home instruction, with 50% compliance
  e.add_work_from_home(0.5)
  e.add_case_isolation()
  e.add_household_isolation()


def work75(e):
  e.remove_all_measures()
  e.add_partial_closure("leisure", 0.5)
  # mimicking a 75% reduction in social contacts.
  e.add_social_distance_imp9()
  # light work from home instruction, with 25% compliance
  e.add_work_from_home(0.25)
  e.add_case_isolation()
  e.add_household_isolation()

def work100(e):
  e.remove_all_measures()
  # mimicking a 75% reduction in social contacts.
  e.add_social_distance_imp9()
  e.add_case_isolation()
  e.add_household_isolation()

_dyn_lock_full = True # we assume this mechanism starts in lockdown mode.
def enact_dynamic_lockdown(e, light_lockdown_func, kpi_value, threshold):
  """
  Dynamic lockdown based on threshold KPI assessment.
  """
  global _dyn_lock_full
  if kpi_value > threshold:
    if not _dyn_lock_full:
      print("DYNAMIC: Full lockdown", file=sys.stderr)
      full_lockdown(e)
      _dyn_lock_full = True
  else:
    if _dyn_lock_full:
      print("DYNAMIC: Light lockdown", file=sys.stderr)
      light_lockdown_func(e)
      _dyn_lock_full = False


def enact_periodic_lockdown(e, light_lockdown_func):
  """
  Dynamic lockdown based on static time intervals.
  """
  global _dyn_lock_full
  if not _dyn_lock_full:
    print("PERIODIC: Full lockdown", file=sys.stderr)
    full_lockdown(e)
    _dyn_lock_full = True
  else:
    print("PERIODIC: Light lockdown", file=sys.stderr)
    light_lockdown_func(e)
    _dyn_lock_full = False
