# %% [markdown]
# This script is modified from the example python script provided by ECMWF.
# This modified version aims to download the hindcasts for SSW events.

# %%
#!/usr/bin/env python
from ecmwfapi import ECMWFDataServer
import datetime 
from datetime import date
import calendar
import os

server = ECMWFDataServer()
origin = "ecmf"


# %%
def retrieve_ECMWF_reforecast(hindcastDate,modelVersionDate):
    """
       A function to demonstrate how to retrieve efficiently all hindcastDates
       for a particular ECMWF reforecast model version.
       Change the variables below to adapt the request to your needs
    """

    # Please note that the "sfc" and "pl" requests below could run in parallel
    # Step 1: Get pressure level data
    pfplTarget = "%s_%s_%s.nc" % (origin, "pfpl", hindcastDate)
    ECMWF_reforecast_pf_pl_request(hindcastDate, modelVersionDate, pfplTarget)

# %%
def ECMWF_reforecast_pf_pl_request(hindcastDate,modelVersionDate,target):
    """
       An ECMWF reforecast, perturbed forecast, pressure level, request.
       Change the keywords below to adapt it to your needs. (eg to add or remove some steps or parameters etc)
    """
    server.retrieve({
        "class": "s2",
        "dataset": "s2s",
        "date": modelVersionDate,
        "expver": "prod",
        "hdate": hindcastDate,
        "levtype": "pl",
        "levelist": "10",
        "origin": origin,
        "param": "131",
        "step": "0/to/1104/by/24",
        "stream": "enfh",
        "target": target,
        "time": "00",
        "number": "1/2/3/4/5/6/7/8/9/10",
        "type": "pf",
        "grid" : "0.5/0.5",
        "format": "netcdf",
    })

# %%
if __name__ == '__main__':
    pathMyDirectory = "/nfs/b0128/Users/earxzho/S2S/data/ECMWF/ssw-archive/"
    # os.chdir(pathMyDirectory)
    # Read hindcastDates from text file, which includes the hindcast Dates before a paticular SSW event
    for i in range(2,15):
        hindcastDates = []
        vfile = f"/nfs/b0128/Users/earxzho/S2S/download_dates/{i}.txt"
        for line in open(vfile):
            dd = line.strip()
            hindcastDates.append(str.strip(dd))

        modelVersionDates = []
        for hindcastDate in hindcastDates:
            dt=datetime.datetime.strptime(hindcastDate, "%Y-%m-%d")
            modelVersionYear = 2020
            modelVersionMonth = dt.month
            modelVersionDay = dt.day
            modelVersionDate = '%04d%02d%02d' % (
                modelVersionYear, modelVersionMonth, modelVersionDay)
            modelVersionDates.append(modelVersionDate)

        if os.path.exists(pathMyDirectory+f'ssw{i}'):
            os.rmdir(pathMyDirectory+f'ssw{i}')
        os.mkdir(pathMyDirectory+f'ssw{i}')
        os.chdir(pathMyDirectory+f'ssw{i}')
        for hindcastDate,modelVersionDate in zip(hindcastDates,modelVersionDates):
            print("Start downloading hindcast at " + str(hindcastDate))
            retrieve_ECMWF_reforecast(hindcastDate,modelVersionDate)





# %%
