#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/30 10:11
# @Author  : Smart Porridge
# @File    : get_recent_Arxiv_papers.py
# @Software: PyCharm Community Edition
# @Dsc     : get_recent_Arxiv_papers
#Veision   : 0.1.1 : add USAGE and help info
#Version   : 0.1.0 : creat
"""
USAGE : python get_ArXiv_recent_paper_names.py --domains=cs.CV,cs.AI --keywords=gan,Action
"""
import urllib2
import re
import argparse

def getHtml(url):
    #print url
    page = urllib2.urlopen(url)
    html = page.read()
    return html

def getTotalPaperNums(htmls,TotalPaperNums):
    for html in htmls:
        urllist = re.findall(r'<small>\[ total of (.*?) entries:',html,re.S)
        TotalPaperNums.append(urllist[0])

def getRecentPaperNames(domains,key_words,htmls,recent_papers,recent_papers_include_keywords):
    for i,html in enumerate(htmls):
        paper_list = re.findall(r'<span class="descriptor">Title:</span> (.*?)\n</div>',html,re.S)
        recent_papers[domains[i]] = paper_list

        papers_contain_keywords = []
        for paper in paper_list:
            for key_word in key_words:
                if bool(re.search(key_word,paper,re.IGNORECASE)):
                    papers_contain_keywords.append(paper)
                    break
        recent_papers_include_keywords[domains[i]] = papers_contain_keywords

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--domains', help='ArXiv academic domain, case sensitive (e.g. cs.CV,cs.AI)',default='cs.CV,cs.AI')
    parser.add_argument('--keywords',help='keywords use to search papers,Not cAsE sEnSiTiVe(e.g. gan,3D)',default='gan,Action')
    args = parser.parse_args()

    domains = args.domains.split(',')
    print domains
    #domains = ['cs.CV','cs.AI'] #请区分大小写
    key_words = args.keywords.split(',')
    print key_words
    #key_words = ['action','temporal'] # key_words大小写均可

    # 读取包含最近论文的HTML
    htmls = []
    for domain in domains:
        #htmls.append(getHtml("http://cn.arxiv.org/list/{}/recent".format(domain)))
        #If you can cross the GFW
        htmls.append (getHtml("https://arxiv.org/list/{}/recent".format(domain)))

    #获取最近5天的文章数目
    TotalPaperNums = []
    getTotalPaperNums(htmls,TotalPaperNums)
    #print TotalPaperNums

    #读取包含最近五天论文的HTML
    htmls = []
    for i,domain in enumerate(domains):
        #htmls.append(getHtml("http://cn.arxiv.org/list/{}/pastweek?show={}".format(domain,TotalPaperNums[i])))
        #If you can cross the GFW
        htmls.append(getHtml("https://arxiv.org/list/{}/pastweek?show={}".format(domain, TotalPaperNums[i])))

    #获取最近的论文名字
    recent_papers = {}
    recent_papers_contain_keywords = {}
    getRecentPaperNames(domains, key_words, htmls, recent_papers, recent_papers_contain_keywords)
    #print recent_papers
    for domain in domains:
        print "*******************************************************************************************"
        print "{}: {} papers in recent days.".format(domain,len(recent_papers[domain]))
        print "\t{} papers contain at least one keyworsd in {}, they are:".format(len(recent_papers_contain_keywords[domain]), key_words)
        for i,paper in enumerate(recent_papers_contain_keywords[domain]):
            print "\t\t{}.{}".format(i,paper)
    print "*******************************************************************************************"
