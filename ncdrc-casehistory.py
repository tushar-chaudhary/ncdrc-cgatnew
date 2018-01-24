import requests
from lxml import etree
import json
from io import StringIO
from datetime import datetime
from bs4 import BeautifulSoup
import re
import ftfy
re.compile('<title>(.*)</title>')


#URL:http://cms.nic.in/ncdrcusersWeb/courtroommodule.do?method=loadCaseHistory
def ncdrccasehistory(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    url = "http://cms.nic.in/ncdrcusersWeb/courtroommodule.do"
    params = [
     ("method",	"caseHistory"),
     ("searchCaseNo",	caseno),
     ("stateid", 0),
     ("distid", 0),
     ("prop1", "on"),
     ("prop2", "on"),
     ("prop4", "on"),
     ("prop6", "on"),
     ("prop8", "on"),
     ("prop10", "on"),
     ("prop12", "on"),
     ("prop13", "on"),
     ("prop14", "on"),
     ("prop15", "on"),
     ("prop16", "on"),
     ("prop18", "on"),
    ]
    r = requests.post(url=url, params = params)
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(r.text), parser)

    #complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[6]
        complainant.append(re.sub(r'[^\x00-\x7F]+', '', complainant1.strip() ))
    except: pass

    #respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[8]
        respondent.append(re.sub(r'[^\x00-\x7F]+', '', respondent1.strip() ))
    except: pass

    # filling date
    fillingdate = []
    try:
        fillingdate1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[1]
        fillingdate.append(re.sub(r'[^\x00-\x7F]+', '', fillingdate1.strip()))
    except:
        pass

    #dateOfnextHearing
    dateOfnextHearing = []
    try:
        dateOfnextHearing1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[4]
        dateOfnextHearing.append(re.sub(r'[^\x00-\x7F]+', '', dateOfnextHearing1.strip() ))
    except: pass



    #Case Stage
    casestage = []
    try:
        casestage1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[2]
        casestage.append(re.sub(r'[^\x00-\x7F]+', '', casestage1.strip() ))
    except: pass

    # CaseNo
    casenoo = []
    try:
        casenoo1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[0]
        casenoo.append(re.sub(r'[^\x00-\x7F]+', '', casenoo1.strip()))
    except: pass

    # CaseCategory
    casecategory = []
    try:
        casecategory1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[3]
        casecategory.append(re.sub(r'[^\x00-\x7F]+', '', casecategory1.strip()))
    except:
        pass

    # ResultOfCase
    resultofcase = []
    try:
        result1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[5]
        resultofcase.append(re.sub(r'[^\x00-\x7F]+', '', result1.strip()))
    except: pass

    # Advocate Name
    advocatename = []
    try:
        advocatename1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[7]
        advocatename.append(re.sub(r'[^\x00-\x7F]+', '', advocatename1.strip()))
    except: pass

    # Advocate Name2
    advocatename2 = []
    try:
        advocatename3 = tree.xpath('//*[@class="maintextborderdata"]/text()')[9]
        advocatename2.append(re.sub(r'[^\x00-\x7F]+', '', advocatename3.strip()))
    except: pass

    # Remarks in Filing
    remarks = []
    try:
        remarks1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[10]
        remarks.append(re.sub(r'[^\x00-\x7F]+', '', remarks1.strip()))
    except: pass

    #additional hearing info
    additionaldetails1 = tree.xpath('//tr[@id="cond3"]//td[@class="maintextborderdata"]//text()')
    additionaldetails = []
    index = []
    info = []
    details = []
    hearinginfo = []
    dates = []
    dateofhearingadd = []
    dateofnexthearingadd = []
    try:

        for i in range(0, len(additionaldetails1)):
            if additionaldetails1[i].strip() != "":
                additionaldetails.append(additionaldetails1[i].strip())
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                index.append(i)
        index.append(len(additionaldetails))

        for i in range(0, len(index) - 1):
            for j in range(index[i] + 1, index[i + 1]):
                info.append(additionaldetails[j])
            details.append(' '.join(info))
            info = []
        for i in range(0, len(details)):
            if details[i] != "":
                hearinginfo.append(re.sub(r'[^\x00-\x7F]+', ' ',details[i].replace('\n', '').replace('\r', '').replace('&nbsp', '')))
        # DATES INFO
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                dates.append(additionaldetails[i])

        for i in range(0, len(dates)):
            if i % 2 == 0:
                dateofhearingadd.append(dates[i])
            else:
                dateofnexthearingadd.append(dates[i])


    except:
        pass


    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Filing Date'] = fillingdate
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Case No'] = casenoo
        ret_this['Case Category'] = casecategory
        ret_this['Advocate Name'] = advocatename
        ret_this['Advocate Name.'] = advocatename2
        ret_this['Remarks in Filing'] = remarks
        ret_this['Result Of The Case'] = resultofcase
        ret_this['Additional Hearing Info'] = {}
        ret_this['Additional Hearing Info']['Date Of Hearing'] = dateofhearingadd
        ret_this['Additional Hearing Info']['Date Of Next Hearing'] = dateofnexthearingadd
        ret_this['Additional Hearing Info']['Case Proceedings Entered'] = hearinginfo
    except: pass


    result = json.dumps({"Case Status" : ret_this})
    print(ftfy.fix_text_encoding(result))


