import requests
from lxml import etree
import json
from io import StringIO
from datetime import datetime
from bs4 import BeautifulSoup
import ftfy
import re
re.compile('<title>(.*)</title>')


#URL:http://cms.nic.in/ncdrcusersWeb/search.do?method=loadSearchPub
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

    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    #date of hearing used to pass the value to the judgment url(usually for last date of hearing)
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
    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)
    except:
        pass
    # lastdate for judgments
    lastdate=[]
    try:
        lastdate = datereversed1[len(datereversed1) - 1]
    except:
        pass
    # Judgements
    judgment = []
    try:
        url2 = "http://cms.nic.in/ncdrcusersWeb/GetJudgement.do"
        payload = {'method': 'GetJudgement', 'dtofhearing': lastdate, 'caseidin': caseidin}
        r2 = requests.post(url=url2, params=payload)
        a = BeautifulSoup(r2.text, "lxml").text
        judgment.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ').replace('&nbsp', ' ')))
    except:
        pass
    ret_this = {}
    try:
        ret_this['Final Judgment'] = judgment
    except:
        pass
    result = json.dumps({"Judgments": ret_this})
    print(ftfy.fix_text_encoding(result))


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
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)
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
    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)
    except:
        pass
    # lastdate for judgments
    lastdate=[]
    try:
        lastdate = datereversed1[len(datereversed1) - 1]
    except:
        pass
    # Judgements
    judgment = []
    try:
        url2 = "http://cms.nic.in/ncdrcusersWeb/GetJudgement.do"
        payload = {'method': 'GetJudgement', 'dtofhearing': lastdate, 'caseidin':caseidin}
        r2 = requests.post(url=url2, params=payload)
        a = BeautifulSoup(r2.text, "lxml").text
        judgment.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ').replace('&nbsp', ' ')))
    except:
        pass
    ret_this = {}
    try:
        ret_this['Final Judgment'] = judgment
    except:
        pass
    result = json.dumps({"Judgments": ret_this})
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
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)
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
    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)
    except:
        pass
    # lastdate for judgments
    lastdate=[]
    try:
        lastdate = datereversed1[len(datereversed1) - 1]
    except:
        pass
    # Judgements
    judgment = []
    try:
        url2 = "http://cms.nic.in/ncdrcusersWeb/GetJudgement.do"
        payload = {'method': 'GetJudgement', 'dtofhearing': lastdate, 'caseidin': caseidin}
        r2 = requests.post(url=url2, params=payload)
        a = BeautifulSoup(r2.text, "lxml").text
        judgment.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ').replace('&nbsp', ' ')))
    except:
        pass
    ret_this = {}
    try:
        ret_this['Final Judgment'] = judgment
    except:
        pass
    result = json.dumps({"Judgments": ret_this})
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
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)
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
    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)
    except:
        pass
    # lastdate for judgments
    lastdate=[]
    try:
        lastdate = datereversed1[len(datereversed1) - 1]
    except:
        pass
    # Judgements
    judgment = []
    try:
        url2 = "http://cms.nic.in/ncdrcusersWeb/GetJudgement.do"
        payload = {'method': 'GetJudgement', 'dtofhearing': lastdate, 'caseidin':caseidin}
        r2 = requests.post(url=url2, params=payload)
        a = BeautifulSoup(r2.text, "lxml").text
        judgment.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ').replace('&nbsp', ' ')))
    except:
        pass
    ret_this = {}
    try:
        ret_this['Final Judgment'] = judgment
    except:
        pass
    result = json.dumps({"Judgments": ret_this})
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
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)
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
    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)
    except:
        pass
    # lastdate for judgments
    lastdate=[]
    try:
        lastdate = datereversed1[len(datereversed1) - 1]
    except:
        pass
    # Judgements
    judgment = []
    try:
        url2 = "http://cms.nic.in/ncdrcusersWeb/GetJudgement.do"
        payload = {'method': 'GetJudgement', 'dtofhearing': lastdate, 'caseidin':caseidin}
        r2 = requests.post(url=url2, params=payload)
        a = BeautifulSoup(r2.text, "lxml").text
        judgment.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ').replace('&nbsp', ' ')))
    except:
        pass
    ret_this = {}
    try:
        ret_this['Final Judgment'] = judgment
    except:
        pass
    result = json.dumps({"Judgments": ret_this})
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
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)
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
    #datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)
    except:
        pass
    #lastdate for judgments
    lastdate=[]
    try:
        lastdate = datereversed1[len(datereversed1) - 1]
    except:
        pass
    #Judgements
    judgment = []
    try:
        url2 = "http://cms.nic.in/ncdrcusersWeb/GetJudgement.do"
        payload = {'method': 'GetJudgement', 'dtofhearing': lastdate, 'caseidin':caseidin}
        r2 = requests.post(url=url2, params=payload)
        a = BeautifulSoup(r2.text, "lxml").text
        judgment.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ').replace('&nbsp', ' ')))
    except:
        pass
    ret_this = {}
    try:
        ret_this['Final Judgment'] = judgment
    except:
        pass
    result = json.dumps({"Judgments": ret_this})
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
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)
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
    #datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)
    except:
        pass
    # lastdate for judgments
    lastdate=[]
    try:
        lastdate = datereversed1[len(datereversed1) - 1]
    except:
        pass
    # Judgements
    judgment = []
    try:
        url2 = "http://cms.nic.in/ncdrcusersWeb/GetJudgement.do"
        payload = {'method': 'GetJudgement', 'dtofhearing': lastdate, 'caseidin':caseidin}
        r2 = requests.post(url=url2, params=payload)
        a = BeautifulSoup(r2.text, "lxml").text
        judgment.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ').replace('&nbsp', ' ')))
    except:
        pass
    ret_this = {}
    try:
        ret_this['Final Judgment'] = judgment
    except:
        pass
    result = json.dumps({"Judgments": ret_this})
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
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)
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
    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)
    except:
        pass
    # lastdate for judgments
    lastdate=[]
    try:
        lastdate = datereversed1[len(datereversed1) - 1]
    except:
        pass
    # Judgements
    judgment = []
    try:
        url2 = "http://cms.nic.in/ncdrcusersWeb/GetJudgement.do"
        payload = {'method': 'GetJudgement', 'dtofhearing': lastdate, 'caseidin':caseidin}
        r2 = requests.post(url=url2, params=payload)
        a = BeautifulSoup(r2.text, "lxml").text
        judgment.append(re.sub(r'[^\x00-\x7F]+', ' ',a.replace('\n', ' ').replace('\r', ' ').replace('&nbsp', ' ')))
    except:
        pass
    ret_this = {}
    try:
        ret_this['Final Judgment'] = judgment
    except:
        pass
    result = json.dumps({"Judgments": ret_this})
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
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)
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
    #datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)
    except:
        pass
    # lastdate for judgments
    lastdate=[]
    try:
        lastdate = datereversed1[len(datereversed1) - 1]
    except:
        pass
    # Judgements
    judgment = []
    try:
        url2 = "http://cms.nic.in/ncdrcusersWeb/GetJudgement.do"
        payload = {'method': 'GetJudgement', 'dtofhearing': lastdate, 'caseidin':caseidin}
        r2 = requests.post(url=url2, params=payload)
        a = BeautifulSoup(r2.text, "lxml").text
        judgment.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ').replace('&nbsp', ' ')))
    except:
        pass
    ret_this = {}
    try:
        ret_this['Final Judgment'] = judgment
    except:
        pass
    result = json.dumps({"Judgments": ret_this})
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
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)
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
    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)
    except:
        pass
    # lastdate for judgments
    lastdate=[]
    try:
        lastdate = datereversed1[len(datereversed1) - 1]
    except:
        pass
    # Judgements
    judgment = []
    try:
        url2 = "http://cms.nic.in/ncdrcusersWeb/GetJudgement.do"
        payload = {'method': 'GetJudgement', 'dtofhearing': lastdate, 'caseidin':caseidin}
        r2 = requests.post(url=url2, params=payload)
        a = BeautifulSoup(r2.text, "lxml").text
        judgment.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ').replace('&nbsp', ' ')))
    except:
        pass
    ret_this = {}
    try:
        ret_this['Final Judgment'] = judgment
    except:
        pass
    result = json.dumps({"Judgments": ret_this})
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
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)
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
    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)
    except:
        pass
    # lastdate for judgments
    lastdate=[]
    try:
        lastdate = datereversed1[len(datereversed1) - 1]
    except:
        pass
    # Judgements
    judgment = []
    try:
        url2 = "http://cms.nic.in/ncdrcusersWeb/GetJudgement.do"
        payload = {'method': 'GetJudgement', 'dtofhearing': lastdate, 'caseidin':caseidin}
        r2 = requests.post(url=url2, params=payload)
        a = BeautifulSoup(r2.text, "lxml").text
        judgment.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ').replace('&nbsp', ' ')))
    except:
        pass
    ret_this = {}
    try:
        ret_this['Final Judgment'] = judgment
    except:
        pass
    result = json.dumps({"Judgments": ret_this})
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
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)
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
    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)
    except:
        pass
    # lastdate for judgments
    lastdate=[]
    try:
        lastdate = datereversed1[len(datereversed1) - 1]
    except:
        pass
    # Judgements
    judgment = []
    try:
        url2 = "http://cms.nic.in/ncdrcusersWeb/GetJudgement.do"
        payload = {'method': 'GetJudgement', 'dtofhearing': lastdate, 'caseidin':caseidin}
        r2 = requests.post(url=url2, params=payload)
        a = BeautifulSoup(r2.text, "lxml").text
        judgment.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ').replace('&nbsp', ' ')))
    except:
        pass
    ret_this = {}
    try:
        ret_this['Final Judgment'] = judgment
    except:
        pass
    result = json.dumps({"Judgments": ret_this})
    print(ftfy.fix_text_encoding(result))


