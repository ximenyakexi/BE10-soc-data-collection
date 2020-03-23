from opcua import Client
import flask
import time
import flask

url = "opc.tcp://192.168.1.33:48010" #server url

client = Client(url)

#set security mode and certificate. Use server's certificate instead. Certificate path need to be modified
client.set_security_string("Basic256,SignAndEncrypt,C:/Users/RSONG/Documents/InduSoft Web Studio v8.1 Projects/Project/Config/uaserver/own/studio.der,C:/Users/RSONG/Documents/InduSoft Web Studio v8.1 Projects/Project/Config/uaserver/own/studio.pem")

#Set client uri to match server's certificate
client.application_uri = "urn:DESKTOP-U34UL7P:Studio:OpcUaServer"

def connect_to_server(client):
    connection_times = 0
    while True:
        connection_times += 1
        try:
            if connection_times > 100:
                raise ValueError('Failed to connect to opcua server')
            client.connect()
            break
        except:
            time.sleep(1)
            print(f"reconnecting to server, {connection_times} times")
            continue

request = True

while request:
    try:
        number_node = client.get_node('ns=2;s=Studio.Tags.Application.Number')
        number = number_node.get_value()

        timer_acc_node = client.get_node('ns=2;s=Studio.Tags.Application.TIMER_ACC')
        timer_acc = timer_acc_node.get_value()

        print(number)
        print(timer_acc)

        time.sleep(5)
    except:
        print("reconnect to server")
        connect_to_server(client)
