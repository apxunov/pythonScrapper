import requests
from bs4 import BeautifulSoup as bs

headers = {'accept': '*/*',
           'user-agent': 'unique'}

base_url = 'https://hh.ru/search/vacancy?L_is_autosearch=false&area=1&clusters=true&enable_snippets=true&search_period=30&text=Javascript&page=0'
# base_url = 'https://www.mrporter.com/en-ru/mens/azdesigners'

def hh_parse(base_url, headers):
    jobs = []
    session = requests.session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        # request.content - это ответ в формате html, который мы будем читать второй переменной - html.parser
        soup = bs(request.content, 'html.parser')
        divs = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})
        for div in divs:
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
        print(jobs)
    else:
        print('error')

hh_parse(base_url, headers)