def statecommisioncasehistory(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    url = "http://cms.nic.in/ncdrcusersWeb/courtroommodule.do"
    params = [
     ("method",	"caseHistory"),
     ("searchCaseNo",	caseno),
     ("stateid", 8),
     ("distid", 0),
     ("prop1", "on"),
     ("prop2", "on"),
     ("prop4", "on"),
     ("prop6", "on"),
     ("prop8", "on"),
     ("prop10", "on"),
     ("prop12", "on"),
     ("prop13", "on"),
     ("prop14", "on"),
     ("prop15", "on"),
     ("prop16", "on"),
     ("prop18", "on"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[6]
        complainant.append(re.sub(r'[^\x00-\x7F]+', '', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[8]
        respondent.append(re.sub(r'[^\x00-\x7F]+', '', respondent1.strip()))
    except:
        pass

    # filling date
    fillingdate = []
    try:
        fillingdate1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[1]
        fillingdate.append(re.sub(r'[^\x00-\x7F]+', '', fillingdate1.strip()))
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        dateOfnextHearing1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[4]
        dateOfnextHearing.append(re.sub(r'[^\x00-\x7F]+', '', dateOfnextHearing1.strip()))
    except:
        pass

    # Case Stage
    casestage = []
    try:
        casestage1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[2]
        casestage.append(re.sub(r'[^\x00-\x7F]+', '', casestage1.strip()))
    except:
        pass

    # CaseNo
    casenoo = []
    try:
        casenoo1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[0]
        casenoo.append(re.sub(r'[^\x00-\x7F]+', '', casenoo1.strip()))
    except:
        pass

    # CaseCategory
    casecategory = []
    try:
        casecategory1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[3]
        casecategory.append(re.sub(r'[^\x00-\x7F]+', '', casecategory1.strip()))
    except:
        pass

    # ResultOfCase
    resultofcase = []
    try:
        result1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[5]
        resultofcase.append(re.sub(r'[^\x00-\x7F]+', '', result1.strip()))
    except:
        pass

    # Advocate Name
    advocatename = []
    try:
        advocatename1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[7]
        advocatename.append(re.sub(r'[^\x00-\x7F]+', '', advocatename1.strip()))
    except:
        pass

    # Advocate Name2
    advocatename2 = []
    try:
        advocatename3 = tree.xpath('//*[@class="maintextborderdata"]/text()')[9]
        advocatename2.append(re.sub(r'[^\x00-\x7F]+', '', advocatename3.strip()))
    except:
        pass

    # Remarks in Filing
    remarks = []
    try:
        remarks1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[10]
        remarks.append(re.sub(r'[^\x00-\x7F]+', '', remarks1.strip()))
    except:
        pass

    additionaldetails1 = tree.xpath('//tr[@id="cond3"]//td[@class="maintextborderdata"]//text()')
    additionaldetails = []
    index = []
    info = []
    details = []
    hearinginfo = []
    dates = []
    dateofhearingadd = []
    dateofnexthearingadd = []
    try:

        for i in range(0, len(additionaldetails1)):
            if additionaldetails1[i].strip() != "":
                additionaldetails.append(additionaldetails1[i].strip())
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                index.append(i)
        index.append(len(additionaldetails))

        for i in range(0, len(index) - 1):
            for j in range(index[i] + 1, index[i + 1]):
                info.append(additionaldetails[j])
            details.append(' '.join(info))
            info = []
        for i in range(0, len(details)):
            if details[i] != "":
                hearinginfo.append(re.sub(r'[^\x00-\x7F]+', ' ', details[i].replace('\n', '').replace('\r', '').replace('&nbsp', '')))
        # DATES INFO
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                dates.append(additionaldetails[i])

        for i in range(0, len(dates)):
            if i % 2 == 0:
                dateofhearingadd.append(dates[i])
            else:
                dateofnexthearingadd.append(dates[i])


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Filing Date'] = fillingdate
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Case No'] = casenoo
        ret_this['Case Category'] = casecategory
        ret_this['Advocate Name'] = advocatename
        ret_this['Advocate Name.'] = advocatename2
        ret_this['Remarks in Filing'] = remarks
        ret_this['Result Of The Case'] = resultofcase
        ret_this['Additional Hearing Info'] = {}
        ret_this['Additional Hearing Info']['Date Of Hearing'] = dateofhearingadd
        ret_this['Additional Hearing Info']['Date Of Next Hearing'] = dateofnexthearingadd
        ret_this['Additional Hearing Info']['Case Proceedings Entered'] = hearinginfo
    except:
        pass

    result = json.dumps({"Case Status": ret_this})
    print(ftfy.fix_text_encoding(result))


def centraldelhicasehistory(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    url = "http://cms.nic.in/ncdrcusersWeb/courtroommodule.do"
    params = [
     ("method",	"caseHistory"),
     ("searchCaseNo",	caseno),
     ("stateid", 8),
     ("distid", 3),
     ("prop1", "on"),
     ("prop2", "on"),
     ("prop4", "on"),
     ("prop6", "on"),
     ("prop8", "on"),
     ("prop10", "on"),
     ("prop12", "on"),
     ("prop13", "on"),
     ("prop14", "on"),
     ("prop15", "on"),
     ("prop16", "on"),
     ("prop18", "on"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[6]
        complainant.append(re.sub(r'[^\x00-\x7F]+', '', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[8]
        respondent.append(re.sub(r'[^\x00-\x7F]+', '', respondent1.strip()))
    except:
        pass

    # filling date
    fillingdate = []
    try:
        fillingdate1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[1]
        fillingdate.append(re.sub(r'[^\x00-\x7F]+', '', fillingdate1.strip()))
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        dateOfnextHearing1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[4]
        dateOfnextHearing.append(re.sub(r'[^\x00-\x7F]+', '', dateOfnextHearing1.strip()))
    except:
        pass

    # Case Stage
    casestage = []
    try:
        casestage1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[2]
        casestage.append(re.sub(r'[^\x00-\x7F]+', '', casestage1.strip()))
    except:
        pass

    # CaseNo
    casenoo = []
    try:
        casenoo1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[0]
        casenoo.append(re.sub(r'[^\x00-\x7F]+', '', casenoo1.strip()))
    except:
        pass

    # CaseCategory
    casecategory = []
    try:
        casecategory1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[3]
        casecategory.append(re.sub(r'[^\x00-\x7F]+', '', casecategory1.strip()))
    except:
        pass

    # ResultOfCase
    resultofcase = []
    try:
        result1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[5]
        resultofcase.append(re.sub(r'[^\x00-\x7F]+', '', result1.strip()))
    except:
        pass

    # Advocate Name
    advocatename = []
    try:
        advocatename1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[7]
        advocatename.append(re.sub(r'[^\x00-\x7F]+', '', advocatename1.strip()))
    except:
        pass

    # Advocate Name2
    advocatename2 = []
    try:
        advocatename3 = tree.xpath('//*[@class="maintextborderdata"]/text()')[9]
        advocatename2.append(re.sub(r'[^\x00-\x7F]+', '', advocatename3.strip()))
    except:
        pass

    # Remarks in Filing
    remarks = []
    try:
        remarks1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[10]
        remarks.append(re.sub(r'[^\x00-\x7F]+', '', remarks1.strip()))
    except:
        pass

    additionaldetails1 = tree.xpath('//tr[@id="cond3"]//td[@class="maintextborderdata"]//text()')
    additionaldetails = []
    index = []
    info = []
    details = []
    hearinginfo = []
    dates = []
    dateofhearingadd = []
    dateofnexthearingadd = []
    try:

        for i in range(0, len(additionaldetails1)):
            if additionaldetails1[i].strip() != "":
                additionaldetails.append(additionaldetails1[i].strip())
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                index.append(i)
        index.append(len(additionaldetails))

        for i in range(0, len(index) - 1):
            for j in range(index[i] + 1, index[i + 1]):
                info.append(additionaldetails[j])
            details.append(' '.join(info))
            info = []
        for i in range(0, len(details)):
            if details[i] != "":
                hearinginfo.append(re.sub(r'[^\x00-\x7F]+', ' ', details[i].replace('\n', '').replace('\r', '').replace('&nbsp', '')))
        # DATES INFO
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                dates.append(additionaldetails[i])

        for i in range(0, len(dates)):
            if i % 2 == 0:
                dateofhearingadd.append(dates[i])
            else:
                dateofnexthearingadd.append(dates[i])


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Filing Date'] = fillingdate
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Case No'] = casenoo
        ret_this['Case Category'] = casecategory
        ret_this['Advocate Name'] = advocatename
        ret_this['Advocate Name.'] = advocatename2
        ret_this['Remarks in Filing'] = remarks
        ret_this['Result Of The Case'] = resultofcase
        ret_this['Additional Hearing Info'] = {}
        ret_this['Additional Hearing Info']['Date Of Hearing'] = dateofhearingadd
        ret_this['Additional Hearing Info']['Date Of Next Hearing'] = dateofnexthearingadd
        ret_this['Additional Hearing Info']['Case Proceedings Entered'] = hearinginfo
    except:
        pass

    result = json.dumps({"Case Status": ret_this})
    print(ftfy.fix_text_encoding(result))


def eastdelhicasehistory(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    url = "http://cms.nic.in/ncdrcusersWeb/courtroommodule.do"
    params = [
     ("method",	"caseHistory"),
     ("searchCaseNo",	caseno),
     ("stateid", 8),
     ("distid", 5),
     ("prop1", "on"),
     ("prop2", "on"),
     ("prop4", "on"),
     ("prop6", "on"),
     ("prop8", "on"),
     ("prop10", "on"),
     ("prop12", "on"),
     ("prop13", "on"),
     ("prop14", "on"),
     ("prop15", "on"),
     ("prop16", "on"),
     ("prop18", "on"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[6]
        complainant.append(re.sub(r'[^\x00-\x7F]+', '', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[8]
        respondent.append(re.sub(r'[^\x00-\x7F]+', '', respondent1.strip()))
    except:
        pass

    # filling date
    fillingdate = []
    try:
        fillingdate1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[1]
        fillingdate.append(re.sub(r'[^\x00-\x7F]+', '', fillingdate1.strip()))
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        dateOfnextHearing1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[4]
        dateOfnextHearing.append(re.sub(r'[^\x00-\x7F]+', '', dateOfnextHearing1.strip()))
    except:
        pass

    # Case Stage
    casestage = []
    try:
        casestage1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[2]
        casestage.append(re.sub(r'[^\x00-\x7F]+', '', casestage1.strip()))
    except:
        pass

    # CaseNo
    casenoo = []
    try:
        casenoo1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[0]
        casenoo.append(re.sub(r'[^\x00-\x7F]+', '', casenoo1.strip()))
    except:
        pass

    # CaseCategory
    casecategory = []
    try:
        casecategory1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[3]
        casecategory.append(re.sub(r'[^\x00-\x7F]+', '', casecategory1.strip()))
    except:
        pass

    # ResultOfCase
    resultofcase = []
    try:
        result1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[5]
        resultofcase.append(re.sub(r'[^\x00-\x7F]+', '', result1.strip()))
    except:
        pass

    # Advocate Name
    advocatename = []
    try:
        advocatename1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[7]
        advocatename.append(re.sub(r'[^\x00-\x7F]+', '', advocatename1.strip()))
    except:
        pass

    # Advocate Name2
    advocatename2 = []
    try:
        advocatename3 = tree.xpath('//*[@class="maintextborderdata"]/text()')[9]
        advocatename2.append(re.sub(r'[^\x00-\x7F]+', '', advocatename3.strip()))
    except:
        pass

    # Remarks in Filing
    remarks = []
    try:
        remarks1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[10]
        remarks.append(re.sub(r'[^\x00-\x7F]+', '', remarks1.strip()))
    except:
        pass

    additionaldetails1 = tree.xpath('//tr[@id="cond3"]//td[@class="maintextborderdata"]//text()')
    additionaldetails = []
    index = []
    info = []
    details = []
    hearinginfo = []
    dates = []
    dateofhearingadd = []
    dateofnexthearingadd = []
    try:

        for i in range(0, len(additionaldetails1)):
            if additionaldetails1[i].strip() != "":
                additionaldetails.append(additionaldetails1[i].strip())
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                index.append(i)
        index.append(len(additionaldetails))

        for i in range(0, len(index) - 1):
            for j in range(index[i] + 1, index[i + 1]):
                info.append(additionaldetails[j])
            details.append(' '.join(info))
            info = []
        for i in range(0, len(details)):
            if details[i] != "":
                hearinginfo.append(re.sub(r'[^\x00-\x7F]+', ' ', details[i].replace('\n', '').replace('\r', '').replace('&nbsp', '')))
        # DATES INFO
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                dates.append(additionaldetails[i])

        for i in range(0, len(dates)):
            if i % 2 == 0:
                dateofhearingadd.append(dates[i])
            else:
                dateofnexthearingadd.append(dates[i])


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Filing Date'] = fillingdate
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Case No'] = casenoo
        ret_this['Case Category'] = casecategory
        ret_this['Advocate Name'] = advocatename
        ret_this['Advocate Name.'] = advocatename2
        ret_this['Remarks in Filing'] = remarks
        ret_this['Result Of The Case'] = resultofcase
        ret_this['Additional Hearing Info'] = {}
        ret_this['Additional Hearing Info']['Date Of Hearing'] = dateofhearingadd
        ret_this['Additional Hearing Info']['Date Of Next Hearing'] = dateofnexthearingadd
        ret_this['Additional Hearing Info']['Case Proceedings Entered'] = hearinginfo
    except:
        pass

    result = json.dumps({"Case Status": ret_this})
    print(ftfy.fix_text_encoding(result))


def newdelhicasehistory(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    url = "http://cms.nic.in/ncdrcusersWeb/courtroommodule.do"
    params = [
        ("method", "caseHistory"),
        ("searchCaseNo", caseno),
        ("stateid", 8),
        ("distid", 12),
        ("prop1", "on"),
        ("prop2", "on"),
        ("prop4", "on"),
        ("prop6", "on"),
        ("prop8", "on"),
        ("prop10", "on"),
        ("prop12", "on"),
        ("prop13", "on"),
        ("prop14", "on"),
        ("prop15", "on"),
        ("prop16", "on"),
        ("prop18", "on"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[6]
        complainant.append(re.sub(r'[^\x00-\x7F]+', '', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[8]
        respondent.append(re.sub(r'[^\x00-\x7F]+', '', respondent1.strip()))
    except:
        pass

    # filling date
    fillingdate = []
    try:
        fillingdate1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[1]
        fillingdate.append(re.sub(r'[^\x00-\x7F]+', '', fillingdate1.strip()))
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        dateOfnextHearing1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[4]
        dateOfnextHearing.append(re.sub(r'[^\x00-\x7F]+', '', dateOfnextHearing1.strip()))
    except:
        pass

    # Case Stage
    casestage = []
    try:
        casestage1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[2]
        casestage.append(re.sub(r'[^\x00-\x7F]+', '', casestage1.strip()))
    except:
        pass

    # CaseNo
    casenoo = []
    try:
        casenoo1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[0]
        casenoo.append(re.sub(r'[^\x00-\x7F]+', '', casenoo1.strip()))
    except:
        pass

    # CaseCategory
    casecategory = []
    try:
        casecategory1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[3]
        casecategory.append(re.sub(r'[^\x00-\x7F]+', '', casecategory1.strip()))
    except:
        pass

    # ResultOfCase
    resultofcase = []
    try:
        result1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[5]
        resultofcase.append(re.sub(r'[^\x00-\x7F]+', '', result1.strip()))
    except:
        pass

    # Advocate Name
    advocatename = []
    try:
        advocatename1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[7]
        advocatename.append(re.sub(r'[^\x00-\x7F]+', '', advocatename1.strip()))
    except:
        pass

    # Advocate Name2
    advocatename2 = []
    try:
        advocatename3 = tree.xpath('//*[@class="maintextborderdata"]/text()')[9]
        advocatename2.append(re.sub(r'[^\x00-\x7F]+', '', advocatename3.strip()))
    except:
        pass

    # Remarks in Filing
    remarks = []
    try:
        remarks1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[10]
        remarks.append(re.sub(r'[^\x00-\x7F]+', '', remarks1.strip()))
    except:
        pass

    additionaldetails1 = tree.xpath('//tr[@id="cond3"]//td[@class="maintextborderdata"]//text()')
    additionaldetails = []
    index = []
    info = []
    details = []
    hearinginfo = []
    dates = []
    dateofhearingadd = []
    dateofnexthearingadd = []
    try:

        for i in range(0, len(additionaldetails1)):
            if additionaldetails1[i].strip() != "":
                additionaldetails.append(additionaldetails1[i].strip())
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                index.append(i)
        index.append(len(additionaldetails))

        for i in range(0, len(index) - 1):
            for j in range(index[i] + 1, index[i + 1]):
                info.append(additionaldetails[j])
            details.append(' '.join(info))
            info = []
        for i in range(0, len(details)):
            if details[i] != "":
                hearinginfo.append(re.sub(r'[^\x00-\x7F]+', ' ', details[i].replace('\n', '').replace('\r', '').replace('&nbsp', '')))
        # DATES INFO
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                dates.append(additionaldetails[i])

        for i in range(0, len(dates)):
            if i % 2 == 0:
                dateofhearingadd.append(dates[i])
            else:
                dateofnexthearingadd.append(dates[i])


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Filing Date'] = fillingdate
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Case No'] = casenoo
        ret_this['Case Category'] = casecategory
        ret_this['Advocate Name'] = advocatename
        ret_this['Advocate Name.'] = advocatename2
        ret_this['Remarks in Filing'] = remarks
        ret_this['Result Of The Case'] = resultofcase
        ret_this['Additional Hearing Info'] = {}
        ret_this['Additional Hearing Info']['Date Of Hearing'] = dateofhearingadd
        ret_this['Additional Hearing Info']['Date Of Next Hearing'] = dateofnexthearingadd
        ret_this['Additional Hearing Info']['Case Proceedings Entered'] = hearinginfo
    except:
        pass

    result = json.dumps({"Case Status": ret_this})
    print(ftfy.fix_text_encoding(result))


def northcasehistory(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    url = "http://cms.nic.in/ncdrcusersWeb/courtroommodule.do"
    params = [
     ("method",	"caseHistory"),
     ("searchCaseNo",	caseno),
     ("stateid", 8),
     ("distid", 9),
     ("prop1", "on"),
     ("prop2", "on"),
     ("prop4", "on"),
     ("prop6", "on"),
     ("prop8", "on"),
     ("prop10", "on"),
     ("prop12", "on"),
     ("prop13", "on"),
     ("prop14", "on"),
     ("prop15", "on"),
     ("prop16", "on"),
     ("prop18", "on"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[6]
        complainant.append(re.sub(r'[^\x00-\x7F]+', '', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[8]
        respondent.append(re.sub(r'[^\x00-\x7F]+', '', respondent1.strip()))
    except:
        pass

    # filling date
    fillingdate = []
    try:
        fillingdate1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[1]
        fillingdate.append(re.sub(r'[^\x00-\x7F]+', '', fillingdate1.strip()))
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        dateOfnextHearing1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[4]
        dateOfnextHearing.append(re.sub(r'[^\x00-\x7F]+', '', dateOfnextHearing1.strip()))
    except:
        pass

    # Case Stage
    casestage = []
    try:
        casestage1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[2]
        casestage.append(re.sub(r'[^\x00-\x7F]+', '', casestage1.strip()))
    except:
        pass

    # CaseNo
    casenoo = []
    try:
        casenoo1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[0]
        casenoo.append(re.sub(r'[^\x00-\x7F]+', '', casenoo1.strip()))
    except:
        pass

    # CaseCategory
    casecategory = []
    try:
        casecategory1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[3]
        casecategory.append(re.sub(r'[^\x00-\x7F]+', '', casecategory1.strip()))
    except:
        pass

    # ResultOfCase
    resultofcase = []
    try:
        result1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[5]
        resultofcase.append(re.sub(r'[^\x00-\x7F]+', '', result1.strip()))
    except:
        pass

    # Advocate Name
    advocatename = []
    try:
        advocatename1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[7]
        advocatename.append(re.sub(r'[^\x00-\x7F]+', '', advocatename1.strip()))
    except:
        pass

    # Advocate Name2
    advocatename2 = []
    try:
        advocatename3 = tree.xpath('//*[@class="maintextborderdata"]/text()')[9]
        advocatename2.append(re.sub(r'[^\x00-\x7F]+', '', advocatename3.strip()))
    except:
        pass

    # Remarks in Filing
    remarks = []
    try:
        remarks1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[10]
        remarks.append(re.sub(r'[^\x00-\x7F]+', '', remarks1.strip()))
    except:
        pass

    additionaldetails1 = tree.xpath('//tr[@id="cond3"]//td[@class="maintextborderdata"]//text()')
    additionaldetails = []
    index = []
    info = []
    details = []
    hearinginfo = []
    dates = []
    dateofhearingadd = []
    dateofnexthearingadd = []
    try:

        for i in range(0, len(additionaldetails1)):
            if additionaldetails1[i].strip() != "":
                additionaldetails.append(additionaldetails1[i].strip())
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                index.append(i)
        index.append(len(additionaldetails))

        for i in range(0, len(index) - 1):
            for j in range(index[i] + 1, index[i + 1]):
                info.append(additionaldetails[j])
            details.append(' '.join(info))
            info = []
        for i in range(0, len(details)):
            if details[i] != "":
                hearinginfo.append(re.sub(r'[^\x00-\x7F]+', ' ', details[i].replace('\n', '').replace('\r', '').replace('&nbsp', '')))
        # DATES INFO
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                dates.append(additionaldetails[i])

        for i in range(0, len(dates)):
            if i % 2 == 0:
                dateofhearingadd.append(dates[i])
            else:
                dateofnexthearingadd.append(dates[i])


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Filing Date'] = fillingdate
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Case No'] = casenoo
        ret_this['Case Category'] = casecategory
        ret_this['Advocate Name'] = advocatename
        ret_this['Advocate Name.'] = advocatename2
        ret_this['Remarks in Filing'] = remarks
        ret_this['Result Of The Case'] = resultofcase
        ret_this['Additional Hearing Info'] = {}
        ret_this['Additional Hearing Info']['Date Of Hearing'] = dateofhearingadd
        ret_this['Additional Hearing Info']['Date Of Next Hearing'] = dateofnexthearingadd
        ret_this['Additional Hearing Info']['Case Proceedings Entered'] = hearinginfo
    except:
        pass

    result = json.dumps({"Case Status": ret_this})
    print(ftfy.fix_text_encoding(result))


def northeastcasehistory(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    url = "http://cms.nic.in/ncdrcusersWeb/courtroommodule.do"
    params = [
     ("method",	"caseHistory"),
     ("searchCaseNo",	caseno),
     ("stateid", 8),
     ("distid", 10),
     ("prop1", "on"),
     ("prop2", "on"),
     ("prop4", "on"),
     ("prop6", "on"),
     ("prop8", "on"),
     ("prop10", "on"),
     ("prop12", "on"),
     ("prop13", "on"),
     ("prop14", "on"),
     ("prop15", "on"),
     ("prop16", "on"),
     ("prop18", "on"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[6]
        complainant.append(re.sub(r'[^\x00-\x7F]+', '', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[8]
        respondent.append(re.sub(r'[^\x00-\x7F]+', '', respondent1.strip()))
    except:
        pass

    # filling date
    fillingdate = []
    try:
        fillingdate1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[1]
        fillingdate.append(re.sub(r'[^\x00-\x7F]+', '', fillingdate1.strip()))
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        dateOfnextHearing1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[4]
        dateOfnextHearing.append(re.sub(r'[^\x00-\x7F]+', '', dateOfnextHearing1.strip()))
    except:
        pass

    # Case Stage
    casestage = []
    try:
        casestage1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[2]
        casestage.append(re.sub(r'[^\x00-\x7F]+', '', casestage1.strip()))
    except:
        pass

    # CaseNo
    casenoo = []
    try:
        casenoo1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[0]
        casenoo.append(re.sub(r'[^\x00-\x7F]+', '', casenoo1.strip()))
    except:
        pass

    # CaseCategory
    casecategory = []
    try:
        casecategory1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[3]
        casecategory.append(re.sub(r'[^\x00-\x7F]+', '', casecategory1.strip()))
    except:
        pass

    # ResultOfCase
    resultofcase = []
    try:
        result1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[5]
        resultofcase.append(re.sub(r'[^\x00-\x7F]+', '', result1.strip()))
    except:
        pass

    # Advocate Name
    advocatename = []
    try:
        advocatename1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[7]
        advocatename.append(re.sub(r'[^\x00-\x7F]+', '', advocatename1.strip()))
    except:
        pass

    # Advocate Name2
    advocatename2 = []
    try:
        advocatename3 = tree.xpath('//*[@class="maintextborderdata"]/text()')[9]
        advocatename2.append(re.sub(r'[^\x00-\x7F]+', '', advocatename3.strip()))
    except:
        pass

    # Remarks in Filing
    remarks = []
    try:
        remarks1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[10]
        remarks.append(re.sub(r'[^\x00-\x7F]+', '', remarks1.strip()))
    except:
        pass

    additionaldetails1 = tree.xpath('//tr[@id="cond3"]//td[@class="maintextborderdata"]//text()')
    additionaldetails = []
    index = []
    info = []
    details = []
    hearinginfo = []
    dates = []
    dateofhearingadd = []
    dateofnexthearingadd = []
    try:

        for i in range(0, len(additionaldetails1)):
            if additionaldetails1[i].strip() != "":
                additionaldetails.append(additionaldetails1[i].strip())
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                index.append(i)
        index.append(len(additionaldetails))

        for i in range(0, len(index) - 1):
            for j in range(index[i] + 1, index[i + 1]):
                info.append(additionaldetails[j])
            details.append(' '.join(info))
            info = []
        for i in range(0, len(details)):
            if details[i] != "":
                hearinginfo.append(re.sub(r'[^\x00-\x7F]+', ' ', details[i].replace('\n', '').replace('\r', '').replace('&nbsp', '')))
        # DATES INFO
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                dates.append(additionaldetails[i])

        for i in range(0, len(dates)):
            if i % 2 == 0:
                dateofhearingadd.append(dates[i])
            else:
                dateofnexthearingadd.append(dates[i])


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Filing Date'] = fillingdate
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Case No'] = casenoo
        ret_this['Case Category'] = casecategory
        ret_this['Advocate Name'] = advocatename
        ret_this['Advocate Name.'] = advocatename2
        ret_this['Remarks in Filing'] = remarks
        ret_this['Result Of The Case'] = resultofcase
        ret_this['Additional Hearing Info'] = {}
        ret_this['Additional Hearing Info']['Date Of Hearing'] = dateofhearingadd
        ret_this['Additional Hearing Info']['Date Of Next Hearing'] = dateofnexthearingadd
        ret_this['Additional Hearing Info']['Case Proceedings Entered'] = hearinginfo
    except:
        pass

    result = json.dumps({"Case Status": ret_this})
    print(ftfy.fix_text_encoding(result))


def northwestcasehistory(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    url = "http://cms.nic.in/ncdrcusersWeb/courtroommodule.do"
    params = [
     ("method",	"caseHistory"),
     ("searchCaseNo",	caseno),
     ("stateid", 8),
     ("distid", 7),
     ("prop1", "on"),
     ("prop2", "on"),
     ("prop4", "on"),
     ("prop6", "on"),
     ("prop8", "on"),
     ("prop10", "on"),
     ("prop12", "on"),
     ("prop13", "on"),
     ("prop14", "on"),
     ("prop15", "on"),
     ("prop16", "on"),
     ("prop18", "on"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[6]
        complainant.append(re.sub(r'[^\x00-\x7F]+', '', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[8]
        respondent.append(re.sub(r'[^\x00-\x7F]+', '', respondent1.strip()))
    except:
        pass

    # filling date
    fillingdate = []
    try:
        fillingdate1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[1]
        fillingdate.append(re.sub(r'[^\x00-\x7F]+', '', fillingdate1.strip()))
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        dateOfnextHearing1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[4]
        dateOfnextHearing.append(re.sub(r'[^\x00-\x7F]+', '', dateOfnextHearing1.strip()))
    except:
        pass

    # Case Stage
    casestage = []
    try:
        casestage1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[2]
        casestage.append(re.sub(r'[^\x00-\x7F]+', '', casestage1.strip()))
    except:
        pass

    # CaseNo
    casenoo = []
    try:
        casenoo1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[0]
        casenoo.append(re.sub(r'[^\x00-\x7F]+', '', casenoo1.strip()))
    except:
        pass

    # CaseCategory
    casecategory = []
    try:
        casecategory1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[3]
        casecategory.append(re.sub(r'[^\x00-\x7F]+', '', casecategory1.strip()))
    except:
        pass

    # ResultOfCase
    resultofcase = []
    try:
        result1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[5]
        resultofcase.append(re.sub(r'[^\x00-\x7F]+', '', result1.strip()))
    except:
        pass

    # Advocate Name
    advocatename = []
    try:
        advocatename1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[7]
        advocatename.append(re.sub(r'[^\x00-\x7F]+', '', advocatename1.strip()))
    except:
        pass

    # Advocate Name2
    advocatename2 = []
    try:
        advocatename3 = tree.xpath('//*[@class="maintextborderdata"]/text()')[9]
        advocatename2.append(re.sub(r'[^\x00-\x7F]+', '', advocatename3.strip()))
    except:
        pass

    # Remarks in Filing
    remarks = []
    try:
        remarks1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[10]
        remarks.append(re.sub(r'[^\x00-\x7F]+', '', remarks1.strip()))
    except:
        pass

    additionaldetails1 = tree.xpath('//tr[@id="cond3"]//td[@class="maintextborderdata"]//text()')
    additionaldetails = []
    index = []
    info = []
    details = []
    hearinginfo = []
    dates = []
    dateofhearingadd = []
    dateofnexthearingadd = []
    try:

        for i in range(0, len(additionaldetails1)):
            if additionaldetails1[i].strip() != "":
                additionaldetails.append(additionaldetails1[i].strip())
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                index.append(i)
        index.append(len(additionaldetails))

        for i in range(0, len(index) - 1):
            for j in range(index[i] + 1, index[i + 1]):
                info.append(additionaldetails[j])
            details.append(' '.join(info))
            info = []
        for i in range(0, len(details)):
            if details[i] != "":
                hearinginfo.append(re.sub(r'[^\x00-\x7F]+', ' ', details[i].replace('\n', '').replace('\r', '').replace('&nbsp', '')))
        # DATES INFO
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                dates.append(additionaldetails[i])

        for i in range(0, len(dates)):
            if i % 2 == 0:
                dateofhearingadd.append(dates[i])
            else:
                dateofnexthearingadd.append(dates[i])


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Filing Date'] = fillingdate
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Case No'] = casenoo
        ret_this['Case Category'] = casecategory
        ret_this['Advocate Name'] = advocatename
        ret_this['Advocate Name.'] = advocatename2
        ret_this['Remarks in Filing'] = remarks
        ret_this['Result Of The Case'] = resultofcase
        ret_this['Additional Hearing Info'] = {}
        ret_this['Additional Hearing Info']['Date Of Hearing'] = dateofhearingadd
        ret_this['Additional Hearing Info']['Date Of Next Hearing'] = dateofnexthearingadd
        ret_this['Additional Hearing Info']['Case Proceedings Entered'] = hearinginfo
    except:
        pass

    result = json.dumps({"Case Status": ret_this})
    print(ftfy.fix_text_encoding(result))


def southdelhicasehistory(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    url = "http://cms.nic.in/ncdrcusersWeb/courtroommodule.do"
    params = [
     ("method",	"caseHistory"),
     ("searchCaseNo",	caseno),
     ("stateid", 8),
     ("distid", 6),
     ("prop1", "on"),
     ("prop2", "on"),
     ("prop4", "on"),
     ("prop6", "on"),
     ("prop8", "on"),
     ("prop10", "on"),
     ("prop12", "on"),
     ("prop13", "on"),
     ("prop14", "on"),
     ("prop15", "on"),
     ("prop16", "on"),
     ("prop18", "on"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[6]
        complainant.append(re.sub(r'[^\x00-\x7F]+', '', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[8]
        respondent.append(re.sub(r'[^\x00-\x7F]+', '', respondent1.strip()))
    except:
        pass

    # filling date
    fillingdate = []
    try:
        fillingdate1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[1]
        fillingdate.append(re.sub(r'[^\x00-\x7F]+', '', fillingdate1.strip()))
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        dateOfnextHearing1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[4]
        dateOfnextHearing.append(re.sub(r'[^\x00-\x7F]+', '', dateOfnextHearing1.strip()))
    except:
        pass

    # Case Stage
    casestage = []
    try:
        casestage1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[2]
        casestage.append(re.sub(r'[^\x00-\x7F]+', '', casestage1.strip()))
    except:
        pass

    # CaseNo
    casenoo = []
    try:
        casenoo1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[0]
        casenoo.append(re.sub(r'[^\x00-\x7F]+', '', casenoo1.strip()))
    except:
        pass

    # CaseCategory
    casecategory = []
    try:
        casecategory1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[3]
        casecategory.append(re.sub(r'[^\x00-\x7F]+', '', casecategory1.strip()))
    except:
        pass

    # ResultOfCase
    resultofcase = []
    try:
        result1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[5]
        resultofcase.append(re.sub(r'[^\x00-\x7F]+', '', result1.strip()))
    except:
        pass

    # Advocate Name
    advocatename = []
    try:
        advocatename1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[7]
        advocatename.append(re.sub(r'[^\x00-\x7F]+', '', advocatename1.strip()))
    except:
        pass

    # Advocate Name2
    advocatename2 = []
    try:
        advocatename3 = tree.xpath('//*[@class="maintextborderdata"]/text()')[9]
        advocatename2.append(re.sub(r'[^\x00-\x7F]+', '', advocatename3.strip()))
    except:
        pass

    # Remarks in Filing
    remarks = []
    try:
        remarks1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[10]
        remarks.append(re.sub(r'[^\x00-\x7F]+', '', remarks1.strip()))
    except:
        pass

    additionaldetails1 = tree.xpath('//tr[@id="cond3"]//td[@class="maintextborderdata"]//text()')
    additionaldetails = []
    index = []
    info = []
    details = []
    hearinginfo = []
    dates = []
    dateofhearingadd = []
    dateofnexthearingadd = []
    try:

        for i in range(0, len(additionaldetails1)):
            if additionaldetails1[i].strip() != "":
                additionaldetails.append(additionaldetails1[i].strip())
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                index.append(i)
        index.append(len(additionaldetails))

        for i in range(0, len(index) - 1):
            for j in range(index[i] + 1, index[i + 1]):
                info.append(additionaldetails[j])
            details.append(' '.join(info))
            info = []
        for i in range(0, len(details)):
            if details[i] != "":
                hearinginfo.append(re.sub(r'[^\x00-\x7F]+', ' ', details[i].replace('\n', '').replace('\r', '').replace('&nbsp', '')))
        # DATES INFO
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                dates.append(additionaldetails[i])

        for i in range(0, len(dates)):
            if i % 2 == 0:
                dateofhearingadd.append(dates[i])
            else:
                dateofnexthearingadd.append(dates[i])


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Filing Date'] = fillingdate
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Case No'] = casenoo
        ret_this['Case Category'] = casecategory
        ret_this['Advocate Name'] = advocatename
        ret_this['Advocate Name.'] = advocatename2
        ret_this['Remarks in Filing'] = remarks
        ret_this['Result Of The Case'] = resultofcase
        ret_this['Additional Hearing Info'] = {}
        ret_this['Additional Hearing Info']['Date Of Hearing'] = dateofhearingadd
        ret_this['Additional Hearing Info']['Date Of Next Hearing'] = dateofnexthearingadd
        ret_this['Additional Hearing Info']['Case Proceedings Entered'] = hearinginfo
    except:
        pass

    result = json.dumps({"Case Status": ret_this})
    print(ftfy.fix_text_encoding(result))


def south2casehistory(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    url = "http://cms.nic.in/ncdrcusersWeb/courtroommodule.do"
    params = [
        ("method", "caseHistory"),
        ("searchCaseNo", caseno),
        ("stateid", 8),
        ("distid", 16),
        ("prop1", "on"),
        ("prop2", "on"),
        ("prop4", "on"),
        ("prop6", "on"),
        ("prop8", "on"),
        ("prop10", "on"),
        ("prop12", "on"),
        ("prop13", "on"),
        ("prop14", "on"),
        ("prop15", "on"),
        ("prop16", "on"),
        ("prop18", "on"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[6]
        complainant.append(re.sub(r'[^\x00-\x7F]+', '', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[8]
        respondent.append(re.sub(r'[^\x00-\x7F]+', '', respondent1.strip()))
    except:
        pass

    # filling date
    fillingdate = []
    try:
        fillingdate1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[1]
        fillingdate.append(re.sub(r'[^\x00-\x7F]+', '', fillingdate1.strip()))
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        dateOfnextHearing1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[4]
        dateOfnextHearing.append(re.sub(r'[^\x00-\x7F]+', '', dateOfnextHearing1.strip()))
    except:
        pass

    # Case Stage
    casestage = []
    try:
        casestage1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[2]
        casestage.append(re.sub(r'[^\x00-\x7F]+', '', casestage1.strip()))
    except:
        pass

    # CaseNo
    casenoo = []
    try:
        casenoo1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[0]
        casenoo.append(re.sub(r'[^\x00-\x7F]+', '', casenoo1.strip()))
    except:
        pass

    # CaseCategory
    casecategory = []
    try:
        casecategory1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[3]
        casecategory.append(re.sub(r'[^\x00-\x7F]+', '', casecategory1.strip()))
    except:
        pass

    # ResultOfCase
    resultofcase = []
    try:
        result1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[5]
        resultofcase.append(re.sub(r'[^\x00-\x7F]+', '', result1.strip()))
    except:
        pass

    # Advocate Name
    advocatename = []
    try:
        advocatename1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[7]
        advocatename.append(re.sub(r'[^\x00-\x7F]+', '', advocatename1.strip()))
    except:
        pass

    # Advocate Name2
    advocatename2 = []
    try:
        advocatename3 = tree.xpath('//*[@class="maintextborderdata"]/text()')[9]
        advocatename2.append(re.sub(r'[^\x00-\x7F]+', '', advocatename3.strip()))
    except:
        pass

    # Remarks in Filing
    remarks = []
    try:
        remarks1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[10]
        remarks.append(re.sub(r'[^\x00-\x7F]+', '', remarks1.strip()))
    except:
        pass

    additionaldetails1 = tree.xpath('//tr[@id="cond3"]//td[@class="maintextborderdata"]//text()')
    additionaldetails = []
    index = []
    info = []
    details = []
    hearinginfo = []
    dates = []
    dateofhearingadd = []
    dateofnexthearingadd = []
    try:

        for i in range(0, len(additionaldetails1)):
            if additionaldetails1[i].strip() != "":
                additionaldetails.append(additionaldetails1[i].strip())
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                index.append(i)
        index.append(len(additionaldetails))

        for i in range(0, len(index) - 1):
            for j in range(index[i] + 1, index[i + 1]):
                info.append(additionaldetails[j])
            details.append(' '.join(info))
            info = []
        for i in range(0, len(details)):
            if details[i] != "":
                hearinginfo.append(re.sub(r'[^\x00-\x7F]+', ' ', details[i].replace('\n', '').replace('\r', '').replace('&nbsp', '')))
        # DATES INFO
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                dates.append(additionaldetails[i])

        for i in range(0, len(dates)):
            if i % 2 == 0:
                dateofhearingadd.append(dates[i])
            else:
                dateofnexthearingadd.append(dates[i])


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Filing Date'] = fillingdate
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Case No'] = casenoo
        ret_this['Case Category'] = casecategory
        ret_this['Advocate Name'] = advocatename
        ret_this['Advocate Name.'] = advocatename2
        ret_this['Remarks in Filing'] = remarks
        ret_this['Result Of The Case'] = resultofcase
        ret_this['Additional Hearing Info'] = {}
        ret_this['Additional Hearing Info']['Date Of Hearing'] = dateofhearingadd
        ret_this['Additional Hearing Info']['Date Of Next Hearing'] = dateofnexthearingadd
        ret_this['Additional Hearing Info']['Case Proceedings Entered'] = hearinginfo
    except:
        pass

    result = json.dumps({"Case Status": ret_this})
    print(ftfy.fix_text_encoding(result))


def southwestcasehistory(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    url = "http://cms.nic.in/ncdrcusersWeb/courtroommodule.do"
    params = [
     ("method",	"caseHistory"),
     ("searchCaseNo",	caseno),
     ("stateid", 8),
     ("distid", 15),
     ("prop1", "on"),
     ("prop2", "on"),
     ("prop4", "on"),
     ("prop6", "on"),
     ("prop8", "on"),
     ("prop10", "on"),
     ("prop12", "on"),
     ("prop13", "on"),
     ("prop14", "on"),
     ("prop15", "on"),
     ("prop16", "on"),
     ("prop18", "on"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[6]
        complainant.append(re.sub(r'[^\x00-\x7F]+', '', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[8]
        respondent.append(re.sub(r'[^\x00-\x7F]+', '', respondent1.strip()))
    except:
        pass

    # filling date
    fillingdate = []
    try:
        fillingdate1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[1]
        fillingdate.append(re.sub(r'[^\x00-\x7F]+', '', fillingdate1.strip()))
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        dateOfnextHearing1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[4]
        dateOfnextHearing.append(re.sub(r'[^\x00-\x7F]+', '', dateOfnextHearing1.strip()))
    except:
        pass

    # Case Stage
    casestage = []
    try:
        casestage1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[2]
        casestage.append(re.sub(r'[^\x00-\x7F]+', '', casestage1.strip()))
    except:
        pass

    # CaseNo
    casenoo = []
    try:
        casenoo1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[0]
        casenoo.append(re.sub(r'[^\x00-\x7F]+', '', casenoo1.strip()))
    except:
        pass

    # CaseCategory
    casecategory = []
    try:
        casecategory1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[3]
        casecategory.append(re.sub(r'[^\x00-\x7F]+', '', casecategory1.strip()))
    except:
        pass

    # ResultOfCase
    resultofcase = []
    try:
        result1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[5]
        resultofcase.append(re.sub(r'[^\x00-\x7F]+', '', result1.strip()))
    except:
        pass

    # Advocate Name
    advocatename = []
    try:
        advocatename1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[7]
        advocatename.append(re.sub(r'[^\x00-\x7F]+', '', advocatename1.strip()))
    except:
        pass

    # Advocate Name2
    advocatename2 = []
    try:
        advocatename3 = tree.xpath('//*[@class="maintextborderdata"]/text()')[9]
        advocatename2.append(re.sub(r'[^\x00-\x7F]+', '', advocatename3.strip()))
    except:
        pass

    # Remarks in Filing
    remarks = []
    try:
        remarks1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[10]
        remarks.append(re.sub(r'[^\x00-\x7F]+', '', remarks1.strip()))
    except:
        pass

    additionaldetails1 = tree.xpath('//tr[@id="cond3"]//td[@class="maintextborderdata"]//text()')
    additionaldetails = []
    index = []
    info = []
    details = []
    hearinginfo = []
    dates = []
    dateofhearingadd = []
    dateofnexthearingadd = []
    try:

        for i in range(0, len(additionaldetails1)):
            if additionaldetails1[i].strip() != "":
                additionaldetails.append(additionaldetails1[i].strip())
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                index.append(i)
        index.append(len(additionaldetails))

        for i in range(0, len(index) - 1):
            for j in range(index[i] + 1, index[i + 1]):
                info.append(additionaldetails[j])
            details.append(' '.join(info))
            info = []
        for i in range(0, len(details)):
            if details[i] != "":
                hearinginfo.append(re.sub(r'[^\x00-\x7F]+', ' ', details[i].replace('\n', '').replace('\r', '').replace('&nbsp', '')))
        # DATES INFO
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                dates.append(additionaldetails[i])

        for i in range(0, len(dates)):
            if i % 2 == 0:
                dateofhearingadd.append(dates[i])
            else:
                dateofnexthearingadd.append(dates[i])


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Filing Date'] = fillingdate
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Case No'] = casenoo
        ret_this['Case Category'] = casecategory
        ret_this['Advocate Name'] = advocatename
        ret_this['Advocate Name.'] = advocatename2
        ret_this['Remarks in Filing'] = remarks
        ret_this['Result Of The Case'] = resultofcase
        ret_this['Additional Hearing Info'] = {}
        ret_this['Additional Hearing Info']['Date Of Hearing'] = dateofhearingadd
        ret_this['Additional Hearing Info']['Date Of Next Hearing'] = dateofnexthearingadd
        ret_this['Additional Hearing Info']['Case Proceedings Entered'] = hearinginfo
    except:
        pass

    result = json.dumps({"Case Status": ret_this})
    print(ftfy.fix_text_encoding(result))


def westdelhicasehistory(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    url = "http://cms.nic.in/ncdrcusersWeb/courtroommodule.do"
    params = [
     ("method",	"caseHistory"),
     ("searchCaseNo",	caseno),
     ("stateid", 8),
     ("distid", 4),
     ("prop1", "on"),
     ("prop2", "on"),
     ("prop4", "on"),
     ("prop6", "on"),
     ("prop8", "on"),
     ("prop10", "on"),
     ("prop12", "on"),
     ("prop13", "on"),
     ("prop14", "on"),
     ("prop15", "on"),
     ("prop16", "on"),
     ("prop18", "on"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[6]
        complainant.append(re.sub(r'[^\x00-\x7F]+', '', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[8]
        respondent.append(re.sub(r'[^\x00-\x7F]+', '', respondent1.strip()))
    except:
        pass

    # filling date
    fillingdate = []
    try:
        fillingdate1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[1]
        fillingdate.append(re.sub(r'[^\x00-\x7F]+', '', fillingdate1.strip()))
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        dateOfnextHearing1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[4]
        dateOfnextHearing.append(re.sub(r'[^\x00-\x7F]+', '', dateOfnextHearing1.strip()))
    except:
        pass

    # Case Stage
    casestage = []
    try:
        casestage1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[2]
        casestage.append(re.sub(r'[^\x00-\x7F]+', '', casestage1.strip()))
    except:
        pass

    # CaseNo
    casenoo = []
    try:
        casenoo1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[0]
        casenoo.append(re.sub(r'[^\x00-\x7F]+', '', casenoo1.strip()))
    except:
        pass

    # CaseCategory
    casecategory = []
    try:
        casecategory1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[3]
        casecategory.append(re.sub(r'[^\x00-\x7F]+', '', casecategory1.strip()))
    except:
        pass

    # ResultOfCase
    resultofcase = []
    try:
        result1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[5]
        resultofcase.append(re.sub(r'[^\x00-\x7F]+', '', result1.strip()))
    except:
        pass

    # Advocate Name
    advocatename = []
    try:
        advocatename1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[7]
        advocatename.append(re.sub(r'[^\x00-\x7F]+', '', advocatename1.strip()))
    except:
        pass

    # Advocate Name2
    advocatename2 = []
    try:
        advocatename3 = tree.xpath('//*[@class="maintextborderdata"]/text()')[9]
        advocatename2.append(re.sub(r'[^\x00-\x7F]+', '', advocatename3.strip()))
    except:
        pass

    # Remarks in Filing
    remarks = []
    try:
        remarks1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[10]
        remarks.append(re.sub(r'[^\x00-\x7F]+', '', remarks1.strip()))
    except:
        pass

    additionaldetails1 = tree.xpath('//tr[@id="cond3"]//td[@class="maintextborderdata"]//text()')
    additionaldetails = []
    index = []
    info = []
    details = []
    hearinginfo = []
    dates = []
    dateofhearingadd = []
    dateofnexthearingadd = []
    try:

        for i in range(0, len(additionaldetails1)):
            if additionaldetails1[i].strip() != "":
                additionaldetails.append(additionaldetails1[i].strip())
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                index.append(i)
        index.append(len(additionaldetails))

        for i in range(0, len(index) - 1):
            for j in range(index[i] + 1, index[i + 1]):
                info.append(additionaldetails[j])
            details.append(' '.join(info))
            info = []
        for i in range(0, len(details)):
            if details[i] != "":
                hearinginfo.append(re.sub(r'[^\x00-\x7F]+', ' ', details[i].replace('\n', '').replace('\r', '').replace('&nbsp', '')))
        # DATES INFO
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                dates.append(additionaldetails[i])

        for i in range(0, len(dates)):
            if i % 2 == 0:
                dateofhearingadd.append(dates[i])
            else:
                dateofnexthearingadd.append(dates[i])


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Filing Date'] = fillingdate
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Case No'] = casenoo
        ret_this['Case Category'] = casecategory
        ret_this['Advocate Name'] = advocatename
        ret_this['Advocate Name.'] = advocatename2
        ret_this['Remarks in Filing'] = remarks
        ret_this['Result Of The Case'] = resultofcase
        ret_this['Additional Hearing Info'] = {}
        ret_this['Additional Hearing Info']['Date Of Hearing'] = dateofhearingadd
        ret_this['Additional Hearing Info']['Date Of Next Hearing'] = dateofnexthearingadd
        ret_this['Additional Hearing Info']['Case Proceedings Entered'] = hearinginfo
    except:
        pass

    result = json.dumps({"Case Status": ret_this})
    print(ftfy.fix_text_encoding(result))





