# -*- coding=utf-8 -*-
__author__ = 'rocky'
import urllib2, re, os, codecs,sys,datetime
from bs4 import BeautifulSoup
# example https://zhhrb.sinaapp.com/index.php?date=20160610
from mail_template import MailAtt
reload(sys)
sys.setdefaultencoding('utf-8')

def save2file(filename, content):
    filename = filename + ".txt"
    f = codecs.open(filename, 'a', encoding='utf-8')
    f.write(content)
    f.close()


def getPost(date_time, filter_p):
    url = 'https://zhhrb.sinaapp.com/index.php?date=' + date_time
    user_agent = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
    header = {"User-Agent": user_agent}
    req = urllib2.Request(url, headers=header)
    resp = urllib2.urlopen(req)
    content = resp.read()
    p = re.compile('<h2 class="question-title">(.*)</h2></br></a>')
    result = re.findall(p, content)
    count = -1
    row = -1
    for i in result:
        #print i
        return_content = re.findall(filter_p, i)

        if return_content:
            row = count
            break
            #print return_content[0]
        count = count + 1
    #print row
    if row == -1:
        return 0
    link_p = re.compile('<a href="(.*)" target="_blank" rel="nofollow">')
    link_result = re.findall(link_p, content)[row + 1]
    print link_result
    result_req = urllib2.Request(link_result, headers=header)
    result_resp = urllib2.urlopen(result_req)
    #result_content= result_resp.read()
    #print result_content

    bs = BeautifulSoup(result_resp, "html.parser")
    title = bs.title.string.strip()
    #print title
    filename = re.sub('[\/:*?"<>|]', '-', title)
    print filename
    print date_time
    save2file(filename, title)
    save2file(filename, "\n\n\n\n--------------------%s Detail----------------------\n\n" %date_time)

    detail_content = bs.find_all('div', class_='content')

    for i in detail_content:
        #print i
        save2file(filename,"\n\n-------------------------answer  -------------------------\n\n")
        for j in i.strings:

            save2file(filename, j)

    smtp_server = 'smtp.126.com'
    from_mail = sys.argv[1]
    password = sys.argv[2]
    to_mail = 'jinweizsu@kindle.cn'
    #send_kindle = MailAtt(smtp_server, from_mail, password, to_mail)
    #send_kindle.send_txt(filename)


def main():
    sub_folder = os.path.join(os.getcwd(), "content")
    if not os.path.exists(sub_folder):
        os.mkdir(sub_folder)
    os.chdir(sub_folder)


    date_time = '20160611'
    filter_p = re.compile('大误.*')
    ori_day=datetime.date(datetime.date.today().year,01,01)
    t=datetime.date(datetime.date.today().year,datetime.date.today().month,datetime.date.today().day)
    delta=(t-ori_day).days
    print delta
    for i in range(delta):
        day=datetime.date(datetime.date.today().year,01,01)+datetime.timedelta(i)
        getPost(day.strftime("%Y%m%d"),filter_p)
    #getPost(date_time, filter_p)

if __name__ == "__main__":
    main()
