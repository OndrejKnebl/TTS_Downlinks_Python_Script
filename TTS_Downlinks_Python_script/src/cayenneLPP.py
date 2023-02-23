import ctypes

sensor_types = {
    'addDigitalInput' : {'type':"00", 'size':1, 'multipl':1, 'signed':False, 'min':0, 'max':255, 'arrLen':3},
    'addDigitalOutput' : {'type':"01", 'size':1, 'multipl':1, 'signed':False, 'min':0, 'max':255, 'arrLen':3},
    'addAnalogInput' : {'type':"02", 'size':2, 'multipl':100, 'signed':True, 'min':-327.67, 'max':327.67, 'arrLen':3},
    'addAnalogOutput' : {'type':"03", 'size':2, 'multipl':100, 'signed':True, 'min':-327.67, 'max':327.67, 'arrLen':3},
    'addGenericSensor' : {'type':"64", 'size':4, 'multipl':1, 'signed':False, 'min':0, 'max':4294967295, 'arrLen':3},
    'addLuminosity' : {'type':"65", 'size':2, 'multipl':1, 'signed':False, 'min':0, 'max':65535, 'arrLen':3},
    'addPresence' : {'type':"66", 'size':1, 'multipl':1, 'signed':False, 'min':0, 'max':255, 'arrLen':3},    
    'addTemperature' : {'type':"67", 'size':2, 'multipl':10, 'signed':True, 'min':-3276.7, 'max':3276.7, 'arrLen':3},
    'addRelativeHumidity' : {'type':"68", 'size':1, 'multipl':2, 'signed':False, 'min':0, 'max':100, 'arrLen':3}, #'max':127.5
    'addAccelerometer' : {'type':"71", 'size':6, 'multipl':1000, 'signed':True, 'min':-32.767, 'max':32.767, 'arrLen':5},
    'addBarometricPressure' : {'type':"73", 'size':2, 'multipl':10, 'signed':False, 'min':0, 'max':6553.5, 'arrLen':3},
    'addVoltage' : {'type':"74", 'size':2, 'multipl':100, 'signed':False, 'min':0, 'max':655.34, 'arrLen':3},
    'addCurrent' : {'type':"75", 'size':2, 'multipl':1000, 'signed':False, 'min':0, 'max':65.535, 'arrLen':3},
    'addFrequency' : {'type':"76", 'size':4, 'multipl':1, 'signed':False, 'min':0, 'max':4294967295, 'arrLen':3},
    'addPercentage' : {'type':"78", 'size':1, 'multipl':1, 'signed':False, 'min':0, 'max':255, 'arrLen':3},
    'addAltitude' : {'type':"79", 'size':2, 'multipl':1, 'signed':True, 'min':-32767, 'max':32767, 'arrLen':3},
    'addConcentration' : {'type':"7D", 'size':2, 'multipl':1, 'signed':False, 'min':0, 'max':65535, 'arrLen':3},
    'addPower' : {'type':"80", 'size':2, 'multipl':1, 'signed':False, 'min':0, 'max':65535, 'arrLen':3},
    'addDistance' : {'type':"82", 'size':4, 'multipl':1000, 'signed':False, 'min':0, 'max':4294967.295, 'arrLen':3},
    'addEnergy' : {'type': "83", 'size':4, 'multipl':1000, 'signed':False, 'min':0, 'max':4294967.295, 'arrLen':3},
    'addDirection' : {'type':"84", 'size':2, 'multipl':1, 'signed':False, 'min':0, 'max':65535, 'arrLen':3},
    'addUnixTime' : {'type':"85", 'size':4, 'multipl':1, 'signed':False, 'min':0, 'max':4294967295, 'arrLen':3},
    'addGyrometer' : {'type':"86", 'size':6, 'multipl':100, 'signed':True, 'min':-327.67, 'max':327.67, 'arrLen':5},
    'addColour' : {'type':"87", 'size':1, 'multipl':1, 'signed':False, 'min':0, 'max':255, 'arrLen':5}, # size changed
    'addGPS' : {'type':"88", 'size':9, 'multipl_l_l' : 10000, 'multipl_alt' : 100, 'signed': True, 'min_l_l':-838.8607, 'max_l_l':838.8607, 'min_alt':-83886.07, 'max_alt':83886.07, 'arrLen':5},
    'addSwitch' : {'type':"8E", 'size':1, 'multipl':1, 'signed':False, 'min':0, 'max':255, 'arrLen':3}
}


