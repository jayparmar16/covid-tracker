# IMPORTS
import bs4
import requests
import pandas as pd
from twilio.rest import Client
import datetime
from datetime import date
from csv import writer

today = date.today()
d1 = today.strftime("%d/%m/%Y")

#REQUESTS and BS4
res = requests.get("https://gujcovid19.gujarat.gov.in/") #Using local website
res.raise_for_status()
covidSoup = bs4.BeautifulSoup(res.text,'html.parser')

#NECESSARY DECLAREMENTS
ac = []
tc = []
pr = []
uq = []
td = []
date = []
row_contents = []
date.append(d1)
row_contents.append(d1)

#MINING 
activeCases = covidSoup.select('#ctl00_body_h3TotalActiveConfirmedCount')
ac.append(activeCases[0].getText())
row_contents.append(activeCases[0].getText())

totalCases = covidSoup.select('#ctl00_body_h3PatientTestedCount')
tc.append(totalCases[0].getText())
row_contents.append(totalCases[0].getText())

patientsRec = covidSoup.select('#ctl00_body_h3PatientCuredCount')
pr.append(patientsRec[0].getText())
row_contents.append(patientsRec[0].getText())

underQuar = covidSoup.select("#ctl00_body_h3PeopleQuarantineCount")
uq.append(underQuar[0].getText())
row_contents.append(underQuar[0].getText())

totalDeaths = covidSoup.select('#ctl00_body_h3TotalDath')
td.append(totalDeaths[0].getText())
row_contents.append(totalDeaths[0].getText())

#Function to append new values to the csv file
def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open('final.csv', 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)


#DICTIONARY WITH ALL VALUES
results = {"Date":date,"Active Cases":ac,"Total Cases":tc,"Patients Recovered":pr,"People under Quarantine":uq,"Total Deaths":td}
df = pd.DataFrame(results)
idx = (df.index[df['Date'] == d1].tolist())
row_contents.insert(0,idx[0]+1)
append_list_as_row('final.csv', row_contents) #Appending new row with new cases

# Statistics- Finding increase or decrease based on previous day
df2 = pd.read_csv('final.csv')
pac=[]
ptc=[]
ppr=[]
ptd=[]
l = len(df2)
for i in range(1,3):
    pac.append(df2["Active Cases"].values[-i])
    ptc.append(df2["Total Cases"].values[-i])
    ppr.append(df2["Patients Recovered"].values[-i])
    ptd.append(df2["Total Deaths"].values[-i])


def incrordecr(x,y):
    d = x - y
    flag = False
    if d < 0:
        d= -d
        flag = True
    return flag,d

# Main message string to be passed to whatsapp
m = "Active Cases : "+ activeCases[0].getText() + " Total Cases : " + totalCases[0].getText() + " Patients Recoverd : " + patientsRec[0].getText() + " Patients under quarantine : " + underQuar[0].getText() + " Total Deaths : " + totalDeaths[0].getText() + "\n"

t = incrordecr(pac[0],pac[1])
if t[0] == True:
    m += "There is a decrease in Active Cases by " + str(t[1]) + "\n"
else:
    m += "There is an increase in Active Cases by " + str(t[1]) + "\n"
t1 = incrordecr(ptc[0],ptc[1])
if t1[0] == True:
    m += "There is a decrease in Total Cases by " + str(t1[1])  + "\n"
else:
    m += "There is an increase in Total Cases by " + str(t1[1])  + "\n"
t2 = incrordecr(ppr[0],ppr[1])
if t2[0] == True:
    m += "There is a decrease in Patients recovery by " + str(t2[1])  + "\n"
else:
    m += "Theere is an increase in Patients recovery by " + str(t2[1])  + "\n"
t3 = incrordecr(ptd[0],ptd[1])
if t3[0] == True:
    m += "There is a decrease in Total Deaths by " + str(t3[1])  + "\n"
else:
    m += "Theere is an increase in Total Deaths by " + str(t3[1])  + "\n"


#print(m)

#Function to send whatsapp message using Twilio

def send_whatsapp_message(msg):
    account_sid = 'AC2837e41794e450ef88925f85a46a6508'
    auth_token = '051928be54ee7522d8f98707f40e1525'
    Client(account_sid, auth_token).messages.create(
        from_='whatsapp:+14155238886',
        to='whatsapp:+916353991474',
        body=msg
    )

send_whatsapp_message(m)
