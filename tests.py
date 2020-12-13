from readers import read_poly


log_prefix = "output"
cases_in_regions_today = {}
def log_region_status(t):
  global cases_in_regions_today
  out_inf = open("{}/cases_in_regions2.csv".format(log_prefix),'a+')
  out_inf.seek(0,0) #go to start of file
  if out_inf.readline().split(",")[0] != "day": #check if header exists or not
    header = "day,"
    for name in cases_in_regions_today.keys():
      header += str(name) + ","
    header = header[:-1]
    print(header,file=out_inf)
  out_inf.seek(0, 2) #go to start of file
  output = str(t)+","
  for case_count in cases_in_regions_today.values():
    output += str(case_count)+","
  output = output[:-1]
  print(output, file=out_inf)


def set_regions(regions):
    temp = {}
    for x in regions.keys():
      temp[x] = 1
    temp["unknown"] = 0
    return temp

regions = read_poly.readPolyFiles("poly_files")
for i in range(5):
  regions = set_regions(regions)
  print(regions)

# print(cases_in_regions_today.keys())
# log_region_status(1)


