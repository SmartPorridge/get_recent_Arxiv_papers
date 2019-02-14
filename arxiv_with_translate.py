# coding=utf-8
import os,time
from selenium import webdriver
from tools import *

def get_arxiv_recent_domain_papers(driver, domains=['cs.CV'], \
                                   trans2zh_CN=False, \
                                   wait_time=10, cn_url=False,\
                                   abstract=True,days_to_get=1
                                   ):
    """get recent 5 days paper"""
    recent_papers = {}
    for domain in domains:
        print('obtain domain {} papers...'.format(domain))
        current_domain_papers = []
        if cn_url:
            current_domain_link = 'http://cn.arxiv.org/list/{}/recent'.format(domain)
        else:
            current_domain_link = 'https://arxiv.org/list/{}/recent'.format(domain)
        print(current_domain_link)
        driver.get(current_domain_link)

        # click "all" button to view recent 5 days' all papers
        time.sleep(1)
        driver.find_element_by_css_selector('#dlpage > small:nth-child(6) > a:nth-child(3)').click()
        time.sleep(wait_time)
        recent_dates = driver.find_elements_by_tag_name('h3') # obtain recent dates
        per_date_paper_blocks = driver.find_elements_by_tag_name('dl') # obtain per date's paper blocks

        # for date_index, date_paper_block in enumerate(per_date_paper_blocks):
        for date_index in range(days_to_get):
            date_paper_block = per_date_paper_blocks[date_index]
            current_date = recent_dates[date_index]
            cur_date_paper_id_list = date_paper_block.find_elements_by_tag_name('dt')
            cur_date_paper_content_list = date_paper_block.find_elements_by_tag_name('dd')
            assert len(cur_date_paper_content_list) == len(cur_date_paper_id_list)
            for i in range(len(cur_date_paper_id_list)):
                if i<len(cur_date_paper_id_list): #1 #test
                    paper = {}
                    paper['date'] = current_date.text
                    paper_id_links = cur_date_paper_id_list[i].find_elements_by_tag_name('a')
                    paper['id'] = paper_id_links[1].text
                    paper['url'] = paper_id_links[1].get_attribute('href')
                    paper['pdf_url'] = paper_id_links[2].get_attribute('href')

                    paper['title'] = cur_date_paper_content_list[i].find_element_by_class_name('list-title').text
                    paper['authors'] = cur_date_paper_content_list[i].find_element_by_class_name('list-authors').text
                    paper['subjects'] = cur_date_paper_content_list[i].find_element_by_class_name('list-subjects').text

                    print(paper['title'])
                    current_domain_papers.append(paper)

        recent_papers[domain] = current_domain_papers
    if abstract:
        recent_papers = get_abstract(driver,recent_papers,domains,trans2zh_CN)
    driver.close()
    return recent_papers

def get_abstract(driver, recent_papers, domains=['cs.CV','cs.AI'], trans2zh_CN=False):
    print('get abstracts...')
    for domain in domains:
        print(domain)
        papers = recent_papers[domain]
        for i,paper in enumerate(papers):
            print(i)
            paper_url = paper['url']
            driver.get(paper_url)
            abstract = driver.find_element_by_css_selector('#abs > div.leftcolumn > blockquote').text
            abstract.replace('\t',' ')
            paper['abstract'] = abstract
            if trans2zh_CN:
                print('translating abstract...')
                abstract_CN = translate_google(abstract)
                # abstract_CN = translate(abstract)
                abstract_CN.replace('\t','')
                paper['abstract_zh_CN'] = abstract_CN
    return recent_papers

def write_recent_papers2file(recent_papers,save_file='./save.txt', abstract=True,trans2zh_CN=False):
    file = open(save_file,'w',encoding='utf-8')
    domains = list(recent_papers.keys())
    file.write('############################################\n')
    file.write('# arXiv papers updated in past 5 days\n')
    file.write('# {}\n'.format(time.strftime("%Y.%m.%d", time.localtime())))
    file.write('# Domains:{}\n'.format(domains))
    file.write('############################################\n')
    for domain in domains:
        print('saving {}...'.format(domain))
        file.write('Papers in [{}]:\n'.format(domain))
        papers = recent_papers[domain]
        for i,paper in enumerate(papers):
            file.write('【{}】{}\n\n'.format(i, paper['title']))
            file.write('{}\n'.format(paper['date']))
            file.write('[作者]:{}\n'.format(paper['authors']))
            if abstract:
                file.write('[摘要]:{}\n\n'.format(paper['abstract']))
                if trans2zh_CN:
                    file.write('[摘要]：{}\n\n'.format(paper['abstract_zh_CN']))

    print('saving done.')





if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome('C:\ProgramData\Anaconda3\Scripts\chromedriver.exe', options=options)

    try_time = 0

    # obtain papers
    domains = ['cs.CV','cs.AI']
    days_to_get = 1 # get how many days' paper only support [1-5]
    cn_url = False # if use CN link i.e http://cn.arxiv.org
    abstract = True
    trans2zh_CN = True # translate abstract
    recent_papers = get_arxiv_recent_domain_papers(driver, domains=domains, \
                                                   trans2zh_CN=trans2zh_CN,\
                                                   wait_time=10,cn_url=cn_url,abstract=abstract,\
                                                   days_to_get=days_to_get)

    # save to file
    current_date_time = time.strftime("%Y_%m_%d_%Hh%mmin", time.localtime())
    save_file = 'recent_arxiv_papers_{}.txt'.format(current_date_time)
    write_recent_papers2file(recent_papers, save_file=save_file, abstract=abstract,trans2zh_CN=trans2zh_CN)
    print('all done')
    driver.quit()

