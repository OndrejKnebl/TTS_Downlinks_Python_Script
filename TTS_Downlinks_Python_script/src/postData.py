import requests
from base64 import b64encode
import config


def sendData(payload, fPort, confirmedDownlink, priority, schedule):

    if payload == "":
        print("Nothing to send!")
        exit(0)
    else:
        print("Sending payload:", payload)


    # CayenneLPP hex -> base64
    payloadBase64 = b64encode(bytes.fromhex(payload)).decode()


    # POST
    url = 'https://eu1.cloud.thethings.network/api/v3/as/applications/' + config.applicationName + '/devices/' + config.endDeviceName + '/down/'+ schedule
    header = {'Authorization': 'Bearer ' + config.APIKey, 
            'Content-Type': 'application/json',
            'User-Agent': 'my-integration/my-integration-version'
            }

    data = {"downlinks":[{
        "frm_payload": payloadBase64,
        "f_port": fPort,
        "confirmed": confirmedDownlink,
        "priority": priority
        }]}

    response = requests.post(url, headers=header, json=data)

    print("Status code", response.status_code)
