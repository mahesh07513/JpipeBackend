from __future__ import unicode_literals
from django.shortcuts import render
import requests
from .models import *
from django.http import HttpResponse
from django.http import JsonResponse
import json
import logging
from django.db.models import *
from datetime import datetime
import sys
import random
sys.path.append('..')
#import send_config_to_device as sendConfig
import base64
import paho.mqtt.publish as publish



##################### add user #############################
def add_user(request): 
    if(request.method == "POST"):
        logging.debug("add_user: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output_str = "add_user- Unable to Authenticate/add_user... "
        logging.debug("add_user:input- "+str(request.body))
        try:
            data = json.loads(request.body)
            print (request.body)
        except ValueError as e:
            output_str += ",invalid input, no proper JSON request "
            output = '{"error_code":"400","error_desc":"Response=%s"}' %(output_str)
            logging.debug("add_user:"+ output)
            HttpResponse(output)
        try:
            kwargs = {}
            if((data.get('Username') is None) or ((data.get('Username') is not  None) and (len(data['Username']) <= 0))):
                output_str += ",Username is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("add_user:"+ output)
                return HttpResponse(output)
            else:
                username    = data['Username']
                kwargs['Username'] = username
            if((data.get('Password') is None) or ((data.get('Password') is not  None) and (len(data['Password']) <= 0))):
                output_str += ",Password is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("add_user:"+ output)
                return HttpResponse(output)
            else:
                password    = data['Password']
                kwargs['Password'] = password
            if((data.get('Fname') is not  None) and (len(data['Fname']) > 0)):
                fname = data['Fname']     
                kwargs['Fname'] = fname
            if((data.get('Lname') is not  None) and (len(data['Lname']) > 0)):
                lname = data['Lname']     
                kwargs['Lname'] = lname
            if((data.get('TransPass') is not  None) and (len(data['TransPass']) > 0)):
                transpass = data['TransPass']     
                kwargs['TransPass'] = transpass
            if((data.get('Email') is not  None) and (len(data['Email']) > 0)):
                email = data['Email']     
                kwargs['Email'] = email
            if((data.get('MobileNo') is not  None) and (len(data['MobileNo']) > 0)):
                mobileno = data['MobileNo']     
                kwargs['MobileNo'] = mobileno
            if((data.get('Address') is not  None) and (len(data['Address']) > 0)):
                address = data['Address']     
                kwargs['Address'] = address
            logging.debug("add_user:input: user="+username)
            check_user = JP_Users.objects.filter(Username=username)
            print(check_user)
            if len(check_user) > 0:
                output = '{"error_code":"429","error_desc":"Response=Username already exists"}' 
                logging.debug("add_user:"+ output)
                return HttpResponse(output)
            else:
                add_usr_rec=JP_Users(**kwargs);
                add_usr_rec.save()
                #add_usr_rec.save()
                print(add_usr_rec.Username)
                if(len(str(add_usr_rec)) > 0):
                    output = '{"error_code":"200","Response":"Successfully added the User, %s","UserId":"%s"}' %(username,add_usr_rec.UserId)
                    logging.debug("add_user:"+ output)
                    return HttpResponse(output)
                else:
                    output = '{"error_code":"409","error_desc":"Response=Failed to add the user"}' 
                    logging.debug("add_user:"+ output)
                    return HttpResponse(output)
        except Exception as e:
            err_desc = 'add_user:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
            logging.debug("add_user:"+ err_desc)
            output = '{"error_code":"500","error_desc":"Response=Failed to add the user"}'
            logging.debug("add_user:"+ output)
            return HttpResponse(output)
    
    else:
        logging.debug("add_user: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output = '{"error_code":"405","error_desc":"Response=GET is not supported"}'
        logging.debug("add_user:"+ output)
        return HttpResponse(output)

#############################Login###############################
def login(request):
    if(request.method == "POST"):
        logging.debug("login: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output_str = "login- Unable to Authenticate/login... " 
        logging.debug("login:input- "+str(request.body))
        try:
            data = json.loads(request.body)
            print (request.body)
        except ValueError as e:
            output_str += ",invalid input, no proper JSON request "
            output = '{"error_code":"400","error_desc":"Response=%s"}' %(output_str )
            logging.debug("login:"+ output)
            return HttpResponse(output)
     
        try:
            kwargs = {}
            if((data.get('Username') is None) or ((data.get('Username') is not  None) and (len(data['Username']) <= 0))):
                output_str += ",Username is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("login:"+ output)
                return HttpResponse(output)
            else:
                username    = data['Username']
                kwargs['Username'] = username
            if((data.get('Password') is None) or ((data.get('Password') is not  None) and (len(data['Password']) <= 0))):
                output_str += ",Password is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("login:"+ output)
                return HttpResponse(output)
            else:
                password    = data['Password']
                kwargs['Password'] = password

            if JP_Users.objects.filter(Username=username,Password=password,StatusActive=True).exists():
                get_user=JP_Users.objects.filter(Username=username,Password=password)
                #print(get_user[0].UserId)
                output = '{"error_code":"200","Response":"Successfully Authenticated the User","UserId":"%s" }' %(get_user[0].UserId) 
                logging.debug("login:"+ output)
                return HttpResponse(output)
            else:
                output = '{"error_code":"401","error_desc":"Response=Failed to Authenticate the user"}'
                logging.debug("login:"+ output)
                return HttpResponse(output)
        except Exception as e:
            err_desc = 'login:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
            logging.debug("login:"+ err_desc)
            output = '{"error_code":"500","error_desc":"Response=Failed to add the user"}'
            logging.debug("login:"+ output)
            return HttpResponse(output)
    else:
        logging.debug("login: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output = '{"error_code":"405","error_desc":"Response=GET is not supported"}'
        logging.debug("login:"+ output)
        return HttpResponse(output)


##################### add device #############################
def add_device(request): 
    if(request.method == "POST"):
        logging.debug("add_device: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output_str = "add_device- Unable to Authenticate/add_device... "
        logging.debug("add_device:input- "+str(request.body))
        try:
            data = json.loads(request.body)
            print (request.body)
        except ValueError as e:
            output_str += ",invalid input, no proper JSON request "
            output = '{"error_code":"400","error_desc":"Response=%s"}' %(output_str)
            logging.debug("add_device:"+ output)
            HttpResponse(output)
        try:
            kwargs = {}
            if((data.get('UserId') is None) or ((data.get('UserId') is not  None) and (len(data['UserId']) <= 0))):
                output_str += ",UserId is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("add_device:"+ output)
                return HttpResponse(output)
            else:
                userid    = data['UserId']
                get_user = JP_Company_Users.objects.get(CUId=userid,StatusActive=True)
                print(get_user)
                if len(str(get_user)) > 0:
                    print('inside if')
                    kwargs['CUId'] = get_user


            if((data.get('DeviceMac') is None) or ((data.get('DeviceMac') is not  None) and (len(data['DeviceMac']) <= 0))):
                output_str += ",DeviceMac is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("add_device:"+ output)
                return HttpResponse(output)
            else:
                dmac    = data['DeviceMac']
                kwargs['DeviceMac'] = dmac
            if((data.get('DeviceName') is not  None) and (len(data['DeviceName']) > 0)):
                cdesc = data['DeviceName']     
                kwargs['DeviceName'] = cdesc
            
            logging.debug("add_device:input: company="+dmac)
            
            check_device = JP_Devices.objects.filter(DeviceMac=dmac)
            print(check_device)
            if len(check_device) > 0:
                output = '{"error_code":"429","error_desc":"Response=device already associated"}' 
                logging.debug("add_device:"+ output)
                return HttpResponse(output)
            else:
                add_comp_rec=JP_Devices(**kwargs);
                add_comp_rec.save()
                print(add_comp_rec.DeviceMac)
                if(len(str(add_comp_rec.DeviceMac)) > 0):
                    output = '{"error_code":"200","Response":"Successfully added the device, %s"}' %(dmac)
                    logging.debug("add_device:"+ output)
                    return HttpResponse(output)
                else:
                    output = '{"error_code":"409","error_desc":"Response=Failed to add the dev"}'
                    logging.debug("add_device:"+ output)
                    return HttpResponse(output)
        except Exception as e:
            err_desc = 'add_device:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
            logging.debug("add_device:"+ err_desc)
            output = '{"error_code":"500","error_desc":"Response=Failed to add the device"}'
            logging.debug("add_device:"+ output)
            return HttpResponse(output)
    
    else:
        logging.debug("add_device: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output = '{"error_code":"405","error_desc":"Response=GET is not supported"}'
        logging.debug("add_device:"+ output)
        return HttpResponse(output)


##################### get devices #############################
def get_devices(request):
    if(request.method == "POST"):
        logging.debug("get_devices: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output_str = "get_devices - Unable to Authenticate/get_devices... " 
        logging.debug("get_devices:input- "+str(request.body))
        try:
            data = json.loads(request.body)
            print (request.body)
        except ValueError:
            output_str += ",invalid input, no proper JSON request "
            output = '{"error_code":"400","error_desc":"Response=%s"}' %(output_str )
            logging.debug("get_devices:"+ output)
            return HttpResponse(output)
        try:
            kwargs = {}
            if((data.get('Username') is None) or ((data.get('Username') is not  None) and (len(data['Username']) <= 0))):
                output_str += ",Username is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("get_devices:"+ output)
                return HttpResponse(output)
            else:
                username    = data['Username']
                kwargs['Username'] = username
            if((data.get('Password') is None) or ((data.get('Password') is not  None) and (len(data['Password']) <= 0))):
                output_str += ",Password is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("get_devices:"+ output)
                return HttpResponse(output)
            else:
                password    = data['Password']
                kwargs['Password'] = password

            if JP_Users.objects.filter(Username=username,Password=password,StatusActive=True).exists():
                get_user = JP_Users.objects.get(Username=username,Password=password, StatusActive=True)
                print(get_user)
                if len(str(get_user)) > 0:
                    print('inside if')
                    #kwargs['UserId'] = get_user

                get_devices = JP_Devices.objects.all()
                print(get_devices)
                if len(get_devices) > 0:
                    output = '{"error_code":"200","Response":"Successfully got %d companies", \n "get_devices":' %len(get_devices)
                    output += '['
                    counter = 0
                    for rec in get_devices:
                        counter += 1
                        if(counter == 1):
                            output += '{"serial_id":"%s","device_name":"%s","device_mac":"%s"}' %(rec.DeviceId ,rec.DeviceName,rec.DeviceMac)
                        else: 
                            output += ',\n {"serial_id":"%s","device_name":"%s","device_mac":"%s"}' %(rec.DeviceId ,rec.DeviceName,rec.DeviceMac)

                    output += ']\n'
                    output += '}'
                    logging.debug("get_devices:"+ output)
                    return HttpResponse(output)
                else:
                    output = '{"error_code":"403", "error_desc": "Response=Failed to get get_devices records, NO_DATA_FOUND"}' 
                    logging.debug("get_devices:"+ output)
                    return HttpResponse(output)
                    
            else:
                output = '{"error_code":"401","error_desc":"Response=Failed to Authenticate the user for get_devices"}'
                logging.debug("get_devices:"+ output)
                return HttpResponse(output)

        except Exception as e:
            err_desc = 'get_devices:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
            logging.debug("get_devices:"+ err_desc)
            output = '{"error_code":"500","error_desc":"Response=Failed to get the get_devices"}'
            logging.debug("get_devices:"+ output)
            return HttpResponse(output)
    
    else:
        logging.debug("get_devices: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output = '{"error_code":"405","error_desc":"Response=GET is not supported"}'
        logging.debug("get_devices:"+ output)
        return HttpResponse(output)

######################################################################
def add_data(request):
    if(request.method == "POST"):
        logging.debug("add_data: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output_str = "add_data - Unable to Authenticate/add_data... " 
        logging.debug("add_data:input- "+str(request.body))
        try:
            print(request.body)
            data = json.loads(eval(str(request.body)))
            print (data)
        except ValueError as e:
            output_str += ",invalid input, no proper JSON request "
            output = '{"error_code":"400", "error_desc": "Response=%s"}' %(output_str)
            logging.debug("add_data:"+ output)
            HttpResponse(output)
        try:
            device = JP_Devices.objects.get(DeviceMac=data['macid'])
            print('device is : ',device.DeviceId)
           
            # data2={}
            # for key in data:
            #     if key != 'macid':
            #         data2[key]=data[key]
            #         #d2=PipeData.objects.filter(DeviceId=device.DeviceId,attrs=key)
            # print(data2)
            add_data_rec = JP_Device_Data(DeviceId=device,Voltage=data['V'])
            add_data_rec.save()
            print(add_data_rec.DeviceId)
            if(len(str(add_data_rec.DeviceId)) > 0):
                output = '{"error_code":"200","Response":"Successfully added the data"}' 
                logging.debug("add_data:"+ output)
                return HttpResponse(output)
            else:
                output = '{"error_code":"409","error_desc":"Response=Failed to add the data"}'
                logging.debug("add_data:"+ output)
                return HttpResponse(output)

            # d2 = JP_Device_Data.objects.create(DeviceId=device,attrs=data2)
            # print('d2 key is :',d2)
            # d3=JP_Device_Data.objects.filter(DeviceId=device)
            # for data3 in d3:
            #     print(data3.attrs)

                    
            # deviceData = PipeData(DeviceId=device,UserId=user)
            # deviceData.save();
            # print('deviceData ' , deviceData)
            # print('sending data is :',device.DeviceId,user.username)
            # output = '{"error_code":"200", "Response":"Successfully added the data","DeviceId":"%s"}' %(device.DeviceId)
            # return HttpResponse(output)
            # d1=ShopItem.objects.create(name='Camembert')
            # print(d1)
            # d2=ShopItem.objects.create(name='Cheddar', attrs={'smelliness': 15, 'hardness': 5})
            # print(d2)

        
        except Exception as e:

            err_desc = 'add_data:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
            logging.debug("add_data:"+ err_desc)
            output = '{"error_code":"500", "error_desc": "Response=Failed to add the data"}'
            logging.debug("add_data:"+ output)
            return HttpResponse(output)
         
    else:
        logging.debug("add_data: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output = '{"error_code":"405", "error_desc": "Response=GET is not supported"}'
        logging.debug("add_data:"+ output)
        return HttpResponse(output)

######################################################################
def add_snipet(request):
    if(request.method == "POST"):
        logging.debug("add_snipet: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output_str = "add_snipet - Unable to Authenticate/add_snipet... " 
        logging.debug("add_snipet:input- "+str(request.body))
        try:
            print(request.body)
            data = json.loads(request.body)
            print (data)
        except ValueError as e:
            output_str += ",invalid input, no proper JSON request "
            output = '{"error_code":"400", "error_desc": "Response=%s"}' %(output_str)
            logging.debug("add_snipet:"+ output)
            HttpResponse(output)
        try:

            kwargs = {}
            if((data.get('UserId') is None) or ((data.get('UserId') is not  None) and (len(data['UserId']) <= 0))):
                output_str += ",UserId is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("add_snipet:"+ output)
                return HttpResponse(output)
            else:
                userid    = data['UserId']
                #kwargs['UserId'] = userid

            get_user = JP_Users.objects.get(UserId=userid)
            print('userid is : ',get_user)
            #print(get_user.id)
            data2={}
            for key in data:
                if key != 'UserId':
                    data2[key]=str(data[key])
                    #d2=PipeData.objects.filter(DeviceId=device.DeviceId,attrs=key)
            print(data2)
            add_snipet_data = JP_User_Snipet(UserId=get_user,SniptDesc=str(data2))
            add_snipet_data.save()
            print(add_snipet_data.SniptDesc)
            if(len(str(add_snipet_data.SniptDesc)) > 0):
                output = '{"error_code":"200","Response":"Successfully added the snipet"}' 
                logging.debug("add_snipet:"+ output)
                return HttpResponse(output)
            else:
                output = '{"error_code":"409","error_desc":"Response=Failed to add the snipet"}'
                logging.debug("add_snipet:"+ output)
                return HttpResponse(output)
        
        except Exception as e:

            err_desc = 'add_snipet:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
            logging.debug("add_snipet:"+ err_desc)
            output = '{"error_code":"500", "error_desc": "Response=Failed to add the data"}'
            logging.debug("add_snipet:"+ output)
            return HttpResponse(output)
         
    else:
        logging.debug("add_snipet: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output = '{"error_code":"405", "error_desc": "Response=GET is not supported"}'
        logging.debug("add_snipet:"+ output)
        return HttpResponse(output)

##################### get devices #############################
def get_snipets(request):
    if(request.method == "POST"):
        logging.debug("get_snipets: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output_str = "get_snipets - Unable to Authenticate/get_snipets... " 
        logging.debug("get_snipets:input- "+str(request.body))
        try:
            data = json.loads(request.body)
            print (request.body)
        except ValueError:
            output_str += ",invalid input, no proper JSON request "
            output = '{"error_code":"400","error_desc":"Response=%s"}' %(output_str )
            logging.debug("get_snipets:"+ output)
            return HttpResponse(output)
        try:
            kwargs = {}
            if((data.get('Username') is None) or ((data.get('Username') is not  None) and (len(data['Username']) <= 0))):
                output_str += ",Username is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("get_snipets:"+ output)
                return HttpResponse(output)
            else:
                username    = data['Username']
                kwargs['Username'] = username
            if((data.get('Password') is None) or ((data.get('Password') is not  None) and (len(data['Password']) <= 0))):
                output_str += ",Password is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("get_snipets:"+ output)
                return HttpResponse(output)
            else:
                password    = data['Password']
                kwargs['Password'] = password

            if JP_Users.objects.filter(Username=username,Password=password,StatusActive=True).exists():
                get_user = JP_Users.objects.get(Username=username,Password=password, StatusActive=True)
                print(get_user)
                if len(str(get_user)) > 0:
                    print('inside if')
                    #kwargs['UserId'] = get_user


                get_snipets_recs = JP_User_Snipet.objects.filter(UserId=get_user)
                
                if len(get_snipets_recs) > 0:
                    output = '{"error_code":"200","Response":"Successfully got %d snipets", \n "get_snipets":' %len(get_snipets_recs)
                    output += '['
                    counter = 0
                    lit_volatge=[]
                    for rec in get_snipets_recs:
                        counter += 1
                        print(rec.SniptDesc)
                        data2 = eval(str(rec.SniptDesc))
                        print('json dumps : ',data2 , type(data2))
                        #data3 = json.loads(data2)
                        #print('json loads : ',data3)
                        print(data2['param1'])
                        # for key in data2:
                        #     pass
                            # if key not 'frequency':
                            #     if key == 


                        if(counter == 1):
                            output += '{"snipet_id":"%s","snipet_name":"%s","min":"%s"' %(1,'snipet_Name',20)
                        else: 
                            output += ',\n {"snipet_id":"%s","snipet_name":"%s","min":"%s"' %(1,'snipet_Name',20)
                    output += ']\n'
                    output += '}'
                    logging.debug("get_snipets:"+ output)
                    return HttpResponse(output)
                else:
                    output = '{"error_code":"403", "error_desc": "Response=Failed to get get_snipets records, NO_DATA_FOUND"}' 
                    logging.debug("get_snipets:"+ output)
                    return HttpResponse(output)
                    
            else:
                output = '{"error_code":"401","error_desc":"Response=Failed to Authenticate the user for get_snipets"}'
                logging.debug("get_snipets:"+ output)
                return HttpResponse(output)

        except Exception as e:
            err_desc = 'get_snipets:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
            logging.debug("get_snipets:"+ err_desc)
            output = '{"error_code":"500","error_desc":"Response=Failed to get the get_snipets"}'
            logging.debug("get_snipets:"+ output)
            return HttpResponse(output)
    
    else:
        logging.debug("get_snipets: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output = '{"error_code":"405","error_desc":"Response=GET is not supported"}'
        logging.debug("get_snipets:"+ output)
        return HttpResponse(output)
################ company views #################
##################### add company #############################
def add_company(request): 
    if(request.method == "POST"):
        logging.debug("add_company: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output_str = "add_company- Unable to Authenticate/add_company... "
        logging.debug("add_company:input- "+str(request.body))
        try:
            data = json.loads(request.body)
            print (request.body)
        except ValueError as e:
            output_str += ",invalid input, no proper JSON request "
            output = '{"error_code":"400","error_desc":"Response=%s"}' %(output_str)
            logging.debug("add_company:"+ output)
            HttpResponse(output)
        try:
            kwargs = {}
            if((data.get('UserId') is None) or ((data.get('UserId') is not  None) and (len(data['UserId']) <= 0))):
                output_str += ",UserId is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("add_company:"+ output)
                return HttpResponse(output)
            else:
                userid    = data['UserId']
                get_user = JP_Users.objects.get(UserId=userid,StatusActive=True)
                print(get_user)
                if len(str(get_user)) > 0:
                    print('inside if')
                    kwargs['UserId'] = get_user


            if((data.get('CName') is None) or ((data.get('CName') is not  None) and (len(data['CName']) <= 0))):
                output_str += ",CName is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("add_company:"+ output)
                return HttpResponse(output)
            else:
                cname    = data['CName']
                kwargs['CName'] = cname
            if((data.get('CDesc') is not  None) and (len(data['CDesc']) > 0)):
                cdesc = data['CDesc']     
                kwargs['CDesc'] = cdesc
            if((data.get('CAddress') is not  None) and (len(data['CAddress']) > 0)):
                caddress = data['CAddress']     
                kwargs['CAddress'] = caddress
            
            logging.debug("add_company:input: company="+cname)
            
            check_company = JP_Company.objects.filter(UserId=get_user ,CName=cname)
            print(check_company)
            if len(check_company) > 0:
                output = '{"error_code":"429","error_desc":"Response=company already associated"}' 
                logging.debug("add_company:"+ output)
                return HttpResponse(output)
            else:
                add_comp_rec=JP_Company(**kwargs);
                add_comp_rec.save()
                print(add_comp_rec.CName)
                if(len(str(add_comp_rec.CName)) > 0):
                    output = '{"error_code":"200","Response":"Successfully added the company, %s"}' %(cname)
                    logging.debug("add_company:"+ output)
                    return HttpResponse(output)
                else:
                    output = '{"error_code":"409","error_desc":"Response=Failed to add the company"}'
                    logging.debug("add_company:"+ output)
                    return HttpResponse(output)
        except Exception as e:
            err_desc = 'add_company:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
            logging.debug("add_company:"+ err_desc)
            output = '{"error_code":"500","error_desc":"Response=Failed to add the company"}'
            logging.debug("add_company:"+ output)
            return HttpResponse(output)
    
    else:
        logging.debug("add_company: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output = '{"error_code":"405","error_desc":"Response=GET is not supported"}'
        logging.debug("add_company:"+ output)
        return HttpResponse(output)

##################### add company #############################
def update_company(request): 
    if(request.method == "POST"):
        logging.debug("update_company: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output_str = "update_company- Unable to Authenticate/update_company... "
        logging.debug("update_company:input- "+str(request.body))
        try:
            data = json.loads(request.body)
            print (request.body)
        except ValueError as e:
            output_str += ",invalid input, no proper JSON request "
            output = '{"error_code":"400","error_desc":"Response=%s"}' %(output_str)
            logging.debug("update_company:"+ output)
            HttpResponse(output)
        try:
            kwargs = {}
            if((data.get('company_id') is None) or ((data.get('company_id') is not  None) and (len(data['company_id']) <= 0))):
                output_str += ",company_id is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("update_company:"+ output)
                return HttpResponse(output)
            else:
                cid    = data['company_id']
                

            if((data.get('CName') is not  None) and (len(data['CName']) > 0)):
                cname = data['CName']     
                kwargs['CName'] = cname

            if((data.get('CDesc') is not  None) and (len(data['CDesc']) > 0)):
                cdesc = data['CDesc']     
                kwargs['CDesc'] = cdesc
            if((data.get('CAddress') is not  None) and (len(data['CAddress']) > 0)):
                caddress = data['CAddress']     
                kwargs['CAddress'] = caddress
            
            logging.debug("update_company:input: company="+cname)
            kwargs['Change_Date'] = datetime.now()
            get_company = JP_Company.objects.get(CId=cid,StatusActive=True)
            print(get_company)
            if len(str(get_company)) > 0:
                print('inside if')
                #kwargs['CId'] = get_company
                update_company = JP_Company.objects.filter(CId=cid).update(**kwargs)
                print(update_company)
                if update_company > 0:
                    output = '{"error_code":"200","Response":"Successfully added the company, %s"}' %(cname)
                    logging.debug("update_company:"+ output)
                    return HttpResponse(output)
                    
                else:
                    output = '{"error_code":"409","error_desc":"Response=Failed to update the company"}'
                    logging.debug("update_company:"+ output)
                    return HttpResponse(output)
            else:
                output = '{"error_code":"403", "error_desc": "Response=Failed to get update_company records, NO_DATA_FOUND"}' 
                logging.debug("update_company:"+ output)
                return HttpResponse(output)


        except Exception as e:
            err_desc = 'update_company:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
            logging.debug("update_company:"+ err_desc)
            output = '{"error_code":"500","error_desc":"Response=Failed to update the company"}'
            logging.debug("update_company:"+ output)
            return HttpResponse(output)
    
    else:
        logging.debug("update_company: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output = '{"error_code":"405","error_desc":"Response=GET is not supported"}'
        logging.debug("update_company:"+ output)
        return HttpResponse(output)


##################### get jpipe companies #############################
def get_jpipe_companies(request):
    if(request.method == "POST"):
        logging.debug("get_jpipe_companies: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output_str = "get_jpipe_companies - Unable to Authenticate/get_jpipe_companies... " 
        logging.debug("get_jpipe_companies:input- "+str(request.body))
        try:
            data = json.loads(request.body)
            print (request.body)
        except ValueError:
            output_str += ",invalid input, no proper JSON request "
            output = '{"error_code":"2","error_desc":"Response=%s"}' %(output_str )
            logging.debug("get_jpipe_companies:"+ output)
            return HttpResponse(output)
        try:
            kwargs = {}
            if((data.get('Username') is None) or ((data.get('Username') is not  None) and (len(data['Username']) <= 0))):
                output_str += ",Username is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("get_jpipe_companies:"+ output)
                return HttpResponse(output)
            else:
                username    = data['Username']
                kwargs['Username'] = username
            if((data.get('Password') is None) or ((data.get('Password') is not  None) and (len(data['Password']) <= 0))):
                output_str += ",Password is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("get_jpipe_companies:"+ output)
                return HttpResponse(output)
            else:
                password    = data['Password']
                kwargs['Password'] = password

            if JP_Users.objects.filter(Username=username,Password=password,StatusActive=True).exists():
                get_user = JP_Users.objects.get(Username=username,Password=password, StatusActive=True)
                print(get_user)
                if len(str(get_user)) > 0:
                    print('inside if')
                    kwargs['UserId'] = get_user

                get_companies = JP_Company.objects.filter(UserId=get_user)
                print(get_companies)
                if len(get_companies) > 0:
                    output = '{"error_code":"200","Response":"Successfully got %d companies", \n "get_jpipe_companies":' %len(get_companies)
                    output += '['
                    counter = 0
                    for rec in get_companies:
                        counter += 1
                        if(counter == 1):
                            output += '{"company_id":"%s","company_name":"%s","company_desc":"%s","company_address":"%s"}' %(rec.CId ,rec.CName,rec.CDesc,rec.CAddress)
                        else: 
                            output += ',\n {"company_id":"%s","company_name":"%s","company_desc":"%s","company_address":"%s"}' %(rec.CId ,rec.CName,rec.CDesc,rec.CAddress)

                    output += ']\n'
                    output += '}'
                    logging.debug("get_jpipe_companies:"+ output)
                    return HttpResponse(output)
                else:
                    output = '{"error_code":"403", "error_desc": "Response=Failed to get get_jpipe_companies records, NO_DATA_FOUND"}' 
                    logging.debug("get_jpipe_companies:"+ output)
                    return HttpResponse(output)
                    
            else:
                output = '{"error_code":"401","error_desc":"Response=Failed to Authenticate the user for get_jpipe_companies"}'
                logging.debug("get_jpipe_companies:"+ output)
                return HttpResponse(output)

        except Exception as e:
            err_desc = 'get_jpipe_companies:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
            logging.debug("get_jpipe_companies:"+ err_desc)
            output = '{"error_code":"500","error_desc":"Response=Failed to get the get_jpipe_companies"}'
            logging.debug("get_jpipe_companies:"+ output)
            return HttpResponse(output)
    
    else:
        logging.debug("get_jpipe_companies: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output = '{"error_code":"405","error_desc":"Response=GET is not supported"}'
        logging.debug("get_jpipe_companies:"+ output)
        return HttpResponse(output)
##################### add company users #############################
def add_company_user(request): 
    if(request.method == "POST"):
        logging.debug("add_company_user: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output_str = "add_company_user- Unable to Authenticate/add_company_user... "
        logging.debug("add_company_user:input- "+str(request.body))
        try:
            data = json.loads(request.body)
            print (request.body)
        except ValueError as e:
            output_str += ",invalid input, no proper JSON request "
            output = '{"error_code":"400","error_desc":"Response=%s"}' %(output_str)
            logging.debug("add_company_user:"+ output)
            HttpResponse(output)
        try:
            kwargs = {}
            if((data.get('CUsername') is None) or ((data.get('CUsername') is not  None) and (len(data['CUsername']) <= 0))):
                output_str += ",CUsername is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("add_company_user:"+ output)
                return HttpResponse(output)
            else:
                cusername    = data['CUsername']
                kwargs['CUsername'] = cusername


            if((data.get('CPassword') is None) or ((data.get('CPassword') is not  None) and (len(data['CPassword']) <= 0))):
                output_str += ",CPassword is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("add_company_user:"+ output)
                return HttpResponse(output)
            else:
                cpassword    = data['CPassword']
                kwargs['CPassword'] = cpassword

            if((data.get('CId') is None) or ((data.get('CId') is not  None) and (len(data['CId']) <= 0))):
                output_str += ",CId is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("add_company_user:"+ output)
                return HttpResponse(output)
            else:
                cid    = data['CId']
                get_company = JP_Company.objects.get(CId=cid,StatusActive=True)
                print(get_company)
                if len(str(get_company)) > 0:
                    print('inside if')
                    kwargs['CId'] = get_company

            if((data.get('CUname') is not  None) and (len(data['CUname']) > 0)):
                cuname = data['CUname']     
                kwargs['CUname'] = cuname
            logging.debug("add_company_user:input: company="+cusername)
            
            check_company_user = JP_Company_Users.objects.filter(CUsername=cusername ,StatusActive=True,CId=get_company)
            print(check_company_user)
            if len(check_company_user) > 0:
                output = '{"error_code":"429","error_desc":"Response=company user already associated"}' 
                logging.debug("add_company_user:"+ output)
                return HttpResponse(output)
            else:
                add_comp_rec=JP_Company_Users(**kwargs);
                add_comp_rec.save()
                print(add_comp_rec.CUsername)
                if(len(str(add_comp_rec.CUsername)) > 0):
                    output = '{"error_code":"200","Response":"Successfully added the company user, %s"}' %(cusername)
                    logging.debug("add_company_user:"+ output)
                    return HttpResponse(output)
                else:
                    output = '{"error_code":"409","error_desc":"Response=Failed to add the company user"}'
                    logging.debug("add_company_user:"+ output)
                    return HttpResponse(output)
        except Exception as e:
            err_desc = 'add_company_user:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
            logging.debug("add_company_user:"+ err_desc)
            output = '{"error_code":"500","error_desc":"Response=Failed to add the company"}'
            logging.debug("add_company_user:"+ output)
            return HttpResponse(output)
    
    else:
        logging.debug("add_company_user: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output = '{"error_code":"405","error_desc":"Response=GET is not supported"}'
        logging.debug("add_company_user:"+ output)
        return HttpResponse(output)



##################### get jpipe company users #############################
def get_company_users(request):
    if(request.method == "POST"):
        logging.debug("get_company_users: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output_str = "get_company_users - Unable to Authenticate/get_company_users... " 
        logging.debug("get_company_users:input- "+str(request.body))
        try:
            data = json.loads(request.body)
            print (request.body)
        except ValueError:
            output_str += ",invalid input, no proper JSON request "
            output = '{"error_code":"2","error_desc":"Response=%s"}' %(output_str )
            logging.debug("get_company_users:"+ output)
            return HttpResponse(output)
        try:
            kwargs = {}
            if((data.get('Username') is None) or ((data.get('Username') is not  None) and (len(data['Username']) <= 0))):
                output_str += ",Username is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("get_company_users:"+ output)
                return HttpResponse(output)
            else:
                username    = data['Username']
                kwargs['Username'] = username
            if((data.get('Password') is None) or ((data.get('Password') is not  None) and (len(data['Password']) <= 0))):
                output_str += ",Password is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("get_company_users:"+ output)
                return HttpResponse(output)
            else:
                password    = data['Password']
                kwargs['Password'] = password

            if JP_Users.objects.filter(Username=username,Password=password,StatusActive=True).exists():
                get_user = JP_Users.objects.get(Username=username,Password=password, StatusActive=True)
                print(get_user)
                if len(str(get_user)) > 0:
                    print('inside if')
                    kwargs['UserId'] = get_user

                get_company_id = JP_Company.objects.get(UserId=get_user)
                print(get_company_id)
                get_company_user = JP_Company_Users.objects.filter(CId=get_company_id)
                if len(get_company_user) > 0:
                    output = '{"error_code":"200","Response":"Successfully got %d company users", \n "get_company_user":' %len(get_company_user)
                    output += '['
                    counter = 0
                    for rec in get_company_user:
                        counter += 1
                        if(counter == 1):
                            output += '{"userid":"%s","name":"%s","username":"%s"}' %(rec.CUId ,rec.CUname,rec.CUsername)
                        else: 
                            output += ',\n {"userid":"%s","name":"%s","username":"%s"}' %(rec.CUId ,rec.CUname,rec.CUsername)

                    output += ']\n'
                    output += '}'
                    logging.debug("get_company_users:"+ output)
                    return HttpResponse(output)
                else:
                    output = '{"error_code":"403", "error_desc": "Response=Failed to get get_company_users records, NO_DATA_FOUND"}' 
                    logging.debug("get_company_users:"+ output)
                    return HttpResponse(output)
                    
            else:
                output = '{"error_code":"401","error_desc":"Response=Failed to Authenticate the user for get_company_users"}'
                logging.debug("get_company_users:"+ output)
                return HttpResponse(output)

        except Exception as e:
            err_desc = 'get_company_users:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
            logging.debug("get_company_users:"+ err_desc)
            output = '{"error_code":"500","error_desc":"Response=Failed to get the get_company_users"}'
            logging.debug("get_company_users:"+ output)
            return HttpResponse(output)
    
    else:
        logging.debug("get_company_users: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output = '{"error_code":"405","error_desc":"Response=GET is not supported"}'
        logging.debug("get_company_users:"+ output)
        return HttpResponse(output)


##################### add device config type #############################
def add_dconfig_Type(request): 
    if(request.method == "POST"):
        logging.debug("add_dconfig_Type: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output_str = "add_dconfig_Type- Unable to Authenticate/add_dconfig_Type... "
        logging.debug("add_dconfig_Type:input- "+str(request.body))
        try:
            data = json.loads(request.body)
            print (request.body)
        except ValueError as e:
            output_str += ",invalid input, no proper JSON request "
            output = '{"error_code":"400","error_desc":"Response=%s"}' %(output_str)
            logging.debug("add_dconfig_Type:"+ output)
            HttpResponse(output)
        try:
            kwargs = {}
            if((data.get('CTdesc') is None) or ((data.get('CTdesc') is not  None) and (len(data['CTdesc']) <= 0))):
                output_str += ",CTdesc is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("add_dconfig_Type:"+ output)
                return HttpResponse(output)
            else:
                ctdesc    = data['CTdesc']
                kwargs['CTdesc'] = ctdesc
            check_dconfig_param = JP_Dconfig_Type.objects.filter(CTdesc=ctdesc)
            print(check_dconfig_param)
            if len(check_dconfig_param) > 0:
                output = '{"error_code":"429","error_desc":"Response=param value already associated"}' 
                logging.debug("add_dconfig_Type:"+ output)
                return HttpResponse(output)
            else:
                add_config_rec=JP_Dconfig_Type(**kwargs);
                add_config_rec.save()
                print(add_config_rec.CTdesc)
                if(len(str(add_config_rec.CTdesc)) > 0):
                    output = '{"error_code":"200","Response":"Successfully added the param value"}' 
                    logging.debug("add_dconfig_Type:"+ output)
                    return HttpResponse(output)
                else:
                    output = '{"error_code":"409","error_desc":"Response=Failed to add the param value"}'
                    logging.debug("add_dconfig_Type:"+ output)
                    return HttpResponse(output)
        except Exception as e:
            err_desc = 'add_dconfig_Type:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
            logging.debug("add_dconfig_Type:"+ err_desc)
            output = '{"error_code":"500","error_desc":"Response=Failed to add the param value"}'
            logging.debug("add_dconfig_Type:"+ output)
            return HttpResponse(output)
    
    else:
        logging.debug("add_dconfig_Type: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output = '{"error_code":"405","error_desc":"Response=GET is not supported"}'
        logging.debug("add_dconfig_Type:"+ output)
        return HttpResponse(output)


##################### get_dconfig_Type #############################
def get_dconfig_Type(request):
    if(request.method == "POST"):
        logging.debug("get_dconfig_Type: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output_str = "get_dconfig_Type - Unable to Authenticate/get_dconfig_Type... " 
        logging.debug("get_dconfig_Type:input- "+str(request.body))
        try:
            data = json.loads(request.body)
            print (request.body)
        except ValueError:
            output_str += ",invalid input, no proper JSON request "
            output = '{"error_code":"2","error_desc":"Response=%s"}' %(output_str )
            logging.debug("get_dconfig_Type:"+ output)
            return HttpResponse(output)
        try:
            kwargs = {}
            if((data.get('Username') is None) or ((data.get('Username') is not  None) and (len(data['Username']) <= 0))):
                output_str += ",Username is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("get_dconfig_Type:"+ output)
                return HttpResponse(output)
            else:
                username    = data['Username']
                kwargs['CUsername'] = username
            if((data.get('Password') is None) or ((data.get('Password') is not  None) and (len(data['Password']) <= 0))):
                output_str += ",Password is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("get_dconfig_Type:"+ output)
                return HttpResponse(output)
            else:
                password    = data['Password']
                kwargs['CPassword'] = password

            if JP_Company_Users.objects.filter(CUsername=username,CPassword=password,StatusActive=True).exists():
                get_user = JP_Company_Users.objects.get(CUsername=username,CPassword=password, StatusActive=True)
                print(get_user)
                if len(str(get_user)) > 0:
                    print('inside if')
                    kwargs['UserId'] = get_user

                get_dconfig_type = JP_Dconfig_Type.objects.all()
                print(get_dconfig_type)
                if len(get_dconfig_type) > 0:
                    output = '{"error_code":"200","Response":"Successfully got %d types", \n "get_dconfig_Type":' %len(get_dconfig_type)
                    output += '['
                    counter = 0
                    for rec in get_dconfig_type:
                        counter += 1
                        if(counter == 1):
                            output += '{"type_id":"%s","type_desc":"%s"}' %(rec.CTid ,rec.CTdesc)
                        else: 
                            output += ',\n {"type_id":"%s","type_desc":"%s"}' %(rec.CTid ,rec.CTdesc)

                    output += ']\n'
                    output += '}'
                    logging.debug("get_dconfig_Type:"+ output)
                    return HttpResponse(output)
                else:
                    output = '{"error_code":"403", "error_desc": "Response=Failed to get get_dconfig_Type records, NO_DATA_FOUND"}' 
                    logging.debug("get_dconfig_Type:"+ output)
                    return HttpResponse(output)
                    
            else:
                output = '{"error_code":"401","error_desc":"Response=Failed to Authenticate the user for get_dconfig_Type"}'
                logging.debug("get_dconfig_Type:"+ output)
                return HttpResponse(output)

        except Exception as e:
            err_desc = 'get_dconfig_Type:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
            logging.debug("get_dconfig_Type:"+ err_desc)
            output = '{"error_code":"500","error_desc":"Response=Failed to get the get_dconfig_Type"}'
            logging.debug("get_dconfig_Type:"+ output)
            return HttpResponse(output)
    
    else:
        logging.debug("get_dconfig_Type: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output = '{"error_code":"405","error_desc":"Response=GET is not supported"}'
        logging.debug("get_dconfig_Type:"+ output)
        return HttpResponse(output)


############ add device config type if serial select#######################
def add_serial_Type(request): 
    if(request.method == "POST"):
        logging.debug("add_serial_Type: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output_str = "add_serial_Type- Unable to Authenticate/add_serial_Type... "
        logging.debug("add_serial_Type:input- "+str(request.body))
        try:
            data = json.loads(request.body)
            print (request.body)
        except ValueError as e:
            output_str += ",invalid input, no proper JSON request "
            output = '{"error_code":"400","error_desc":"Response=%s"}' %(output_str)
            logging.debug("add_serial_Type:"+ output)
            HttpResponse(output)
        try:
            kwargs = {}
            if((data.get('TSdesc') is None) or ((data.get('TSdesc') is not  None) and (len(data['TSdesc']) <= 0))):
                output_str += ",TSdesc is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("add_serial_Type:"+ output)
                return HttpResponse(output)
            else:
                tsdesc    = data['TSdesc']
                kwargs['TSdesc'] = tsdesc
            check_dconfig_param = JP_DCType_Serial.objects.filter(TSdesc=tsdesc)
            print(check_dconfig_param)
            if len(check_dconfig_param) > 0:
                output = '{"error_code":"429","error_desc":"Response=param value already associated"}' 
                logging.debug("add_serial_Type:"+ output)
                return HttpResponse(output)
            else:
                add_config_rec=JP_DCType_Serial(**kwargs);
                add_config_rec.save()
                print(add_config_rec.TSdesc)
                if(len(str(add_config_rec.TSdesc)) > 0):
                    output = '{"error_code":"200","Response":"Successfully added the param value"}' 
                    logging.debug("add_serial_Type:"+ output)
                    return HttpResponse(output)
                else:
                    output = '{"error_code":"409","error_desc":"Response=Failed to add the param value"}'
                    logging.debug("add_serial_Type:"+ output)
                    return HttpResponse(output)
        except Exception as e:
            err_desc = 'add_serial_Type:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
            logging.debug("add_serial_Type:"+ err_desc)
            output = '{"error_code":"500","error_desc":"Response=Failed to add the param value"}'
            logging.debug("add_serial_Type:"+ output)
            logging.debug("add_serial_Type:"+ str(e))

            return HttpResponse(output)
    
    else:
        logging.debug("add_serial_Type: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output = '{"error_code":"405","error_desc":"Response=GET is not supported"}'
        logging.debug("add_dconfig_Type:"+ output)
        return HttpResponse(output)

##################### add device config operations #############################
def add_dconfig_Operations(request): 
    if(request.method == "POST"):
        logging.debug("add_dconfig_Operations: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output_str = "add_dconfig_Operations- Unable to Authenticate/add_dconfig_Operations... "
        logging.debug("add_dconfig_Operations:input- "+str(request.body))
        try:
            data = json.loads(request.body)
            print (request.body)
        except ValueError as e:
            output_str += ",invalid input, no proper JSON request "
            output = '{"error_code":"400","error_desc":"Response=%s"}' %(output_str)
            logging.debug("add_dconfig_Operations:"+ output)
            HttpResponse(output)
        try:
            kwargs = {}
            if((data.get('COdesc') is None) or ((data.get('COdesc') is not  None) and (len(data['COdesc']) <= 0))):
                output_str += ",COdesc is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("add_dconfig_Operations:"+ output)
                return HttpResponse(output)
            else:
                codesc    = data['COdesc']
                kwargs['COdesc'] = codesc
            check_dconfig_param = JP_Dconfig_Operations.objects.filter(COdesc=codesc)
            print(check_dconfig_param)
            if len(check_dconfig_param) > 0:
                output = '{"error_code":"429","error_desc":"Response=param value already associated"}' 
                logging.debug("add_dconfig_Operations:"+ output)
                return HttpResponse(output)
            else:
                add_config_rec=JP_Dconfig_Operations(**kwargs);
                add_config_rec.save()
                print(add_config_rec.COdesc)
                if(len(str(add_config_rec.COdesc)) > 0):
                    output = '{"error_code":"200","Response":"Successfully added the param value"}' 
                    logging.debug("add_dconfig_Operations:"+ output)
                    return HttpResponse(output)
                else:
                    output = '{"error_code":"409","error_desc":"Response=Failed to add the param value"}'
                    logging.debug("add_dconfig_Operations:"+ output)
                    return HttpResponse(output)
        except Exception as e:
            err_desc = 'add_dconfig_Operations:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
            logging.debug("add_dconfig_Operations:"+ err_desc)
            output = '{"error_code":"500","error_desc":"Response=Failed to add the param value"}'
            logging.debug("add_dconfig_Operations:"+ output)
            return HttpResponse(output)
    
    else:
        logging.debug("add_dconfig_Operations: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output = '{"error_code":"405","error_desc":"Response=GET is not supported"}'
        logging.debug("add_dconfig_Type:"+ output)
        return HttpResponse(output)



##################### get_dconfig_Operations #############################
def get_dconfig_Operations(request):
    if(request.method == "POST"):
        logging.debug("get_dconfig_Operations: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output_str = "get_dconfig_Operations - Unable to Authenticate/get_dconfig_Operations... " 
        logging.debug("get_dconfig_Operations:input- "+str(request.body))
        try:
            data = json.loads(request.body)
            print (request.body)
        except ValueError:
            output_str += ",invalid input, no proper JSON request "
            output = '{"error_code":"2","error_desc":"Response=%s"}' %(output_str )
            logging.debug("get_dconfig_Operations:"+ output)
            return HttpResponse(output)
        try:
            kwargs = {}
            if((data.get('Username') is None) or ((data.get('Username') is not  None) and (len(data['Username']) <= 0))):
                output_str += ",Username is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("get_dconfig_Operations:"+ output)
                return HttpResponse(output)
            else:
                username    = data['Username']
                kwargs['CUsername'] = username
            if((data.get('Password') is None) or ((data.get('Password') is not  None) and (len(data['Password']) <= 0))):
                output_str += ",Password is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("get_dconfig_Operations:"+ output)
                return HttpResponse(output)
            else:
                password    = data['Password']
                kwargs['CPassword'] = password

            if JP_Company_Users.objects.filter(CUsername=username,CPassword=password,StatusActive=True).exists():
                get_user = JP_Company_Users.objects.get(CUsername=username,CPassword=password, StatusActive=True)
                print(get_user)
                if len(str(get_user)) > 0:
                    print('inside if')
                    kwargs['UserId'] = get_user

                get_dconfig_type = JP_Dconfig_Operations.objects.all()
                print(get_dconfig_type)
                if len(get_dconfig_type) > 0:
                    output = '{"error_code":"200","Response":"Successfully got %d operations", \n "get_dconfig_Operations":' %len(get_dconfig_type)
                    output += '['
                    counter = 0
                    for rec in get_dconfig_type:
                        counter += 1
                        if(counter == 1):
                            output += '{"operation_id":"%s","operation_desc":"%s"}' %(rec.COid ,rec.COdesc)
                        else: 
                            output += ',\n {"operation_id":"%s","operation_desc":"%s"}' %(rec.COid ,rec.COdesc)

                    output += ']\n'
                    output += '}'
                    logging.debug("get_dconfig_Operations:"+ output)
                    return HttpResponse(output)
                else:
                    output = '{"error_code":"403", "error_desc": "Response=Failed to get get_dconfig_Operations records, NO_DATA_FOUND"}' 
                    logging.debug("get_dconfig_Operations:"+ output)
                    return HttpResponse(output)
                    
            else:
                output = '{"error_code":"401","error_desc":"Response=Failed to Authenticate the user for get_dconfig_Operations"}'
                logging.debug("get_dconfig_Operations:"+ output)
                return HttpResponse(output)

        except Exception as e:
            err_desc = 'get_dconfig_Operations:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
            logging.debug("get_dconfig_Operations:"+ err_desc)
            output = '{"error_code":"500","error_desc":"Response=Failed to get the get_dconfig_Operations"}'
            logging.debug("get_dconfig_Operations:"+ output)
            return HttpResponse(output)
    
    else:
        logging.debug("get_dconfig_Operations: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output = '{"error_code":"405","error_desc":"Response=GET is not supported"}'
        logging.debug("get_dconfig_Operations:"+ output)
        return HttpResponse(output)



##################### add device config details #############################
def add_dconfig_details(request): 
    if(request.method == "POST"):
        logging.debug("add_dconfig_details: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output_str = "add_dconfig_details- Unable to Authenticate/add_dconfig_details... "
        logging.debug("add_dconfig_details:input- "+str(request.body))
        try:
            data = json.loads(request.body)
            print (request.body)
        except ValueError as e:
            output_str += ",invalid input, no proper JSON request "
            output = '{"error_code":"400","error_desc":"Response=%s"}' %(output_str)
            logging.debug("add_dconfig_details:"+ output)
            HttpResponse(output)
        try:
            kwargs = {}
            kwargs2 = {}
            if((data.get('UserId') is None) or ((data.get('UserId') is not  None) and (len(data['UserId']) <= 0))):
                output_str += ",UserId is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("add_dconfig_details:"+ output)
                return HttpResponse(output)
            else:
                userid    = data['UserId']
                
                get_user = JP_Company_Users.objects.get(CUId=userid,StatusActive=True)
                print(get_user)
                if len(str(get_user)) > 0:
                    kwargs['CUId'] = get_user
                    print('getting company instance',get_user.CId.CId)
                    get_company = JP_Company.objects.get(CId=get_user.CId.CId,StatusActive=True)
                    print(get_company)

                    if len(str(get_company)) > 0:
                        print('inside if')
                        kwargs['CId'] = get_company

            if((data.get('ConfigName') is None) or ((data.get('ConfigName') is not  None) and (len(data['ConfigName']) <= 0))):
                output_str += ",ConfigName is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("add_dconfig_details:"+ output)
                return HttpResponse(output)
            else:
                configname    = data['ConfigName']
                kwargs['ConfigName'] = configname
                add_config_rec=JP_Device_Config(**kwargs);
                add_config_rec.save()
                print(add_config_rec.ConfigId)
                if(len(str(add_config_rec.ConfigId)) > 0):
                    print('getting config company_id: ',add_config_rec,add_config_rec.ConfigId)
                    kwargs2['ConfigId']=add_config_rec

            if((data.get('Type') is None) or ((data.get('Type') is not  None) and (len(data['Type']) <= 0))):
                output_str += ",Type is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("add_dconfig_details:"+ output)
                return HttpResponse(output)
            else:
                ctype    = data['Type']
                get_type_id = JP_Dconfig_Type.objects.get(CTdesc=ctype,StatusActive=True)
                print(get_type_id)
                if len(str(get_type_id)) > 0:
                    print('inside if get_type_id')
                    kwargs2['CTid'] = get_type_id

            if((data.get('Operation') is None) or ((data.get('Operation') is not  None) and (len(data['Operation']) <= 0))):
                output_str += ",Operation is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("add_dconfig_details:"+ output)
                return HttpResponse(output)
            else:
                operation    = data['Operation']
                get_op_id = JP_Dconfig_Operations.objects.get(COdesc=operation,StatusActive=True)
                print(get_op_id)
                if len(str(get_op_id)) > 0:
                    print('inside if get_op_id')
                    kwargs2['COid'] = get_op_id


            if((data.get('Frequency') is None) or ((data.get('Frequency') is not  None) and (len(data['Frequency']) <= 0))):
                output_str += ",Frequency is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("add_dconfig_details:"+ output)
                return HttpResponse(output)
            else:
                frequency    = data['Frequency']
                time1 = datetime.strptime(frequency, '%H:%M:%S').time()
                kwargs2['Frequency'] = time1

            if((data.get('GpioPins') is None) or ((data.get('GpioPins') is not  None) and (len(data['GpioPins']) <= 0))):
                output_str += ",GpioPins is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("add_dconfig_details:"+ output)
                return HttpResponse(output)
            else:
                gpioPins    = data['GpioPins']
                kwargs2['GpioPins'] = gpioPins
     
            check_dconfig_details = JPD_Config_Details.objects.filter(**kwargs2)
            print(check_dconfig_details)
            if len(check_dconfig_details) > 0:
                output = '{"error_code":"429","error_desc":"Response= config details  already associated"}' 
                logging.debug("add_dconfig_details:"+ output)
                return HttpResponse(output)
            else:
                add_config_rec=JPD_Config_Details(**kwargs2);
                add_config_rec.save()
                print(add_config_rec.CDId)
                if(len(str(add_config_rec.CDId)) > 0):

                    output = '{"error_code":"200","Response":"Successfully added the config details"}' 
                    logging.debug("add_dconfig_details:"+ output)
                    return HttpResponse(output)
                else:
                    output = '{"error_code":"409","error_desc":"Response=Failed to add the config"}'
                    logging.debug("add_dconfig_details:"+ output)
                    return HttpResponse(output)
        except Exception as e:
            err_desc = 'add_dconfig_details:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
            logging.debug("add_dconfig_details:"+ err_desc)
            output = '{"error_code":"500","error_desc":"Response=Failed to add the config details"}'
            logging.debug("add_dconfig_details:"+ output)
            return HttpResponse(output)
    
    else:
        logging.debug("add_dconfig_details: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output = '{"error_code":"405","error_desc":"Response=GET is not supported"}'
        logging.debug("add_dconfig_details:"+ output)
        return HttpResponse(output)

##################### get jpipe company users #############################
def get_dconfig_details(request):
    if(request.method == "POST"):
        logging.debug("get_dconfig_details: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output_str = "get_dconfig_details - Unable to Authenticate/get_dconfig_details... " 
        logging.debug("get_dconfig_details:input- "+str(request.body))
        try:
            data = json.loads(request.body)
            print (request.body)
        except ValueError:
            output_str += ",invalid input, no proper JSON request "
            output = '{"error_code":"2","error_desc":"Response=%s"}' %(output_str )
            logging.debug("get_dconfig_details:"+ output)
            return HttpResponse(output)
        try:
            kwargs = {}
            if((data.get('Username') is None) or ((data.get('Username') is not  None) and (len(data['Username']) <= 0))):
                output_str += ",Username is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("get_dconfig_details:"+ output)
                return HttpResponse(output)
            else:
                username    = data['Username']
               
            if((data.get('Password') is None) or ((data.get('Password') is not  None) and (len(data['Password']) <= 0))):
                output_str += ",Password is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("get_dconfig_details:"+ output)
                return HttpResponse(output)
            else:
                password    = data['Password']
               
            jpipe_user = False
            company_user = False
            if JP_Users.objects.filter(Username=username,Password=password,StatusActive=True).exists():
                print('jpipe user')
                jpipe_user = True
                get_user = JP_Users.objects.get(Username=username,Password=password, StatusActive=True)
                print(get_user)
                if len(str(get_user)) > 0:
                    print('inside if')
                    get_company = JP_Company.objects.get(UserId=get_user, StatusActive=True)
                    kwargs['CId'] = get_company
            elif JP_Company_Users.objects.filter(CUsername=username,CPassword=password,StatusActive=True).exists():
                print('company user')
                company_user = True
                get_user = JP_Company_Users.objects.get(CUsername=username,CPassword=password,StatusActive=True)
                print(get_user)
                if len(str(get_user)) > 0:
                    kwargs['CUId'] = get_user

            else:
                output = '{"error_code":"401","error_desc":"Response=Failed to Authenticate the user for get_dconfig_details"}'
                logging.debug("get_dconfig_details:"+ output)
                return HttpResponse(output)


            if jpipe_user == True or company_user == True:
                print('inside jpipe_user if ')
                get_config_details = JP_Device_Config.objects.filter(**kwargs)
                print(get_config_details)
                if len(get_config_details) > 0:
                    output = '{"error_code":"200","Response":"Successfully got %d company users", \n "get_company_user":' %len(get_config_details)
                    output += '['
                    counter = 0
                    for rec in get_config_details:
                        counter += 1
                        if(counter == 1):
                            output += '{"config_id":"%s","config_name":"%s"}' %(rec.ConfigId,rec.ConfigName)
                        else: 
                            output += ',\n {"config_id":"%s","config_name":"%s"}' %(rec.ConfigId,rec.ConfigName)

                    output += ']\n'
                    output += '}'
                    logging.debug("get_dconfig_details:"+ output)
                    return HttpResponse(output)

                else:
                    output = '{"error_code":"403", "error_desc": "Response=Failed to get get_dconfig_details records, NO_DATA_FOUND"}' 
                    logging.debug("get_dconfig_details:"+ output)
                    return HttpResponse(output)
                    
            else:
                output = '{"error_code":"401","error_desc":"Response=Failed to Authenticate the user for get_dconfig_details"}'
                logging.debug("get_dconfig_details:"+ output)
                return HttpResponse(output)
                

        except Exception as e:
            err_desc = 'get_dconfig_details:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
            logging.debug("get_dconfig_details:"+ err_desc)
            output = '{"error_code":"500","error_desc":"Response=Failed to get the get_dconfig_details"}'
            logging.debug("get_dconfig_details:"+ output)
            return HttpResponse(output)
    
    else:
        logging.debug("get_dconfig_details: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output = '{"error_code":"405","error_desc":"Response=GET is not supported"}'
        logging.debug("get_dconfig_details:"+ output)
        return HttpResponse(output)

##################### add Config device mappings #############################
def add_device_config_mapping(request): 
    if(request.method == "POST"):
        logging.debug("add_device_config_mapping: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output_str = "add_device_config_mapping- Unable to Authenticate/add_device_config_mapping... "
        logging.debug("add_device_config_mapping:input- "+str(request.body))
        try:
            data = json.loads(request.body)
            print (request.body)
        except ValueError as e:
            output_str += ",invalid input, no proper JSON request "
            output = '{"error_code":"400","error_desc":"Response=%s"}' %(output_str)
            logging.debug("add_device_config_mapping:"+ output)
            HttpResponse(output)
        try:
            kwargs = {}
            kwargs2 = {}
            if((data.get('UserId') is None) or ((data.get('UserId') is not  None) and (len(data['UserId']) <= 0))):
                output_str += ",UserId is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("add_device_config_mapping:"+ output)
                return HttpResponse(output)
            else:
                userid    = data['UserId']
                
                get_user = JP_Company_Users.objects.get(CUId=userid,StatusActive=True)
                print(get_user)
                #kwargs['CUId'] = get_user

            if((data.get('DeviceId') is None) or ((data.get('DeviceId') is not  None) and (len(data['DeviceId']) <= 0))):
                output_str += ",DeviceId is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("add_device_config_mapping:"+ output)
                return HttpResponse(output)
            else:
                deviceid    = data['DeviceId']
                
                get_device = JP_Devices.objects.get(DeviceId=deviceid,StatusActive=True)
                print(get_device)
                kwargs['DeviceId'] = get_device
                print('macid : ',get_device.DeviceMac)    

            if((data.get('ConfigId') is None) or ((data.get('ConfigId') is not  None) and (len(data['ConfigId']) <= 0))):
                output_str += ",ConfigId is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("add_device_config_mapping:"+ output)
                return HttpResponse(output)
            else:
                configid    = data['ConfigId']
                
                get_configid = JP_Device_Config.objects.get(ConfigId=configid,StatusActive=True)
                print(get_configid)
                kwargs['ConfigId'] = get_configid
                get_config_details = JPD_Config_Details.objects.filter(ConfigId=configid,StatusActive=True)
                print(get_config_details)
                print(get_config_details[0].Frequency)
                d1=get_config_details[0].Frequency
                print((d1.hour * 60 + d1.minute) * 60 + d1.second)
                mill=((d1.hour * 60 + d1.minute) * 60 + d1.second)* 1000
                print('mill : ',mill)
                print(get_config_details[0].GpioPins)
                print(get_config_details[0].CTid.CTdesc)
                #{"IC":["RA-36","D-2000"]}

                send_str='{"IC":["RA-%s","D-%s"]}' %(get_config_details[0].GpioPins,mill)
                print(send_str,'',get_device.DeviceMac)
                
            check_dconfig_details = JP_Device_Config_Mapping.objects.filter(**kwargs)
            print(check_dconfig_details)
            if len(check_dconfig_details) > 0:
                msg =  base64.b64encode(send_str.encode('utf-8'))
                publish.single('jts/jpipe/v000001/Dev/'+str(get_device.DeviceMac), 'eyJjbGVhckFsbElDIjoiMSJ9', hostname='cld003.jts-prod.in', auth={'username': 'esp', 'password': 'ptlesp01'})
                publish.single('jts/jpipe/v000001/Dev/'+str(get_device.DeviceMac), msg, hostname='cld003.jts-prod.in', auth={'username': 'esp', 'password': 'ptlesp01'})
                #print('single classs : ',req)
                #req=config_publish(get_device.DeviceMac,send_str)
                #print(req)
               
                output = '{"error_code":"429","error_desc":"Response= config details  already associated"}'
                logging.debug("add_device_config_mapping:"+ output)
                return HttpResponse(output)
               
            else:
                add_config_rec=JP_Device_Config_Mapping(**kwargs);
                add_config_rec.save()
                print(add_config_rec.CMId)
                if(len(str(add_config_rec.CMId)) > 0):
                    msg =  base64.b64encode(send_str.encode('utf-8'))
                    publish.single('jts/jpipe/v000001/Dev/'+str(get_device.DeviceMac), 'eyJjbGVhckFsbElDIjoiMSJ9', hostname='cld003.jts-prod.in', auth={'username': 'esp', 'password': 'ptlesp01'})
                    publish.single('jts/jpipe/v000001/Dev/'+str(get_device.DeviceMac), msg, hostname='cld003.jts-prod.in', auth={'username': 'esp', 'password': 'ptlesp01'})
                    output = '{"error_code":"200","Response":"Successfully added the config details"}' 
                    logging.debug("add_device_config_mapping:"+ output)
                    return HttpResponse(output)
                    
                else:
                    output = '{"error_code":"409","error_desc":"Response=Failed to add the config"}'
                    logging.debug("add_device_config_mapping:"+ output)
                    return HttpResponse(output)
        except Exception as e:
            err_desc = 'add_device_config_mapping:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
            logging.debug("add_device_config_mapping:"+ err_desc)
            output = '{"error_code":"500","error_desc":"Response=Failed to add the config details"}'
            logging.debug("add_device_config_mapping:"+ output)
            return HttpResponse(output)
    
    else:
        logging.debug("add_device_config_mapping: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output = '{"error_code":"405","error_desc":"Response=GET is not supported"}'
        logging.debug("add_device_config_mapping:"+ output)
        return HttpResponse(output)

##################### add device #############################
def add_adapter(request): 
    if(request.method == "POST"):
        logging.debug("add_adapter: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output_str = "add_adapter- Unable to Authenticate/add_adapter... "
        logging.debug("add_adapter:input- "+str(request.body))
        try:
            data = json.loads(request.body)
            print (request.body)
        except ValueError as e:
            output_str += ",invalid input, no proper JSON request "
            output = '{"error_code":"400","error_desc":"Response=%s"}' %(output_str)
            logging.debug("add_adapter:"+ output)
            HttpResponse(output)
        try:
            kwargs = {}
            if((data.get('UserId') is None) or ((data.get('UserId') is not  None) and (len(data['UserId']) <= 0))):
                output_str += ",UserId is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("add_adapter:"+ output)
                return HttpResponse(output)
            else:
                userid    = data['UserId']
                get_user = JP_Company_Users.objects.get(CUId=userid,StatusActive=True)
                print(get_user)
                if len(str(get_user)) > 0:
                    print('inside if')
                    kwargs['CUId'] = get_user


            if((data.get('AdapterName') is None) or ((data.get('AdapterName') is not  None) and (len(data['AdapterName']) <= 0))):
                output_str += ",AdapterName is mandatory"
                output = '{"error_code":"411","error_desc":"Response=%s"}' %output_str
                logging.debug("add_adapter:"+ output)
                return HttpResponse(output)
            else:
                adapterName    = data['AdapterName']
                kwargs['AdapterName'] = adapterName

            if((data.get('AdapterMac') is not  None) and (len(data['AdapterMac']) > 0)):
                adapterMac = data['AdapterMac']     
                kwargs['AdapterMac'] = adapterMac
            
            logging.debug("add_adapter:input: company="+adapterName)
            
            check_device = JP_Adapter.objects.filter(AdapterName=adapterName)
            print(check_device)
            if len(check_device) > 0:
                output = '{"error_code":"429","error_desc":"Response=device already associated"}' 
                logging.debug("add_adapter:"+ output)
                return HttpResponse(output)
            else:
                add_comp_rec=JP_Adapter(**kwargs);
                add_comp_rec.save()
                print(add_comp_rec.AdapterName)
                if(len(str(add_comp_rec.AdapterName)) > 0):
                    output = '{"error_code":"200","Response":"Successfully added the apater, %s"}' %(adapterName)
                    logging.debug("add_adapter:"+ output)
                    return HttpResponse(output)
                else:
                    output = '{"error_code":"409","error_desc":"Response=Failed to add the adapter"}'
                    logging.debug("add_adapter:"+ output)
                    return HttpResponse(output)
        except Exception as e:
            err_desc = 'add_adapter:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
            logging.debug("add_adapter:"+ err_desc)
            output = '{"error_code":"500","error_desc":"Response=Failed to add the adapter"}'
            logging.debug("add_adapter:"+ output)
            return HttpResponse(output)
    
    else:
        logging.debug("add_adapter: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
        output = '{"error_code":"405","error_desc":"Response=GET is not supported"}'
        logging.debug("add_adapter:"+ output)
        return HttpResponse(output)





