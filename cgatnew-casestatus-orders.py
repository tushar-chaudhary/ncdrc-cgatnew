import requests
from lxml import etree
import json
from io import StringIO
from datetime import datetime
from bs4 import BeautifulSoup
import re
import ftfy
re.compile('<title>(.*)</title>')

def cgatnewcasestatus(casetype, caseno, caseyear):
    if casetype == "Cr.CP":
        number="7"
    elif casetype == "C.P.":
        number="4"
    elif casetype == "M.A.":
        number="3"
    elif casetype == "O.A.":
        number="1"
    elif casetype == "P.T.":
        number="5"
    elif casetype == "R.A.":
        number="6"
    else: number="2"

    url = "http://cgatnew.gov.in/catweb/Delhi/services/case_detail_report.php"
    params = [
     ("frmAction",	"add"),
     ("case_number",	""),
     ("filing_no", "11072000000"),
     ("filing_no", "11072000000"),
     ("app_type", "cno"),
     ("case_type",	number),
     ("case_no",	caseno),
     ("case_year",	caseyear),
     ("pet_name",	""),
     ("res_name", ""),
    ]
    r = requests.post(url=url, params = params)
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(r.text), parser)

    # Applicant Name
    applicantname=[]
    try:
        applicantname1 = tree.xpath('//*[@class="textbox"]/@value')[2]
        applicantname.append(re.sub(r'[^\x00-\x7F]+', ' ',applicantname1.replace(' ', '+')))

    except:
        pass

    # Respondent Name
    respondentname = []
    try:
        respondentname1 = tree.xpath('//*[@class="textbox"]/@value')[3]
        respondentname.append(re.sub(r'[^\x00-\x7F]+', ' ',respondentname1.replace(' ', '+')))
    except:
        pass

    # filling Number
    fillingnumber = []
    try:
        hiddenvalues = tree.xpath('//*[@type="hidden"]/@value')
        for i in range(len(hiddenvalues)-2, len(hiddenvalues)):
            fillingnumber.append(re.sub(r'[^\x00-\x7F]+', ' ',hiddenvalues[i]))
    except:
        pass

    #submitting the above values as parameter to other page
    dairynumber = []
    locationnamelocationcode = []
    casenumber = []
    dateoffiling = []
    casestatus = []
    referencecasenumber = []
    subject = []
    listingdate1=[]
    bench=[]
    court=[]
    proccedingdate=[]
    dateofdisposal=[]
    court1=[]
    bench1=[]
    lastactionincourt=[]
    applicant=[]
    applicantadvocate=[]
    respondent =[]
    respondentadvocate=[]
    try:
        url2 = "http://cgatnew.gov.in/catweb/Delhi/services/case_detail_report_action2.php"
        params2 = [
            ("frmAction", "add"),
            ("case_number", ""),
            ("filing_no", fillingnumber[0]),
            ("filing_no", fillingnumber[1]),
            ("app_type", "cno"),
            ("case_type", number),
            ("case_no", caseno),
            ("case_year", caseyear),
            ("pet_name", applicantname),
            ("res_name", respondentname),
        ]
        r1 = requests.post(url=url2, params=params2)
        parser1 = etree.HTMLParser()
        tree1 = etree.parse(StringIO(r1.text), parser1)
        ##################################CASE DETAIL################################################################
        try:
            #DAIRY NUMBER
            details1=tree1.xpath('//table[1]/tr[3]/td[2]/font/text()')
            dairynumber.append(details1[0].strip())

            #LOCATION NAME / LOCATION CODE
            details2 =tree1.xpath('//table[1]/tr[4]/td[2]/font/text()')
            locationnamelocationcode.append(details2[0].strip())

            #CASE NUMBER
            details3 =tree1.xpath('//table[1]/tr[5]/td[2]/font/text()')
            casenumber.append(details3[0].strip())

            #DATE OF FILING.
            details4 =tree1.xpath('//table[1]/tr[6]/td[2]/font/text()')
            dateoffiling.append(details4[0].strip())

            #CASE STATUS
            details5 = tree1.xpath('//table[1]/tr[7]/td[2]/font/text()')
            casestatus.append(details5[0].strip())

            #REFERENCE CASE NUMBER
            details6 = tree1.xpath('//table[1]/tr[8]/td[2]/font/text()')
            referencecasenumber.append( details6[0].strip())

            #SUBJECT
            details7 = tree1.xpath('//table[1]/tr[9]/td[2]/font/text()')
            subject.append(details7[0].strip())
        except:
            pass

        try:
            ##################################################CASE LISTING DETAILS##########################################
            # LISTING DATE
            listingdate1 = tree1.xpath('//table[2]/tr[2]/td[1]/table/tr[1]/td[2]/font/text()')

            # BENCH
            bench = tree1.xpath('//table[2]/tr[2]/td[1]/table/tr[2]/td[2]/font/text()')

            # COURT
            court = tree1.xpath('//table[2]/tr[2]/td[1]/table/tr[3]/td[2]/font/text()')
        except:
            pass


        try:
            ###############################################CASE PROCEEDINGS DETAILS#####################################
            # PROCEEDING DATE
            proccedingdate = tree1.xpath('//table[2]/tr[2]/td[2]/table/tr[1]/td[2]/font/text()')

            # DATE OF DISPOSAL
            dateofdisposal = tree1.xpath('//table[2]/tr[2]/td[2]/table/tr[2]/td[2]/font/text()')

            # COURT
            court1 = tree1.xpath('//table[2]/tr[2]/td[2]/table/tr[3]/td[2]/font/text()')

            # BENCH
            bench1 = tree1.xpath('//table[2]/tr[2]/td[2]/table/tr[4]/td[2]/font/text()')

            # LAST ACTION IN COUURT
            lastactionincourt = tree1.xpath('//table[2]/tr[2]/td[2]/table/tr[5]/td[2]/font/text()')

        except:
            pass

        try:
            ##############################################APPLICANT AND APPLICANT ADVOCATES#############################
            #APPLICANT
            applicant = tree1.xpath('//table[3]/tr[2]/td[2]/font/text()')

            # APPLICANT ADVOCATE
            applicantadvocate = tree1.xpath('//table[3]/td[2]/font/text()')

        except:
            pass

        try:
            #############################################RESPONDENT AND RESPONDENT ADVOCATES############################
            #RESPONDENT NAME
            respondent = tree1.xpath('//table[3]/tr[4]/td[2]/font/text()')

            #RESPONDENT ADVOCATE
            respondentadvocate = tree1.xpath('//table[3]/td[4]/font/text()')
        except:
            pass

    except:
        pass

    ret_this = {}
    try:
        ret_this['Case Details'] = {}
        ret_this['CASE LISTING DETAILS'] = {}
        ret_this['CASE PROCEEDING DETAILS'] = {}
        ret_this['APPLICANT AND APPLICANT ADVOCATES'] = {}
        ret_this['RESPONDENT AND RESPONDENT ADVOCATES']={}
        ret_this['Case Details']['Dairy Number'] = dairynumber
        ret_this['Case Details']['LOCATION NAME / LOCATION CODE'] = locationnamelocationcode
        ret_this['Case Details']['CASE NUMBER'] = casenumber
        ret_this['Case Details']['DATE OF FILING.'] = dateoffiling
        ret_this['Case Details']['CASE STATUS'] = casestatus
        ret_this['Case Details']['REFERENCE CASE NUMBER'] = referencecasenumber
        ret_this['Case Details']['SUBJECT'] = subject
        ret_this['CASE LISTING DETAILS']['LISTING DATES'] = listingdate1
        ret_this['CASE LISTING DETAILS']['BENCH'] = bench
        ret_this['CASE LISTING DETAILS']['COURT'] = court
        ret_this['CASE PROCEEDING DETAILS']['PROCEEDING DATE']= proccedingdate
        ret_this['CASE PROCEEDING DETAILS']['NEXT LISTING DATE / DATE OF DISPOSAL'] = dateofdisposal
        ret_this['CASE PROCEEDING DETAILS']['COURT'] = court1
        ret_this['CASE PROCEEDING DETAILS']['BENCH'] = bench1
        ret_this['CASE PROCEEDING DETAILS']['LAST ACTION IN COURT'] = lastactionincourt
        ret_this['APPLICANT AND APPLICANT ADVOCATES']['APPLICANT'] = applicant
        ret_this['APPLICANT AND APPLICANT ADVOCATES']['APPLICANT ADVOCATE'] = applicantadvocate
        ret_this['RESPONDENT AND RESPONDENT ADVOCATES']['RESPONDENT NAME'] = respondent
        ret_this['RESPONDENT AND RESPONDENT ADVOCATES']['RESPONDENT ADVOCATE'] = respondentadvocate

    except: pass


    result = json.dumps({"Case Status" : ret_this})
    print(ftfy.fix_text_encoding(result))

