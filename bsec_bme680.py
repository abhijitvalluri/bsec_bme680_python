#!/usr/bin/env python3

import subprocess
import json
import requests
import time
import datetime
from statistics import median

# Open C File
proc = subprocess.Popen(['./bsec_bme680'], stdout=subprocess.PIPE)

listIAQ_Accuracy = []
listPressure = []
listGas = []
listTemperature = []
listIAQ = []
listHumidity = []
listStatus = []

for line in iter(proc.stdout.readline, ''):
    lineJSON = json.loads(line.decode("utf-8"))  # process line-by-line
    lineDict = dict(lineJSON)

    listIAQ_Accuracy.append(int(lineDict['iaq_accuracy']))
    listIAQ.append(float(lineDict['iaq']))
    listPressure.append(float(lineDict['pressure']))
    listGas.append(int(lineDict['gas']))
    listTemperature.append(float(lineDict['temperature']))
    listHumidity.append(float(lineDict['humidity']))
    listStatus.append(int(lineDict['status']))

    if len(listIAQ_Accuracy) == 5:
        # generate the median for each value
        IAQ_Accuracy = listIAQ_Accuracy[-1]
        Pressure = median(listPressure)
        Gas = median(listGas)
        Temperature = median(listTemperature)
        IAQ = median(listIAQ)
        Humidity = median(listHumidity)
        Status = listStatus[-1]

        # clear lists
        listIAQ_Accuracy.clear()
        listPressure.clear()
        listGas.clear()
        listTemperature.clear()
        listIAQ.clear()
        listHumidity.clear()
        listStatus.clear()

        # Temperature Offset
        Temperature = Temperature + 2

        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(
            ts).strftime('%Y-%m-%d %H:%M:%S')

        payload = {
            "timestamp": timestamp,
            "iaq": IAQ,
            "iaq_accuracy": IAQ_Accuracy,
            "temperature": Temperature,
            "humidity": Humidity,
            "pressure": Pressure,
            "gas": Gas,
            "status": Status
        }

        r = requests.post("https://abhijitvalluri.com/testDash/ingest.php", data=payload)