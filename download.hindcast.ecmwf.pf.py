#!/usr/bin/env python
# This is adapted from the example provided by ecmwf:
# https://confluence.ecmwf.int/display/WEBAPI/S2S+ECMWF+reforecasts+retrieval+efficiency
# How to use this script:
# Specify the year of the model version. Modify the parameter year.
# Note that all the versions during the specified year will be retrieved.
# This is used to retrieve data from ecmwf, but can be adapted for other on the fly models.

from ecmwfapi import ECMWFDataServer
import datetime 
from datetime import date
import calendar

server = ECMWFDataServer()
origin = "ecmf"
year = 2020     # Select the Year of Model Version (can be any year from 2015 to 2021).
 
def retrieve_ECMWF_reforecast(modelVersionDate):
    """
       A function to demonstrate how to retrieve efficiently all hindcastDates
       for a particular ECMWF reforecast model version.
       Change the variables below to adapt the request to your needs
    """
    dt=datetime.datetime.strptime(modelVersionDate, "%Y-%m-%d")
    modelVersionYear = dt.year
    modelVersionMonth = dt.month
    modelVersionDay = dt.day
    hindcastYears = range(modelVersionYear-20,modelVersionYear)

    hindcastDates = []
    for hindcastYear in hindcastYears:
        hindcastDate = '%04d%02d%02d' % (
            hindcastYear, modelVersionMonth, modelVersionDay)
        hindcastDates.append(hindcastDate)

    # Please note that the "sfc" and "pl" requests below could run in parallel
    # Step 1: Get pressure level data
    pfplTarget = "%s_%s_%s.grb" % (origin, "pfpl", modelVersionDate)
    print(pfplTarget)
    ECMWF_reforecast_pf_pl_request(modelVersionDate,"/".join(hindcastDates), pfplTarget)

 
def ECMWF_reforecast_pf_pl_request(modelVersionDate,hindcastDate, target):
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
    })

if __name__ == '__main__':

    c = calendar.TextCalendar(calendar.SUNDAY)
    for m in range(1,13):
        for i in c.itermonthdays(year,m):
            if i != 0:                                      #calendar constructs months with leading zeros (days belongng to the previous month)
                day = date(year,m,i)
                if day.weekday() == 0 or day.weekday() == 3: #if its Tuesday or Thursday
                    modelVersionDate = '%04d-%02d-%02d' % (
                            year, m, i)
                    retrieve_ECMWF_reforecast(modelVersionDate)
