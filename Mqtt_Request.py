import paho.mqtt.client as mqtt
import json
#import datetime
import sys
#import time
from datetime import datetime
import requests
import Encryption_Data as ed
from rest_framework.response import Response
import MySQLdb


###################### register the new device ##################
def device_register(mosq,obj,msg):
     
    date1 = datetime.today()
    date = datetime.strftime(date1, '%Y-%m-%d %H:%M:%S')
    print('msg : ',msg.payload,msg.topic)
    #1234567812345678
    #jts/jpipe/v000001/data/dregister
    cipher = ed.AESCipher('1234567812345678')
    decrypted = cipher.decrypt(msg.payload)
    print ("decrypted : ",decrypted)
    try:
       data = json.loads(msg.payload)
       print('json is : ',data)
    except ValueError:
       return mqttc.publish('jts/jpipe/v000001/data/Response','{"error_code":"2","error_desc":"Response=invalid input, no proper JSON request"}' )
    except Exception as e:
       return mqttc.publish('jts/jpipe/v000001/data/Response','{"error_code":"2","error_desc":"Response=invalid input, no proper JSON request"}' )
    try:
       req2 = requests.post(url = 'http://localhost:8000/authentication/register/', data = data,verify=False)
       res = req2.text
       res = json.loads(res)
       print('res is : ',res)
       return res
       # des = cipher.encrypt(str(res)) 
       # print('enc is : ',des)

       # print(Response(r.json()))
       # return Response(r.json())
      
          
    # except MySQLdb.Error as e:
    #     try:
    #         #print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
    #         return mqttc.publish('jts/GenAc/Response',str(e.args[0])+str(e.args[1]))
    #     except IndexError:
    #         #print "MySQL Error: %s" % str(e)
    #         return mqttc.publish('jts/GenAc/Response',str(e)) 
    except Exception as e:
       
        output = '{"error_code":"3", "error_desc": "Response=Failed to add the temp"}'
        return mqttc.publish('jts/jpipe/v000001/data/Response',output)

###################### get the data from device ##################
# def device_data(mosq,obj,msg):
     
#     date1 = datetime.today()
#     date = datetime.strftime(date1, '%Y-%m-%d %H:%M:%S')
#     print('msg : ',msg.payload,msg.topic)
    
#     try:
#        data = json.loads(msg.payload)
#        # cipher = ed.AESCipher(data["uname"])
#        # decrypted = cipher.decrypt(data["data"])
#        # print ("decrypted : ",decrypted)
#        # data = json.loads(decrypted)
#        print('json is : ',data)
#     except ValueError:
#        return mqttc.publish('jts/jpipe/v000001/data/Response','{"error_code":"2","error_desc":"Response=invalid input, no proper JSON request"}' )
#     except Exception as e:
#        return mqttc.publish('jts/jpipe/v000001/data/Response','{"error_code":"2","error_desc":"Response=invalid input, no proper JSON request"}' )
#     try:
#        req2 = requests.post(url = 'http://localhost:8000/authentication/register/', data = data,verify=False)
#        res = req2.text
#        res = json.loads(res)
#        print('res is : ',res)
#        des = cipher.encrypt(str(res)) 
#        print('enc is : ',des)
       
#        # print(Response(r.json()))
#        # return Response(r.json())
      
          
#     # except MySQLdb.Error as e:
#     #     try:
#     #         #print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
#     #         return mqttc.publish('jts/GenAc/Response',str(e.args[0])+str(e.args[1]))
#     #     except IndexError:
#     #         #print "MySQL Error: %s" % str(e)
#     #         return mqttc.publish('jts/GenAc/Response',str(e)) 
#     except Exception as e:
       
#         output = '{"error_code":"3", "error_desc": "Response=Failed to add the temp"}'
#         return mqttc.publish('jts/jpipe/v000001/data/Response',output)

#############################################################################
def device_data(mosq,obj,msg):

    date1 = datetime.today()
    date = datetime.strftime(date1, '%Y-%m-%d %H:%M:%S')
    print('msg : ',msg.payload,msg.topic)
    send_data = msg.payload
    try:
        #data = json.loads(msg.payload)
        cipher = ed.AESCipher('1234567812345678')
        decrypted = cipher.decrypt(msg.payload)
        print ("decrypted : ",decrypted)
        data = json.loads(decrypted)
        print('json is : ',data)
    except ValueError:
        return mqttc.publish('jts/jpipe/v000001/data/Response','{"error_code":"2","error_desc":"Response=invalid input, no proper JSON request"}' )
    except Exception as e:
        return mqttc.publish('jts/jpipe/v000001/data/Response','{"error_code":"2","error_desc":"Response=invalid input, no proper JSON request"}' )
    try:
        req2 = requests.post(url = 'http://localhost:5901/JpipeDevice/add_data/', data = decrypted,verify=False)
        res = req2.text
        res = json.loads(res)
        print('res is : ',res)
        # if res['username'] == 'mahesh12':
        #     print
        #     mqttc.publish('jts/jpipe/v000001/Adaptor/1',send_data)
        # else:
        #     mqttc.publish('jts/jpipe/v000001/Adaptor/2',send_data)
        

          
    except MySQLdb.Error as e:
        try:
            #print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            return mqttc.publish('jts/GenAc/Response',str(e.args[0])+str(e.args[1]))
        except IndexError:
            #print "MySQL Error: %s" % str(e)
            return mqttc.publish('jts/GenAc/Response',str(e)) 
    except Exception as e:
       
        output = '{"error_code":"3", "error_desc": "Response=Failed to add the temp"}'
        return mqttc.publish('jts/jpipe/v000001/data/Response',output)
################## publish response #################################################
def on_publish(client, userdata, result):
        print ("data published \n")
        #pass
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    mqttc.subscribe("jts/jpipe/v000001/data/#")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print ("Unexpected MQTT disconnection. Will auto-reconnect")
        mqttc.subscribe("jts/jpipe/v000001/data/#")

######################### mqtt methods ####################################
mqttc = mqtt.Client()
#################### esp calls ####################################
#mqttc.message_callback_add('/test/e2s/gr1',grow_data)
mqttc.message_callback_add('jts/jpipe/v000001/data/device_register',device_register)
mqttc.message_callback_add('jts/jpipe/v000001/data/device_data',device_data)
#mqttc.message_callback_add('jts/jpipe/v000001/Adaptor/1',device_data1)
#mqttc.message_callback_add('/test/e2s/ble',ble_data)
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_publish = on_publish
mqttc.username_pw_set('esp', 'ptlesp01')
mqttc.connect("cld003.jts-prod.in", 1883, 60)
#mqttc.subscribe("jts/jpipe/v000001/#")
mqttc.loop_forever()
#mqttc.username_pw_set('esp', 'ptlesp01')
#jts/jpipe/v000001/Adaptor/1




