import requests
from lxml import etree
import json
from io import StringIO
from datetime import datetime
from bs4 import BeautifulSoup
import re
import ftfy
re.compile('<title>(.*)</title>')

#URL:http://cms.nic.in/ncdrcusersWeb/login.do?method=caseStatus
#case:CC/123/2017
def ncdrccasestatus(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "0/0/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"0"),
     ("distCode",	"0"),
    ]
    r = requests.post(url=url, params = params)
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(r.text), parser)

    #complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="rpttxthval"]/text()')[0]
        complainant.append(re.sub(r'[^\x00-\x7F]+', ' ', complainant1.strip()))
    except: pass

    #respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="rpttxthval"]/text()')[1]
        respondent.append(re.sub(r'[^\x00-\x7F]+', ' ', respondent1.strip()))
    except: pass

    #date of hearing
    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        hearing = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(1, len(hearing), 2):
            if hearing[i] != " ":
                date = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                hearing1 = date.strip()
                if hearing1 != "":
                    dateOfnextHearing.append(hearing1)

    except:
        pass


    #Case Stage
    casestage = []
    try:
        case = tree.xpath('//*[@class="rpttxthval"]/text()')
        for i in range(2, len(case)):
            if case[i] != " ":
                case1 = tree.xpath('//*[@class="rpttxthval"]/text()')[i]
                case2 = case1.strip()
                if case2 != "":
                    casestage.append(case2)
    except:
        pass


    #datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except: pass

    #Proceedings
    proceedings = []
    try:
        for i in range(0, len(datereversed1)):
            url2 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetProceedings"
            payload = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings'}
            r2 = requests.post(url=url2, params=payload)
            a = BeautifulSoup(r2.text, "lxml").text
            proceedings.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ')))


    except: pass


    #orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings', 'orderflag':	'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ', a1.replace('\n', ' ').replace('\r', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))


    except: pass


    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Date Of Hearing'] = dateOfHearing
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Court Proceedings'] = proceedings
        ret_this['Orders'] = orders
    except: pass


    result = json.dumps({"Case Status" : ret_this})
    print (ftfy.fix_text_encoding(result))


