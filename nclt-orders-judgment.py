import requests
from lxml import etree
from io import StringIO
import re
re.compile('<title>(.*)</title>')
import requests.packages
import urllib3
urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()


def natinalcompanylawtribunal(caseno, bench, year):
    bench_code = {}
    bench_code['NEW DELHI BENCH COURT II']  = 1483
    bench_code['NEW DELHI BENCH COURT III'] = 1484
    bench_code['NEW DELHI BENCH COURT IV']  = 33628


    url = "https://nclt.gov.in/case-wise-exposed-filter"
    params = [
     ("advocate_name",	""),
     ("field_case_bench_nid", bench_code[bench]),
     ("field_case_date_value[value][year]", year),
     ("field_case_date_value[value][year]", year),
     ("field_case_date_value[value][year]", year),
     ("field_name_of_petition_value", ""),
     ("field_name_of_respondent_value",	""),
     ("title",	caseno),
    ]

    ########################     MAIN   LINK ###########################################################################
    r = requests.post(url=url, params = params ,verify=False)

    #######################      CHANGING THE URL   ####################################################################
    link = str(r.url).replace('case-wise-exposed-filter', 'case-wise')
    r2 = requests.get(url=link, verify=False)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r2.text), parser)
    #Getting SerialNo. or Number of Cases
    sno1 = []
    try:
        sno = tree.xpath('//*[@class="views-field views-field-counter"]/text()')
        for i  in range(0, len(sno)):
            sno1.append(sno[i].strip())

    except:
        pass

    #Getting Dairy Number and Case
    dairyno1                          = []
    combined_dairynumber_status       = []
    dairyno = tree.xpath('//*[@class="views-field views-field-title"]//text()')
    for i in range(1, len(dairyno)):
        if dairyno[i].strip() != '' and dairyno[i].strip() != 'Order(s) Judgement(s)':
            dairyno1.append(dairyno[i].strip())
    for j in range(0 , len(dairyno1)-1, 2):
        dairy_number = dairyno1[j]
        status       = dairyno1[j+1]
        combined_dairynumber_status.append(dairy_number + ' ' + status)

    #Getting Petioner vs Respondent
    pet_vs_res_1        =[]
    pet_vs_res_advocate = []
    pet_vs_res = tree.xpath('//*[@class="views-field views-field-field-case-advocate"]//text()')
    for i in range(1, len(pet_vs_res)):
        if pet_vs_res[i].strip() != '' :
            pet_vs_res_1.append(pet_vs_res[i].strip().replace('\n', ''))
    for j in range(0 , len(pet_vs_res_1)-1, 2):
        pet_vs_res_name = pet_vs_res_1[j]
        advocate_name       = pet_vs_res_1[j+1]
        pet_vs_res_advocate.append(pet_vs_res_name + ' ' + advocate_name)

    #Getting Listing Date / Court No.
    listing_date_1 =[]
    listing_date_2 =[]
    listing_date = tree.xpath('//*[@class="views-field views-field-field-date-of-orders"]//text()')
    for i in range(1, len(listing_date)):
        listing_date_1.append(listing_date[i].strip())

    for j in range(0, len(listing_date_1)-1):
        if listing_date_1[j] == '' and listing_date_1[j+1] == '':
            listing_date_2.append('')
        elif listing_date_1[j] != '' and listing_date_1[j+1] != '':
            a = listing_date_1[j]
            b = listing_date_1[j+1]
            listing_date_2.append(a + b)


    ############################################ For Orders and Judgments #########################################
    orders_link = []
    orders_judgment = {}
    orders_link_1 = tree.xpath('//*[@class="views-field views-field-title"]/p/a/@href')
    for i in range(0, len(orders_link_1)):
        orders_link.append('https://nclt.gov.in/' + orders_link_1[i])

    ret_this = {}
    order_and_judgment = {}
    try:
        ret_this['Serial Number'] = sno1
        ret_this['Dairy Number/Case Number'] = combined_dairynumber_status
        ret_this['Petioner vs Respondent'] = pet_vs_res_advocate
        ret_this['Listing Date / Court No.'] = listing_date_2
    except:
        pass
    result = {"Orders and Judgments": ret_this}
    print(result)
    for i in range(0, len(orders_link)):
        orders_judgment[orders_link[i]] = order_judgment(orders_link[i])

    order_and_judgment['Orders and Judgments'] = orders_judgment
    order_and_judgment = {"Orders and Judgments": order_and_judgment}
    print(order_and_judgment)




def order_judgment(order_link):
    r3 = requests.get(url=order_link, verify=False)
    parser1 = etree.HTMLParser()
    tree1 = etree.parse(StringIO(r3.text), parser1)

    # Getting SerialNo. or Number of Cases
    sno_order_1 = []
    sno_order = tree1.xpath('//*[@class="views-field views-field-counter"]/text()')
    try:
        for i in range(1, len(sno_order)):
            sno_order_1.append(sno_order[i].strip())

    except:
        pass

    # Case No Judgement(s)
    case_no_1 = []
    case_no = tree1.xpath('//*[@class="views-field views-field-field-interim-order-cp-ca-no-"]/text()')
    try:
        for i in range(1, len(case_no)):
            case_no_1.append(case_no[i].strip())

    except:
        pass

    # Date of Order
    date_order_1 = []
    date_order = tree1.xpath('//*[@class="views-field views-field-field-interim-order-date"]//text()')
    try:
        for i in range(1, len(date_order)):
            if date_order[i].strip() != '':
                date_order_1.append(date_order[i].strip())

    except:
        pass

    # Orders of PDF
    pdf_1 = []
    pdf = tree1.xpath('//*[@class="views-field views-field-field-interim-order-pdf"]/span/a/@href')
    try:
        for i in range(0, len(pdf)):
            if pdf[i].strip() != '':
                pdf_1.append(pdf[i].strip())


    except:
        pass

    return sno_order_1, case_no_1, date_order_1 , pdf_1




if __name__ == "__main__":
    CP_No = str(input("enter case no."))
    Bench = input("enter bench")
    Year = input("enter year")
    natinalcompanylawtribunal(caseno=CP_No, bench=Bench, year=Year)