def encodeCayenneLPP(lpp):

    payload = ""
    onePayload = ""
    duplicityDict = {}


    for i in range(0,len(lpp)):
            
        sensorInfo = sensor_types.get(lpp[i][1])

        if sensorInfo == None:
            print("Unknown type " + str(lpp[i][1]) + " in channel " + str(lpp[i][0]) + ".")
            continue

        if len(lpp[i]) != sensorInfo.get("arrLen"):
            print("Too few/many values in channel " + str(lpp[i][0]) + " of the type " + str(lpp[i][1]))

        else:

            try:
                onePayload += str(f'{lpp[i][0]:02x}')    # channel
            except:
                print("The channel number is in the wrong format!")
                continue
            
            
            # check for same channel and type
            if lpp[i][1] in duplicityDict:
                if duplicityDict[lpp[i][1]] == lpp[i][0]:
                    print("Duplicity! Channel number " + str(lpp[i][0]) + " and type " + str(lpp[i][1]) + " have already been added!")
                    continue

            duplicityDict[lpp[i][1]] = lpp[i][0]


            onePayload += sensorInfo.get("type")        # sensor type


            for j in range(2,len(lpp[i])):

                error = False
                value = lpp[i][j] 


                if type(value) != int and type(value) != float:
                    print("The value in channel " + str(lpp[i][0]) + " of the type " + lpp[i][1] + " is not a number.")
                    error = True
                    break


                # range and *
                if lpp[i][1] == "addGPS":
                    if j < 4:
                        if not (value >= sensorInfo.get("min_l_l") and value <= sensorInfo.get("max_l_l")):
                            print("Value " + str(value) + " in channel " + str(lpp[i][0]) + " of the type " + lpp[i][1] + " is outside the " + str(sensorInfo.get("min_l_l")) + " - " + str(sensorInfo.get("max_l_l")) + " range!")
                            error = True
                            break
                        valueConversion = int(value * sensorInfo.get("multipl_l_l"))

                    else:
                        if not (value >= sensorInfo.get("min_alt") and value <= sensorInfo.get("max_alt")):
                            print("Value " + str(value) + " in channel " + str(lpp[i][0]) + " of the type " + lpp[i][1] + " is outside the " + str(sensorInfo.get("min_alt")) + " - " + str(sensorInfo.get("max_alt")) + " range!")
                            error = True
                            break
                        valueConversion = int(value * sensorInfo.get("multipl_alt"))
                        
                else:
                    if not (value >= sensorInfo.get("min") and value <= sensorInfo.get("max")):
                        print("Value " + str(value) + " in channel " + str(lpp[i][0]) + " of the type " + lpp[i][1] + " is outside the " + str(sensorInfo.get("min")) + " - " + str(sensorInfo.get("max")) + " range!")
                        error = True
                        break
                    valueConversion = int(value * sensorInfo.get("multipl"))


                # Signed conversion
                sign = False
            
                if value < 0:
                    sign = True

                if sensorInfo.get("signed") & sign:
                    if lpp[i][1] == "addGPS":
                        valueConversion = ctypes.c_uint32(valueConversion).value
                    else:
                        valueConversion = ctypes.c_uint16(valueConversion).value

                # Size
                if sensorInfo.get("size") == 1:
                    onePayload += str(f'{valueConversion:02x}')[-2:]
                elif sensorInfo.get("size") == 2:
                    onePayload += str(f'{valueConversion:04x}')[-4:]
                elif sensorInfo.get("size") == 4:
                    onePayload += str(f'{valueConversion:08x}')[-8:]
                elif sensorInfo.get("size") == 6:
                    onePayload += str(f'{valueConversion:04x}')[-4:]
                elif sensorInfo.get("size") == 9:
                    onePayload += str(f'{valueConversion:06x}')[-6:]
            
            if error == False:
                payload += onePayload
            else:
                onePayload = ""

    return payload
