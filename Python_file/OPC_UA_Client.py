from opcua import Client
import time, logging, datetime, json
from Python_file import app
from flask import jsonify, request, render_template


logging.basicConfig(filename="python_log.log", level=logging.ERROR)

url = "opc.tcp://192.168.1.33:48010" #server url

client = Client(url)

def connect_to_server(client):
    connection_times = 0
    while True:
        connection_times += 1
        try:
            #set security mode and certificate. Use server's certificate instead. Certificate path need to be modified
            client.set_security_string("Basic256,SignAndEncrypt,C:/Users/RSONG/Documents/InduSoft Web Studio v8.1 Projects/Project/Config/uaserver/own/studio.der,C:/Users/RSONG/Documents/InduSoft Web Studio v8.1 Projects/Project/Config/uaserver/own/studio.pem")

            #Set client uri to match server's certificate
            client.application_uri = "urn:DESKTOP-U34UL7P:Studio:OpcUaServer"

            if connection_times > 50:
                logging.error("Failed to connect to opcua server at " + datetime.datetime.utcnow().strftime('%B %d %Y - %H:%M:%S'))
                return "Failed"
            client.connect()
            logging.info("successfully connected to opcua server at " + datetime.datetime.utcnow().strftime('%B %d %Y - %H:%M:%S'))
            return "Success"
            break
        except:
            time.sleep(1)
            logging.error(f"Connection failed, reconnecting to server, {connection_times} times at " + datetime.datetime.utcnow().strftime('%B %d %Y - %H:%M:%S'))
            continue

@app.route('/', methods=['GET', 'POST'])
def pull_soc():
    logging.error("Get a request from javascript")
#    data = None
#    if request.method == 'GET':

#        data = request.get_json()

#    if data and "requested" in data:
#        requested = data["requested"]
#    else:
#        requested = None

    while True:

        status = connect_to_server(client)
        message = ""

        if status == "Failed":
            message = {'message':'failed to pull data from opcua server'}
            #logging.error("test position 111111111")
            return jsonify(message)

        try:
            number_node = client.get_node('ns=2;s=Studio.Tags.Application.Number')
            number = number_node.get_value()

            timer_acc_node = client.get_node('ns=2;s=Studio.Tags.Application.TIMER_ACC')
            timer_acc = timer_acc_node.get_value()

            message = {'number':number, 'timer_acc':timer_acc}
            #logging.error("test position 2222222222")

        except:
            logging.error("Cannot get data from server at " + datetime.datetime.utcnow().strftime('%B %d %Y - %H:%M:%S'))
            message = {'message':'failed to pull data from opcua server'}
            #logging.error("test position 333333333")

        finally:
            client.disconnect()
            return jsonify(message)
