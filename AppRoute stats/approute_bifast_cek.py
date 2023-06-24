"""
import all the reqiured librariers
"""
import requests
import json
from itertools import zip_longest
import difflib
import sys
import os
import time
import logging
import re
from tabulate import tabulate
import yaml
import json
from smtplib import SMTP
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pretty_html_table import build_table
from datetime import datetime, timedelta
import urllib.parse
from IPython.display import display
import matplotlib.pyplot as plt
import numpy as np



from auth_header import Authentication as auth
from operations import Operation 





def url(vmanage_host,vmanage_port,api):
    """ return the URL for the privide API ENDpoint """
    """ function to get the url provide api endpoint """
    
    return f"https://{vmanage_host}:{vmanage_port}{api}"



def post_events(header, data):
    """ return the sla events """
    """  function to get the SLA events from the vmanage """
   

    api_events = '/dataservice/statistics/approute'
    url_events = url(vmanage_host,vmanage_port,api_events)
    events = Operation.post_method(url_events, header, data)

    return events['data']

def send_email(sender_email, mail_passwd, receiver_email, body):
    
    """ return if email is sent successful or not"""
    """ function to sent email """

    
    message = MIMEMultipart()
    message['Subject'] = "SLA EVENTS"

    body_content = body
    message.attach(MIMEText(body_content, "html"))
    msg_body = message.as_string()

    server = SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, mail_passwd)
    try:
        server.sendmail(sender_email, receiver_email, msg_body)
        return ('email sent')
    except:
        return ('error sending mail')

    server.quit()




