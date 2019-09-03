#!/usr/bin/env python3

import subprocess
import json
import requests
import time
import datetime
from statistics import mean

# Open C File
proc = subprocess.Popen(['./bsec_bme680'], stdout=subprocess.PIPE)

listIAQ = []
listStaticIAQ = []
listIAQ_Accuracy = []
listTemperature = []
listHumidity = []
listPressure = []
listGas = []
listCO2eq = []
listBreathVOCeq = []
listStatus = []

for line in iter(proc.stdout.readline, ''):
    lineJSON = json.loads(line.decode("utf-8"))  # process line-by-line
    lineDict = dict(lineJSON)

    listIAQ_Accuracy.append(int(lineDict['iaq_accuracy']))
    listIAQ.append(float(lineDict['iaq']))
    listStaticIAQ.append(float(lineDict['static_iaq']))
    listPressure.append(float(lineDict['pressure']))
    listGas.append(int(lineDict['gas']))
    listTemperature.append(float(lineDict['temperature']))
    listHumidity.append(float(lineDict['humidity']))
    listCO2eq.append(float(lineDict['co2_equivalent']))
    listBreathVOCeq.append(float(lineDict['breath_voc_equivalent']))
    listStatus.append(int(lineDict['status']))

    if len(listIAQ_Accuracy) == 5:
        # generate the mean for each value
        IAQ = mean(listIAQ)
        StaticIAQ = mean(listStaticIAQ)
        IAQ_Accuracy = listIAQ_Accuracy[-1]
        Temperature = mean(listTemperature)
        Humidity = mean(listHumidity)
        Pressure = mean(listPressure)
        Gas = mean(listGas)
        CO2eq = mean(listCO2eq)
        BreathVOCeq = mean(listBreathVOCeq)
        Status = listStatus[-1]

        # clear lists
        listIAQ_Accuracy.clear()
        listPressure.clear()
        listGas.clear()
        listTemperature.clear()
        listIAQ.clear()
        listHumidity.clear()
        listStatus.clear()
        listStaticIAQ.clear()
        listCO2eq.clear()
        listBreathVOCeq.clear()

        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(
            ts).strftime('%Y-%m-%d %H:%M:%S')

        payload = {
            "timestamp": timestamp,
            "iaq": IAQ,
            "static_iaq": StaticIAQ,
            "iaq_accuracy": IAQ_Accuracy,
            "temperature": Temperature,
            "humidity": Humidity,
            "pressure": Pressure,
            "gas": Gas,
            "co2_equivalent": CO2eq,
            "breath_voc_equivalent": BreathVOCeq,
            "status": Status
        }

        r = requests.post("https://abhijitvalluri.com/testDash/ingest.php", data=payload)