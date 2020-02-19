import requests
import csv
from bs4 import BeautifulSoup as bs

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Mobile Safari/537.36'}

base_url = 'https://hh.ru/search/vacancy?L_is_autosearch=false&area=1&clusters=true&enable_snippets=true&search_period=30&text=Node&page=0'

def hh_parse(base_url, headers):
    jobs = []
    urls = []
    urls.append(base_url)

    session = requests.session()
    request = session.get(base_url, headers=headers)

    if request.status_code == 200:
        # request.content - это ответ в формате html, который мы будем читать второй переменной - lxml (шустрее, чем html.parser)
        soup = bs(request.content, 'lxml')

        try:
            pagination = soup.find_all('a', attrs={'data-qa': 'pager-page'})
            countPages = int(pagination[-1].text)
            print(countPages)
            for page in range(countPages):
                url = f'https://hh.ru/search/vacancy?L_is_autosearch=false&area=1&clusters=true&enable_snippets=true&search_period=30&text=Node&page={page}'
                if url not in urls:
                    urls.append(url)
        except:
            pass
        for url in urls:
            request = session.get(url, headers=headers)
            soup = bs(request.content, 'lxml')

            divs = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})
            for div in divs:
                try:
                    title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
                    href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
                    company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
                    responsibility = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
                    requirement = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
                    content = responsibility + ' ' + requirement

                    jobs.append({
                        'title': title,
                        'href': href,
                        'company': company,
                        'content': content
                    })
                except:
                    pass
    else:
        print('error')

    return jobs


def filesWriter(jobs):
    with open('parsed_jobs.csv', 'w') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(('Название вакансии', 'URL', 'Название компании', 'Требования'))
        for job in jobs:
            a_pen.writerow((job['title'], job['href'], job['company'], job['content']))

jobs = hh_parse(base_url, headers)
filesWriter(jobs)
