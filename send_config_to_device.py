import paho.mqtt.client as mqtt
import Encryption_Data as ed
import base64



def config_publish(topicmac,msg):
    print('inside')
    # cipher = ed.AESCipher('1234567812345678')
    # encrypted = cipher.encrypt(msg)
    # print ("encrypted : ",encrypted)
    mqttc=mqtt.Client()
    mqttc.username_pw_set('esp','ptlesp01')
    mqttc.connect("cld003.jts-prod.in",1883,60)
    mqttc.loop_start()
    topic='jts/jpipe/v000001/Dev/%s' %(topicmac)
    print(topic)
    mqttc.publish(topic,'eyJjbGVhckFsbElDIjoiMSJ9')
    mqttc.publish(topic,base64.b64encode(msg.encode('utf-8')))
    mqttc.disconnect()
    mqttc.loop_stop()
    return 'Success'


# ##################### add user #############################
# def config_publish(topicmac,msg):
#     print('inside')
#     count=0
#     # cipher = ed.AESCipher('1234567812345678')
#     # encrypted = cipher.encrypt(msg)
#     # print ("encrypted : ",encrypted)
#     mqttc=mqtt.Client()
#     mqttc.username_pw_set('esp','ptlesp01')
#     mqttc.connect("cld003.jts-prod.in",1883,60)
#     mqttc.loop_start()
#     topic='jts/jpipe/v000001/Dev/%s' %(topicmac)
#     print(topic)
#     msg1=base64.b64encode(msg.encode('utf-8'))
#     print('msg is :',msg1)
#     mqttc.publish(topic,'eyJjbGVhckFsbElDIjoiMSJ9')
#     mqttc.publish(topic,msg1)
#     def on_publish(client,userdata,result):
#         global count
#         count = int(result)
#         print('count is : ',count)
#         print("data published \n",client,userdata,result,'count : ',count)
#         return count
#     mqttc.on_publish = on_publish
#     print('return is : ',mqttc.on_publish.result)
#     mqttc.disconnect()
#     mqttc.loop_stop()
#     return int(count)