def cgatneworders(casetype, caseno, caseyear):
    if casetype == "Cr.CP":
        number="7"
    elif casetype == "C.P.":
        number="4"
    elif casetype == "M.A.":
        number="3"
    elif casetype == "O.A.":
        number="1"
    elif casetype == "P.T.":
        number="5"
    elif casetype == "R.A.":
        number="6"
    else: number="2"
    url = "http://cgatnew.gov.in/catweb/Delhi/services/upload_order_detail.php"
    params = [
        ("search_type", "1"),
        ("judge_detail", "0"),
        ("from_date", ""),
        ("to_date", ""),
        ("from_date1", ""),
        ("to_date1", ""),
        ("case_type", number),
        ("case_no", caseno),
        ("case_year", caseyear),
        ("txtState", ""),
        ("filing_no", ""),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    ###########################################Party Detail#############################################
    #ApplicantVSRespondent
    applicantvsrespondent=[]
    try:
        applicantvsrespondent1 = tree.xpath('//table[6]/tr[2]/td/font/text()')
        applicantvsrespondent.append(applicantvsrespondent1[0].strip())
    except:
        pass

    #SerialNumber
    srno=[]
    srno1=tree.xpath('//*[@class="hoverTable"]/tr/td/text()')
    for i in range(0, len(srno1)):
        if srno1[i].strip().isdigit() == True:
            srno.append(srno1[i].strip())

    #CaseNumber
    caseno=[]
    for i in range(4, len(srno)+4):
        caseno1=tree.xpath("//table[6]/tr[{}]/td[2]/text()".format(i))
        caseno.append(caseno1[0].strip())

    #Part Detail
    partydetail=[]
    join=[]
    for i in range(4, len(srno) + 4):
        partydetail1= tree.xpath("//table[6]/tr[{}]/td[3]/text()".format(i))
        join.append(''.join(partydetail1))
        partydetail.append(join[0].strip())
        join=[]

    #Member Name
    membername=[]
    join1=[]
    for i in range(4, len(srno) + 4):
        membername1= tree.xpath("//table[6]/tr[{}]/td[4]/text()".format(i))
        join1.append(''.join(membername1))
        membername.append(join1[0].strip())
        join1=[]


    #Date Of Order
    dateoforder=[]
    join2=[]
    for i in range(4, len(srno) + 4):
        dateoforder1= tree.xpath("//table[6]/tr[{}]/td[5]/text()".format(i))
        join2.append(''.join(dateoforder1))
        dateoforder.append(join2[0].strip())
        join2=[]

    #Remarks
    remarks=[]
    join3=[]
    for i in range(4, len(srno) + 4):
        remarks1 = tree.xpath("//table[6]/tr[{}]/td[6]/text()".format(i))
        join3.append(''.join(remarks1))
        remarks.append(join3[0].strip())
        join3 = []

    #Orders
    join4=[]
    orders_link=[]
    for i in range(4, len(srno) + 4):
        orders1 = tree.xpath("//table[6]/tr[{}]/td[7]/a/@href".format(i))
        join4.append(''.join(orders1))
        orders_link.append("http://cgatnew.gov.in/catweb/Delhi/services/" + join4[0])
        join4=[]

    ret_this = {}
    try:
        ret_this['ApplicantVSRespondent'] = applicantvsrespondent
        ret_this['Sr No'] = srno
        ret_this['PARTY DETAIL'] = partydetail
        ret_this[' Member Name'] = membername
        ret_this['Date of Order'] = dateoforder
        ret_this['Remarks'] = remarks
        ret_this['Orders File'] = orders_link
    except:
        pass

    result = json.dumps({"Orders": ret_this})
    print(ftfy.fix_text_encoding(result))


