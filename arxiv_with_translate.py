# coding=utf-8
import os,time
from selenium import webdriver
from tools import *
from mail import Email

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
        time.sleep(30)
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
            print(i,paper['title'])
            paper_url = paper['url']
            driver.get(paper_url)

            try:
                abstract = driver.find_element_by_css_selector('#abs > div.leftcolumn > blockquote').text
            except:
                print(paper_url)
                driver.get(paper_url)
                time.sleep(30)
                abstract = driver.find_element_by_css_selector('#abs > div.leftcolumn > blockquote').text

            abstract.replace('\t',' ')
            paper['abstract'] = abstract
            if trans2zh_CN:
                print('translating abstract...')
                try:
                    abstract_CN = translate_google(abstract, cn_host=False)
                    # abstract_CN = translate(abstract)
                    abstract_CN.replace('\t','')
                    paper['abstract_zh_CN'] = abstract_CN
                except:
                    paper['abstract_zh_CN'] = ''

                # translate title
                print('translating title...')
                try:
                    title_CN = translate_google(paper['title'], cn_host=False)
                    # title_CN = translate(paper['title'])
                    paper['title_CN'] = title_CN
                except:
                    paper['title_CN'] = ''

    return recent_papers

def write_recent_papers2file(recent_papers,save_file='./save.txt', abstract=True,trans2zh_CN=False,days_to_get=1):
    finall_string = ''
    domains = list(recent_papers.keys())
    #finall_string += ('##############################\n')
    finall_string += (' arXiv papers updated in the past {} day(s)\n'.format(days_to_get))
    finall_string += (' {}\n'.format(time.strftime("%Y.%m.%d", time.localtime())))
    finall_string += (' Domains:{}\n'.format(domains))
    finall_string += ('###############################\n')
    for domain in domains:
        print('saving {}...'.format(domain))
        finall_string += ('Papers in [{}]:\n'.format(domain))
        papers = recent_papers[domain]
        for i,paper in enumerate(papers):
            finall_string += ('【{}】{}\n\n'.format(i, paper['title']))
            if trans2zh_CN:
                finall_string += '{}\n'.format(paper['title_CN'])
            finall_string += ('日期：{}\n'.format(paper['date']))
            finall_string += ('作者：{}\n'.format(paper['authors']))
            if abstract:
                finall_string += ('摘要：\n{}\n\n'.format(paper['abstract']))
                if trans2zh_CN:
                    finall_string += ('摘要：\n{}\n\n'.format(paper['abstract_zh_CN']))
            finall_string += ('arXiv:{}\n'.format(paper['url']))

    file = open(save_file,'w',encoding='utf-8')
    file.write(finall_string)
    print('saving done.')

def edit_recent_papers2mail(recent_papers,save_file='./save2mail.txt', abstract=True,trans2zh_CN=False,days_to_get=1):
    finall_string = ''
    domains = list(recent_papers.keys())
    date = time.strftime("%m.%d", time.localtime())
    # finall_string += ('##############################\n')
    finall_string += (' [{}]计算机视觉/人工智能方向论文速递\n'.format(date))
    # finall_string += (' {}\n'.format(time.strftime("%Y.%m.%d", time.localtime())))
    # finall_string += (' {}\n'.format(time.strftime("%Y.%m.%d", time.localtime())))
    finall_string += ('翻译：谷歌翻译\n')
    # finall_string += (' 论文方向:{}\n'.format(domains))
    # finall_string += ('----------------------------------------------\n')
    for domain in domains:
        print('processing {}...'.format(domain))
        papers = recent_papers[domain]
        finall_string += ('{} 方向，共计{}篇\n'.format(domain, len(papers)))
    
    for domain in domains:
        papers = recent_papers[domain]
        finall_string += ('\n[{}]：\n'.format(domain, len(papers)))

        for i,paper in enumerate(papers):
            finall_string += ('【{}】{}\n'.format(i+1, paper['title']))
            if trans2zh_CN:
                finall_string += '{}\n'.format(paper['title_CN'])

    finall_string += ('\n--------------------------------------------\n')
    finall_string += ('论文摘要等详细信息:\n')
    for domain in domains:
        print('processing {}...'.format(domain))

        papers = recent_papers[domain]
        finall_string += ('{} 方向，共计{}篇：\n'.format(domain, len(papers)))

        for i,paper in enumerate(papers):
            finall_string += ('【{}】{}\n'.format(i+1, paper['title']))
            if trans2zh_CN:
                finall_string += '{}\n'.format(paper['title_CN'])
            # finall_string += ('日期：{}\n'.format(paper['date']))
            finall_string += ('作者：{}\n'.format(paper['authors']))
            if abstract:
                finall_string += ('摘要：{}\n'.format(paper['abstract']))
                if trans2zh_CN:
                    finall_string += ('摘要：{}\n'.format(paper['abstract_zh_CN']))
            
            finall_string += ('arXiv:{}\n'.format(paper['url']))
            finall_string += ('--------------------------------------------\n')

    file = open(save_file,'w',encoding='utf-8')
    file.write(finall_string)
    print('saving done.')

    return finall_string




if __name__ == '__main__':
    while(1):
        date = time.strftime("%m.%d", time.localtime())
        ret = False
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            driver = webdriver.Chrome('C:\ProgramData\Anaconda3\Scripts\chromedriver.exe', options=options)

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
            driver.quit()

            # save to file
            current_date_time = time.strftime("%Y_%m_%d_%Hh%mmin", time.localtime())
            if not os.path.exists('./papers'):
                os.makedirs('./papers')
            save_file = './papers/recent_arxiv_papers_{}.txt'.format(current_date_time)
            write_recent_papers2file(recent_papers, save_file=save_file, abstract=abstract,trans2zh_CN=trans2zh_CN, days_to_get=days_to_get)
            
            # Email to me everyday
            paper_info = edit_recent_papers2mail(recent_papers, abstract=abstract,trans2zh_CN=trans2zh_CN, days_to_get=days_to_get)    
            qq_email = Email('@qq.com','jevcecdnbwzlbfah')
            qq_email.send_mail('@163.com',mail_subject='Arxiv每日论文速递',mail_content=paper_info)
            qq_email.send_mail('@.com',mail_subject='Arxiv每日论文速递',mail_content=paper_info)

            print('{} all done'.format(date))
            ret = True
        except:
            ret = False
            time.sleep(30)
        
        if ret == True:
            time.sleep(86400)
            ret = False




