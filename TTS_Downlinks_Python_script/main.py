import src.cayenneLPP as cayenneLPP
import src.postData as postData


# Downlink Settings
fPort = 1
confirmedDownlink = False       # True / False
priority = "NORMAL"             # LOWEST / LOW / BELOW_NORMAL / NORMAL / ABOVE_NORMAL / HIGH / HIGHEST
schedule = "push"               # push / replace


lpp = []

# Downlink CayenneLPP Data
# Add data in format: lpp.append([channelNumber, "sensorType", value])
# --------------------------------------------------------------------

# lpp.append([1, "addDigitalInput", 11])
# lpp.append([2, "addDigitalOutput", 255])
# lpp.append([3, "addAnalogInput", -327.67])
# lpp.append([4, "addAnalogOutput", 327.67])
# lpp.append([5, "addGenericSensor", 4294967295])
# lpp.append([6, "addLuminosity", 65535])
# lpp.append([7, "addPresence", 255])
# lpp.append([8, "addTemperature", -3276.7])
# lpp.append([9, "addRelativeHumidity", 95.7])
# lpp.append([10, "addAccelerometer", -32.767, 0, 32.767])
# lpp.append([11, "addBarometricPressure", 6553.5])
# lpp.append([12, "addVoltage", 655.34])
# lpp.append([13, "addCurrent", 65.535])
# lpp.append([14, "addFrequency", 4294967295])
# lpp.append([15, "addPercentage", 255])
# lpp.append([16, "addAltitude", -32767])
# lpp.append([17, "addConcentration", 65535])
# lpp.append([18, "addPower", 65535])
# lpp.append([19, "addDistance", 4294967.295])
# lpp.append([20, "addEnergy", 4294967.295])
# lpp.append([21, "addDirection", 65535])
# lpp.append([22, "addUnixTime", 4294967295])
# lpp.append([23, "addGyrometer", -327.67, 0, 327.67])
# lpp.append([24, "addColour", 0, 128, 255])
# lpp.append([25, "addGPS", -838.8607, 838.8607, -83886.07])
# lpp.append([26, "addSwitch", 255])



# Encode and send downlink
payload = cayenneLPP.encodeCayenneLPP(lpp)
postData.sendData(payload, fPort, confirmedDownlink, priority, schedule)