def delhistatecommision(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/0/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"8"),
     ("distCode",	"0"),
    ]
    r = requests.post(url=url, params = params)
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="rpttxthval"]/text()')[0]
        complainant.append(re.sub(r'[^\x00-\x7F]+', ' ', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="rpttxthval"]/text()')[1]
        respondent.append(re.sub(r'[^\x00-\x7F]+', ' ', respondent1.strip()))
    except:
        pass

    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        hearing = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(1, len(hearing), 2):
            if hearing[i] != " ":
                date = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                hearing1 = date.strip()
                if hearing1 != "":
                    dateOfnextHearing.append(hearing1)

    except:
        pass

    # Case Stage
    casestage = []
    try:
        case = tree.xpath('//*[@class="rpttxthval"]/text()')
        for i in range(2, len(case)):
            if case[i] != " ":
                case1 = tree.xpath('//*[@class="rpttxthval"]/text()')[i]
                case2 = case1.strip()
                if case2 != "":
                    casestage.append(case2)
    except:
        pass

    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except:
        pass

    # Proceedings
    proceedings = []
    try:
        for i in range(0, len(datereversed1)):
            url2 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetProceedings"
            payload = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings'}
            r2 = requests.post(url=url2, params=payload)
            a = BeautifulSoup(r2.text, "lxml").text
            proceedings.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ')))


    except:
        pass

    # orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings',
                        'orderflag': 'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ', a1.replace('\n', ' ').replace('\r', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Date Of Hearing'] = dateOfHearing
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Court Proceedings'] = proceedings
        ret_this['Orders'] = orders
    except:
        pass

    result = json.dumps({"Case Status": ret_this})
    print(ftfy.fix_text_encoding(result))


def districteastdelhi(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/5/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"8"),
     ("distCode",	"5"),
    ]
    r = requests.post(url=url, params = params)
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="rpttxthval"]/text()')[0]
        complainant.append(re.sub(r'[^\x00-\x7F]+', ' ', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="rpttxthval"]/text()')[1]
        respondent.append(re.sub(r'[^\x00-\x7F]+', ' ', respondent1.strip()))
    except:
        pass

    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        hearing = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(1, len(hearing), 2):
            if hearing[i] != " ":
                date = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                hearing1 = date.strip()
                if hearing1 != "":
                    dateOfnextHearing.append(hearing1)

    except:
        pass

    # Case Stage
    casestage = []
    try:
        case = tree.xpath('//*[@class="rpttxthval"]/text()')
        for i in range(2, len(case)):
            if case[i] != " ":
                case1 = tree.xpath('//*[@class="rpttxthval"]/text()')[i]
                case2 = case1.strip()
                if case2 != "":
                    casestage.append(case2)
    except:
        pass

    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except:
        pass

    # Proceedings
    proceedings = []
    try:
        for i in range(0, len(datereversed1)):
            url2 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetProceedings"
            payload = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings'}
            r2 = requests.post(url=url2, params=payload)
            a = BeautifulSoup(r2.text, "lxml").text
            proceedings.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ')))


    except:
        pass

    # orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings',
                        'orderflag': 'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ', a1.replace('\n', ' ').replace('\r', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Date Of Hearing'] = dateOfHearing
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Court Proceedings'] = proceedings
        ret_this['Orders'] = orders
    except:
        pass

    result = json.dumps({"Case Status": ret_this})
    print(ftfy.fix_text_encoding(result))

def districtsouthdelhi(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/6/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"8"),
     ("distCode",	"6"),
    ]
    r = requests.post(url=url, params = params)
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="rpttxthval"]/text()')[0]
        complainant.append(re.sub(r'[^\x00-\x7F]+', ' ', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="rpttxthval"]/text()')[1]
        respondent.append(re.sub(r'[^\x00-\x7F]+', ' ', respondent1.strip()))
    except:
        pass

    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        hearing = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(1, len(hearing), 2):
            if hearing[i] != " ":
                date = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                hearing1 = date.strip()
                if hearing1 != "":
                    dateOfnextHearing.append(hearing1)

    except:
        pass

    # Case Stage
    casestage = []
    try:
        case = tree.xpath('//*[@class="rpttxthval"]/text()')
        for i in range(2, len(case)):
            if case[i] != " ":
                case1 = tree.xpath('//*[@class="rpttxthval"]/text()')[i]
                case2 = case1.strip()
                if case2 != "":
                    casestage.append(case2)
    except:
        pass

    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except:
        pass

    # Proceedings
    proceedings = []
    try:
        for i in range(0, len(datereversed1)):
            url2 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetProceedings"
            payload = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings'}
            r2 = requests.post(url=url2, params=payload)
            a = BeautifulSoup(r2.text, "lxml").text
            proceedings.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ')))


    except:
        pass

    # orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings',
                        'orderflag': 'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ', a1.replace('\n', ' ').replace('\r', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Date Of Hearing'] = dateOfHearing
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Court Proceedings'] = proceedings
        ret_this['Orders'] = orders
    except:
        pass

    result = json.dumps({"Case Status": ret_this})
    print(ftfy.fix_text_encoding(result))

def districtwestdelhi(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/4/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"8"),
     ("distCode",	"4"),
    ]
    r = requests.post(url=url, params = params)
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="rpttxthval"]/text()')[0]
        complainant.append(re.sub(r'[^\x00-\x7F]+', ' ', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="rpttxthval"]/text()')[1]
        respondent.append(re.sub(r'[^\x00-\x7F]+', ' ', respondent1.strip()))
    except:
        pass

    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        hearing = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(1, len(hearing), 2):
            if hearing[i] != " ":
                date = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                hearing1 = date.strip()
                if hearing1 != "":
                    dateOfnextHearing.append(hearing1)

    except:
        pass

    # Case Stage
    casestage = []
    try:
        case = tree.xpath('//*[@class="rpttxthval"]/text()')
        for i in range(2, len(case)):
            if case[i] != " ":
                case1 = tree.xpath('//*[@class="rpttxthval"]/text()')[i]
                case2 = case1.strip()
                if case2 != "":
                    casestage.append(case2)
    except:
        pass

    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except:
        pass

    # Proceedings
    proceedings = []
    try:
        for i in range(0, len(datereversed1)):
            url2 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetProceedings"
            payload = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings'}
            r2 = requests.post(url=url2, params=payload)
            a = BeautifulSoup(r2.text, "lxml").text
            proceedings.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ')))


    except:
        pass

    # orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings',
                        'orderflag': 'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ', a1.replace('\n', ' ').replace('\r', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Date Of Hearing'] = dateOfHearing
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Court Proceedings'] = proceedings
        ret_this['Orders'] = orders
    except:
        pass

    result = json.dumps({"Case Status": ret_this})
    print(ftfy.fix_text_encoding(result))


def districtcentraldelhi(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/3/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"8"),
     ("distCode",	"3"),
    ]
    r = requests.post(url=url, params = params)
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="rpttxthval"]/text()')[0]
        complainant.append(re.sub(r'[^\x00-\x7F]+', ' ', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="rpttxthval"]/text()')[1]
        respondent.append(re.sub(r'[^\x00-\x7F]+', ' ', respondent1.strip()))
    except:
        pass

    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        hearing = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(1, len(hearing), 2):
            if hearing[i] != " ":
                date = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                hearing1 = date.strip()
                if hearing1 != "":
                    dateOfnextHearing.append(hearing1)

    except:
        pass

    # Case Stage
    casestage = []
    try:
        case = tree.xpath('//*[@class="rpttxthval"]/text()')
        for i in range(2, len(case)):
            if case[i] != " ":
                case1 = tree.xpath('//*[@class="rpttxthval"]/text()')[i]
                case2 = case1.strip()
                if case2 != "":
                    casestage.append(case2)
    except:
        pass

    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except:
        pass

    # Proceedings
    proceedings = []
    try:
        for i in range(0, len(datereversed1)):
            url2 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetProceedings"
            payload = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings'}
            r2 = requests.post(url=url2, params=payload)
            a = BeautifulSoup(r2.text, "lxml").text
            proceedings.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ')))


    except:
        pass

    # orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings',
                        'orderflag': 'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ', a1.replace('\n', ' ').replace('\r', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Date Of Hearing'] = dateOfHearing
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Court Proceedings'] = proceedings
        ret_this['Orders'] = orders
    except:
        pass

    result = json.dumps({"Case Status": ret_this})
    print(ftfy.fix_text_encoding(result))

def districtnewdelhi(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/12/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"8"),
     ("distCode",	"12"),
    ]
    r = requests.post(url=url, params = params)
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="rpttxthval"]/text()')[0]
        complainant.append(re.sub(r'[^\x00-\x7F]+', ' ', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="rpttxthval"]/text()')[1]
        respondent.append(re.sub(r'[^\x00-\x7F]+', ' ', respondent1.strip()))
    except:
        pass

    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        hearing = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(1, len(hearing), 2):
            if hearing[i] != " ":
                date = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                hearing1 = date.strip()
                if hearing1 != "":
                    dateOfnextHearing.append(hearing1)

    except:
        pass

    # Case Stage
    casestage = []
    try:
        case = tree.xpath('//*[@class="rpttxthval"]/text()')
        for i in range(2, len(case)):
            if case[i] != " ":
                case1 = tree.xpath('//*[@class="rpttxthval"]/text()')[i]
                case2 = case1.strip()
                if case2 != "":
                    casestage.append(case2)
    except:
        pass

    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except:
        pass

    # Proceedings
    proceedings = []
    try:
        for i in range(0, len(datereversed1)):
            url2 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetProceedings"
            payload = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings'}
            r2 = requests.post(url=url2, params=payload)
            a = BeautifulSoup(r2.text, "lxml").text
            proceedings.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ')))


    except:
        pass

    # orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings',
                        'orderflag': 'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ', a1.replace('\n', ' ').replace('\r', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Date Of Hearing'] = dateOfHearing
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Court Proceedings'] = proceedings
        ret_this['Orders'] = orders
    except:
        pass

    result = json.dumps({"Case Status": ret_this})
    print(ftfy.fix_text_encoding(result))

def districtnortheastdelhi(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/10/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"8"),
     ("distCode",	"10"),
    ]
    r = requests.post(url=url, params = params)
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="rpttxthval"]/text()')[0]
        complainant.append(re.sub(r'[^\x00-\x7F]+', ' ', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="rpttxthval"]/text()')[1]
        respondent.append(re.sub(r'[^\x00-\x7F]+', ' ', respondent1.strip()))
    except:
        pass

    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        hearing = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(1, len(hearing), 2):
            if hearing[i] != " ":
                date = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                hearing1 = date.strip()
                if hearing1 != "":
                    dateOfnextHearing.append(hearing1)

    except:
        pass

    # Case Stage
    casestage = []
    try:
        case = tree.xpath('//*[@class="rpttxthval"]/text()')
        for i in range(2, len(case)):
            if case[i] != " ":
                case1 = tree.xpath('//*[@class="rpttxthval"]/text()')[i]
                case2 = case1.strip()
                if case2 != "":
                    casestage.append(case2)
    except:
        pass

    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except:
        pass

    # Proceedings
    proceedings = []
    try:
        for i in range(0, len(datereversed1)):
            url2 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetProceedings"
            payload = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings'}
            r2 = requests.post(url=url2, params=payload)
            a = BeautifulSoup(r2.text, "lxml").text
            proceedings.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ')))


    except:
        pass

    # orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings',
                        'orderflag': 'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ', a1.replace('\n', ' ').replace('\r', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Date Of Hearing'] = dateOfHearing
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Court Proceedings'] = proceedings
        ret_this['Orders'] = orders
    except:
        pass

    result = json.dumps({"Case Status": ret_this})
    print(ftfy.fix_text_encoding(result))

def districtnorthwestdelhi(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/7/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"8"),
     ("distCode",	"7"),
    ]
    r = requests.post(url=url, params = params)
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="rpttxthval"]/text()')[0]
        complainant.append(re.sub(r'[^\x00-\x7F]+', ' ', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="rpttxthval"]/text()')[1]
        respondent.append(re.sub(r'[^\x00-\x7F]+', ' ', respondent1.strip()))
    except:
        pass

    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        hearing = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(1, len(hearing), 2):
            if hearing[i] != " ":
                date = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                hearing1 = date.strip()
                if hearing1 != "":
                    dateOfnextHearing.append(hearing1)

    except:
        pass

    # Case Stage
    casestage = []
    try:
        case = tree.xpath('//*[@class="rpttxthval"]/text()')
        for i in range(2, len(case)):
            if case[i] != " ":
                case1 = tree.xpath('//*[@class="rpttxthval"]/text()')[i]
                case2 = case1.strip()
                if case2 != "":
                    casestage.append(case2)
    except:
        pass

    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except:
        pass

    # Proceedings
    proceedings = []
    try:
        for i in range(0, len(datereversed1)):
            url2 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetProceedings"
            payload = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings'}
            r2 = requests.post(url=url2, params=payload)
            a = BeautifulSoup(r2.text, "lxml").text
            proceedings.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ')))


    except:
        pass

    # orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings',
                        'orderflag': 'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ', a1.replace('\n', ' ').replace('\r', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Date Of Hearing'] = dateOfHearing
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Court Proceedings'] = proceedings
        ret_this['Orders'] = orders
    except:
        pass

    result = json.dumps({"Case Status": ret_this})
    print(ftfy.fix_text_encoding(result))

def districtsouth2(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/16/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"8"),
     ("distCode",	"16"),
    ]
    r = requests.post(url=url, params = params)
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="rpttxthval"]/text()')[0]
        complainant.append(re.sub(r'[^\x00-\x7F]+', ' ', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="rpttxthval"]/text()')[1]
        respondent.append(re.sub(r'[^\x00-\x7F]+', ' ', respondent1.strip()))
    except:
        pass

    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        hearing = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(1, len(hearing), 2):
            if hearing[i] != " ":
                date = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                hearing1 = date.strip()
                if hearing1 != "":
                    dateOfnextHearing.append(hearing1)

    except:
        pass

    # Case Stage
    casestage = []
    try:
        case = tree.xpath('//*[@class="rpttxthval"]/text()')
        for i in range(2, len(case)):
            if case[i] != " ":
                case1 = tree.xpath('//*[@class="rpttxthval"]/text()')[i]
                case2 = case1.strip()
                if case2 != "":
                    casestage.append(case2)
    except:
        pass

    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except:
        pass

    # Proceedings
    proceedings = []
    try:
        for i in range(0, len(datereversed1)):
            url2 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetProceedings"
            payload = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings'}
            r2 = requests.post(url=url2, params=payload)
            a = BeautifulSoup(r2.text, "lxml").text
            proceedings.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ')))


    except:
        pass

    # orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings',
                        'orderflag': 'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ', a1.replace('\n', ' ').replace('\r', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Date Of Hearing'] = dateOfHearing
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Court Proceedings'] = proceedings
        ret_this['Orders'] = orders
    except:
        pass

    result = json.dumps({"Case Status": ret_this})
    print(ftfy.fix_text_encoding(result))

def districtsouthwest(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/15/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"8"),
     ("distCode",	"15"),
    ]
    r = requests.post(url=url, params = params)
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="rpttxthval"]/text()')[0]
        complainant.append(re.sub(r'[^\x00-\x7F]+', ' ', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="rpttxthval"]/text()')[1]
        respondent.append(re.sub(r'[^\x00-\x7F]+', ' ', respondent1.strip()))
    except:
        pass

    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        hearing = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(1, len(hearing), 2):
            if hearing[i] != " ":
                date = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                hearing1 = date.strip()
                if hearing1 != "":
                    dateOfnextHearing.append(hearing1)

    except:
        pass

    # Case Stage
    casestage = []
    try:
        case = tree.xpath('//*[@class="rpttxthval"]/text()')
        for i in range(2, len(case)):
            if case[i] != " ":
                case1 = tree.xpath('//*[@class="rpttxthval"]/text()')[i]
                case2 = case1.strip()
                if case2 != "":
                    casestage.append(case2)
    except:
        pass

    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except:
        pass

    # Proceedings
    proceedings = []
    try:
        for i in range(0, len(datereversed1)):
            url2 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetProceedings"
            payload = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings'}
            r2 = requests.post(url=url2, params=payload)
            a = BeautifulSoup(r2.text, "lxml").text
            proceedings.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ')))


    except:
        pass

    # orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings',
                        'orderflag': 'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ', a1.replace('\n', ' ').replace('\r', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Date Of Hearing'] = dateOfHearing
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Court Proceedings'] = proceedings
        ret_this['Orders'] = orders
    except:
        pass

    result = json.dumps({"Case Status": ret_this})
    print(ftfy.fix_text_encoding(result))

def districtnorth(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/9/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"8"),
     ("distCode",	"9"),
    ]
    r = requests.post(url=url, params = params)
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="rpttxthval"]/text()')[0]
        complainant.append(re.sub(r'[^\x00-\x7F]+', ' ', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="rpttxthval"]/text()')[1]
        respondent.append(re.sub(r'[^\x00-\x7F]+', ' ', respondent1.strip()))
    except:
        pass

    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        hearing = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(1, len(hearing), 2):
            if hearing[i] != " ":
                date = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                hearing1 = date.strip()
                if hearing1 != "":
                    dateOfnextHearing.append(hearing1)

    except:
        pass

    # Case Stage
    casestage = []
    try:
        case = tree.xpath('//*[@class="rpttxthval"]/text()')
        for i in range(2, len(case)):
            if case[i] != " ":
                case1 = tree.xpath('//*[@class="rpttxthval"]/text()')[i]
                case2 = case1.strip()
                if case2 != "":
                    casestage.append(case2)
    except:
        pass

    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except:
        pass

    # Proceedings
    proceedings = []
    try:
        for i in range(0, len(datereversed1)):
            url2 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetProceedings"
            payload = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings'}
            r2 = requests.post(url=url2, params=payload)
            a = BeautifulSoup(r2.text, "lxml").text
            proceedings.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ')))


    except:
        pass

    # orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings',
                        'orderflag': 'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ', a1.replace('\n', ' ').replace('\r', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Date Of Hearing'] = dateOfHearing
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Court Proceedings'] = proceedings
        ret_this['Orders'] = orders
    except:
        pass

    result = json.dumps({"Case Status": ret_this})
    print(ftfy.fix_text_encoding(result))



