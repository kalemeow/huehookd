from flask import Flask, request
import requests

''' 
    huehookd.py: Webhook proxy for hue lights.

    This script sets up a simple flask server that proxies
    specific requests to a local hue bridge, to allow for
    external control of the hue light API.  For security
    reasons, only specific endpoints are implemented, 
    specifically the get and set lights and groups states.
    Ideally, this script is run on a raspberry pi or the 
    like and you set up port forwarding from your router
    to this script, which will listen on port 5000.

    In order to get this to work, you have to create a 
    hue user on your bridge and fill in the HUE_USER variable.
    To do so, go to your bridge's debug API interface, found
    at http://192.168.86.165/debug/clip.html, and set the URL
    as '/api' and the message body as 
    '{"devicetype": "huehookd#raspi"}'
    Go press the button on your hue bridge, then press POST
    on the API debugger page; it should respond with 'success'
    and a username that you should paste here.
'''

HUE_IP = '192.168.1.2'
HUE_USER = 'username'
BASE_URL = 'http://%s/api/%s' % (HUE_IP, HUE_USER)

app = Flask(__name__)

@app.route('/hooks/lights/<lightId>', methods=['GET', 'PUT'])
def lightsApi(lightId):
    ''' Get or set the state of the given lightId. 
        If the method is GET, offer the state as a json blob.
        If the method is PUT, expect an appropriate JSON payload
        as defined in the hue API for set light state.
    '''

    if request.method == 'PUT':
        r = requests.put('%s/lights/%s/state' % (BASE_URL, lightId), data = request.data)
        output = str(r.json())
        return output

    else:
        r = requests.get('%s/lights/%s' % (BASE_URL, lightId))
        output = str(r.json())
        return output


@app.route('/hooks/groups/<groupId>', methods=['GET', 'PUT'])
def groupsApi(groupId):
    ''' Get or set the state of the given groupId.
        If the method is GET, offer the state as a json blob.
        If the method is PUT, expect an approrpriate JSON payload
        as defined in the hue API for set group state.
    '''

    if request.method == 'PUT':
        r = requests.put('%s/groups/%s/action' % (BASE_URL, groupId), data = request.data)
        output = str(r.json())
        return output

    else:
        r = requests.get('%s/groups/%s' % (BASE_URL, groupId))
        output = str(r.json())
        return output



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
