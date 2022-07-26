# %% [markdown]
# This script is modified from the example python script provided by ECMWF.
# This modified version aims to download the hindcasts for SSW events.

# %%
#!/usr/bin/env python
from ecmwfapi import ECMWFDataServer
import datetime 
import os
import sys

server = ECMWFDataServer()
origin = "ecmf"

sswlist = ['2000-03-30','2001-02-11','2001-12-30','2003-01-18','2004-01-05','2006-01-21',\
           '2007-02-24','2008-02-22','2009-01-24','2010-02-09','2010-03-24','2013-01-06',
           '2018-02-12','2019-01-02']

modelVersionYear = 2020
# %%
def retrieve_ECMWF_reforecast(hindcastDate,modelVersionDate):
    """
       A function to demonstrate how to retrieve efficiently all hindcastDates
       for a particular ECMWF reforecast model version.
       Change the variables below to adapt the request to your needs
    """
    # Please note that the "sfc" and "pl" requests below could run in parallel
    # Step 1: Get pressure level data
    pfplTarget = "%s_%s_%s.grb" % (origin, "pfpl", hindcastDate)
    cfplTarget = "%s_%s_%s.grb" % (origin, "cfpl", hindcastDate) 
    ECMWF_reforecast_pf_pl_request(hindcastDate, modelVersionDate, pfplTarget)
    ECMWF_reforecast_cf_pl_request(hindcastDate, modelVersionDate, cfplTarget)

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
    })


def ECMWF_reforecast_cf_pl_request(hindcastDate,modelVersionDate,target):
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
        "model": "glob",
        "type": "cf",
        "grid" : "0.5/0.5",
    })
# %%
if __name__ == '__main__':
    pathMyDirectory = "/nfs/b0128/Users/earxzho/S2S/data/ECMWF/ssw-archive/"
    # find hindcastDates 31days before a paticular SSW event
    for sswDate in sswlist[3:]:
        # Preserve data in the ssw-date file
        if os.path.exists(pathMyDirectory+f'ssw-{sswDate}'):
            os.rmdir(pathMyDirectory+f'ssw-{sswDate}')
        os.mkdir(pathMyDirectory+f'ssw-{sswDate}')
        os.chdir(pathMyDirectory+f'ssw-{sswDate}')
        print('Downloading files to '+pathMyDirectory+ f'ssw-{sswDate}')

        d=datetime.datetime.strptime(sswDate, "%Y-%m-%d")
        # decide the modelVersionDate: search from d_start to d_end;
        # if it is Tuesday or Tursday, then it is.

        if d.year >= modelVersionYear:
            sys.exit("SSW year exceeds 2020. \
                Please either change the SSW event or change the model Version Year!")
            
        d_end = d.date() 
        d_start = d_end - datetime.timedelta(days=31)

        while d_start<=d_end:
            d_start_modelVersion = datetime.date(modelVersionYear,d_start.month,d_start.day)
            if d_start_modelVersion.weekday()==0 or d_start_modelVersion.weekday() ==3: #if its Tuesday or Thursday
                modelVersionDate = '%04d-%02d-%02d' % (
                    modelVersionYear, d_start.month, d_start.day)
                hindcastDate = '%04d-%02d-%02d' % (
                    d_start.year, d_start.month, d_start.day) 
                # print(modelVersionDate,hindcastDate) #check the date list
                retrieve_ECMWF_reforecast(hindcastDate,modelVersionDate) 
            d_start+=datetime.timedelta(days=1)
