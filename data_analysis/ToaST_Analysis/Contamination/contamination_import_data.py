import csv
from Contamination.ContaminationMeasurementMultiTrapComparison import ContaminationMeasurementMultiTrapComparison
from uncertainties import ufloat

def format_multi_trap_comparison(line):
    ## Measurement_Multi_Trap_Comparison object takes "raw_data" is a list of the form:
    ##      ['trap name',
    ##       trapping_height_um,
    ##       trap_frequency_MHz,
    ##       days_in_atmosphere,
    ##       weeks_baked
    ##       ufloat(heatingrate,error),
    ##       times_broke_vacuum,
    ##       'evaporation_date']

    trap_name = line[0]
    trapping_height_um = float(line[1])
    trap_frequency_MHz = float(line[2])
    days_in_atmosphere = float(line[3])
    weeks_baked = float(line[4])
    heatingrate = ufloat(line[5].split('+')[0], line[5].split('-')[1])
    times_broke_vacuum = float(line[6])
    evaporation_date = line[7]

    return trap_name, trapping_height_um, trap_frequency_MHz, days_in_atmosphere, weeks_baked, heatingrate, times_broke_vacuum, evaporation_date

def import_multi_trap_comparison_data(filename):
    reader = csv.reader(open(filename))
    # skip header line
    next(reader)

    heatingrate_list = []
    for line in reader:
        trap_name, trapping_height_um, trap_frequency_MHz, days_in_atmosphere, weeks_baked, heatingrate, times_broke_vacuum, evaporation_date = format_multi_trap_comparison(line)
        heatingrate_list.append(ContaminationMeasurementMultiTrapComparison(trap_name, trapping_height_um, trap_frequency_MHz, days_in_atmosphere, weeks_baked, heatingrate, times_broke_vacuum, evaporation_date))

    return heatingrate_list