if __name__=='__main__':

    while True:

        """ open the yaml file where the constant data is stored"""

        with open("approute.yaml") as f:
            config = yaml.safe_load(f.read())
        
        
        """ extracting info from Yaml file"""

        vmanage_host = config['vmanage_host']
        vmanage_port = config['vmanage_port']
        username = config['vmanage_username']
        password = config['vmanage_password']

        time_delta = config['time_delta']
        
        print("local_system_ip = ")
        local_system_ip = input()
        """print("color = ")
        color = input()"""
        
        color = "private2"

        """ get current time and data and use time_delta to subract the time by delta minutes """
        """ format waktu YYYY-MM-DDTHH:MM:SS UTC """
        """date_time = datetime.utcnow()
        end_time = date_time.strftime("%Y-%m-%dT%H:%M:%S UTC")
        delta = date_time - timedelta( minutes = time_delta)
        start_time = delta.strftime("%Y-%m-%dT%H:%M:%S UTC")"""
        start_time = "2023-06-22T23:00:00 UTC"
        end_time = "2023-06-23T07:00:00 UTC"
        """print(start_time)
        print(end_time)"""


        """ Creted dataset"""
        approute_dataset_loss = {"time":[],"local_Device_Name":[],"remote_Device_IP":[],"color":[],"loss":[],}
        approute_dataset_lat = {"time":[],"local_Device_Name":[],"remote_Device_IP":[],"color":[],"latency":[],"jitter":[]}
        

    
        """  Calling the header function from Auth to get 
                'Content-Type': "application/json", 
                'Accept': '*/*', 'Cookie': session_id, 
                'X-XSRF-TOKEN': token_id}  """
        
        header = auth.get_header(vmanage_host, vmanage_port,username, password)



        """ Creating the request payload 
            since nested dict is not execpt in requests we used a str """
        
        
        
        """ Caling the API ('/dataservice/statistics/approute') call with POST request """
        
        
        
        """ parsing the returned data """
        edge = ['172.16.14.126','172.16.15.126','172.16.14.253','172.16.15.253']
        name_edge = ['DC1EXTEDG-1','DC1EXTEDG-2','DRCEXTEDG-1','DRCEXTEDG-2']
        warna = ['r','g','b','m']
        i = 0
        plt.figure()
        plt.xlabel("Time")
        plt.ylabel("Loss (%) ")
        losstest = "no"
        for remote_system_ip in edge: 
            data= '{\"query\":{\"condition\":\"AND\",\"rules\":[{\"value\":[\"'+start_time+'\",\"'+end_time+'\"],\"field\":\"entry_time\",\"type\":\"date\",\"operator\":\"between\"},{\"value\":[\"'+local_system_ip+'\"],\"field\":\"local_system_ip\",\"type\":\"string\",\"operator\":\"in\"},{\"value\":[\"'+remote_system_ip+'\"],\"field\":\"remote_system_ip\",\"type\":\"string\",\"operator\":\"in\"},{\"value\":[\"'+color+'\"],\"field\":\"local_color\",\"type\":\"string\",\"operator\":\"in\"}]}}'
            stats_data = post_events(header, data)
            approute_dataset_loss = {"time":[],"local_Device_Name":[],"remote_Device_IP":[],"color":[],"loss":[],}
            for approute_data in stats_data:
                """print(sla_event_data)"""
                """approute_details = re.split('\=|;',stats_data['details'])"""                
                approute_dataset_loss["time"].append(time.strftime('%H:%M', time.localtime(approute_data['entry_time']//1000)))
                approute_dataset_loss["local_Device_Name"].append(approute_data['host_name'])
                approute_dataset_loss["remote_Device_IP"].append(approute_data['remote_system_ip'])
                approute_dataset_loss["color"].append(approute_data['local_color'])
                approute_dataset_loss["loss"].append(approute_data['loss_percentage'])
                approute_dataframe = pd.DataFrame(approute_dataset_loss)
                approute_dataframe_reverse = approute_dataframe[::-1]
                if approute_data['loss_percentage'] > 5:
                    losstest = "yes"
                """display(approute_dataframe_reverse)"""
            """display(approute_dataframe_reverse)"""
            plt.plot(approute_dataframe_reverse["time"],approute_dataframe_reverse["loss"],warna[i])
            i=i+1
            """ Converting Dataset to Dataframe using pandas"""
        print(losstest)
        plt.legend(name_edge)
        plt.title(approute_dataset_loss["local_Device_Name"][0]+" Loss")
        plt.xticks(rotation=60)
        plt.xticks(np.arange(0, len(approute_dataset_loss["time"]), 60))
        
        i = 0
        plt.figure()
        plt.xlabel("Time")
        plt.ylabel("Latency (ms)")
        lattest = "no"
        for remote_system_ip in edge: 
            data= '{\"query\":{\"condition\":\"AND\",\"rules\":[{\"value\":[\"'+start_time+'\",\"'+end_time+'\"],\"field\":\"entry_time\",\"type\":\"date\",\"operator\":\"between\"},{\"value\":[\"'+local_system_ip+'\"],\"field\":\"local_system_ip\",\"type\":\"string\",\"operator\":\"in\"},{\"value\":[\"'+remote_system_ip+'\"],\"field\":\"remote_system_ip\",\"type\":\"string\",\"operator\":\"in\"},{\"value\":[\"'+color+'\"],\"field\":\"local_color\",\"type\":\"string\",\"operator\":\"in\"}]}}'
            stats_data = post_events(header, data)
            approute_dataset_lat = {"time":[],"local_Device_Name":[],"remote_Device_IP":[],"color":[],"latency":[]}
            for approute_data in stats_data:
                """print(sla_event_data)"""
                """approute_details = re.split('\=|;',stats_data['details'])"""                
                approute_dataset_lat["time"].append(time.strftime('%H:%M', time.localtime(approute_data['entry_time']//1000)))
                approute_dataset_lat["local_Device_Name"].append(approute_data['host_name'])
                approute_dataset_lat["remote_Device_IP"].append(approute_data['remote_system_ip'])
                approute_dataset_lat["color"].append(approute_data['local_color'])
                approute_dataset_lat["latency"].append(approute_data['latency'])
                approute_dataframe = pd.DataFrame(approute_dataset_lat)
                approute_dataframe_reverse = approute_dataframe[::-1]
                if approute_data['latency'] > 25:
                    lattest = "yes"                                      
                """display(approute_dataframe_reverse)"""
            """display(approute_dataframe_reverse)"""
            plt.plot(approute_dataframe_reverse["time"],approute_dataframe_reverse["latency"],warna[i])
            i=i+1
            """ Converting Dataset to Dataframe using pandas"""
        print(lattest)
        plt.legend(name_edge)
        plt.title(approute_dataset_lat["local_Device_Name"][0]+" Latency")
        plt.xticks(rotation=60)
        plt.xticks(np.arange(0, len(approute_dataset_lat["time"]), 60))
        
        i = 0
        plt.figure()
        plt.xlabel("Time")
        plt.ylabel("Jitter (ms)")
        for remote_system_ip in edge: 
            data= '{\"query\":{\"condition\":\"AND\",\"rules\":[{\"value\":[\"'+start_time+'\",\"'+end_time+'\"],\"field\":\"entry_time\",\"type\":\"date\",\"operator\":\"between\"},{\"value\":[\"'+local_system_ip+'\"],\"field\":\"local_system_ip\",\"type\":\"string\",\"operator\":\"in\"},{\"value\":[\"'+remote_system_ip+'\"],\"field\":\"remote_system_ip\",\"type\":\"string\",\"operator\":\"in\"},{\"value\":[\"'+color+'\"],\"field\":\"local_color\",\"type\":\"string\",\"operator\":\"in\"}]}}'
            stats_data = post_events(header, data)
            approute_dataset_lat = {"time":[],"local_Device_Name":[],"remote_Device_IP":[],"color":[],"Jitter":[]}
            for approute_data in stats_data:
                """print(sla_event_data)"""
                """approute_details = re.split('\=|;',stats_data['details'])"""                
                approute_dataset_lat["time"].append(time.strftime('%H:%M', time.localtime(approute_data['entry_time']//1000)))
                approute_dataset_lat["local_Device_Name"].append(approute_data['host_name'])
                approute_dataset_lat["remote_Device_IP"].append(approute_data['remote_system_ip'])
                approute_dataset_lat["color"].append(approute_data['local_color'])
                approute_dataset_lat["Jitter"].append(approute_data['jitter'])
                approute_dataframe = pd.DataFrame(approute_dataset_lat)
                approute_dataframe_reverse = approute_dataframe[::-1]
                                                      
                """display(approute_dataframe_reverse)"""
            """display(approute_dataframe_reverse)"""
            plt.plot(approute_dataframe_reverse["time"],approute_dataframe_reverse["Jitter"],warna[i])
            i=i+1
            """ Converting Dataset to Dataframe using pandas"""
        plt.legend(name_edge)
        plt.title(approute_dataset_lat["local_Device_Name"][0]+" Jitter")
        plt.xticks(rotation=60)
        plt.xticks(np.arange(0, len(approute_dataset_lat["time"]), 60))
                
        plt.show()
                                    
        """approute_dataframe.plot(x ='time', y='loss', kind='line')
        approute_dataframe.plot(x ='time', y='latency', kind='line')
        approute_dataframe.plot(x ='time', y='jitter', kind='line')"""
    time.sleep(900)
