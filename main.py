import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json

keywords = ['Django', 'Flask']
results = []
headers_generator = Headers(os='win', browser='chrome')
response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers=headers_generator.generate())
main_html_data = response.text

main_soup = BeautifulSoup(main_html_data, 'lxml')

vacancy_list = main_soup.find_all(class_='serp-item serp-item_link serp-item-redesign')

for vacancy_tag in vacancy_list:
    vacancy_link_tag = vacancy_tag.find('a', class_='bloko-link')
    vacancy_link = vacancy_link_tag['href']

    response = requests.get(vacancy_link, headers=headers_generator.generate())
    vacancy_html_data = response.text
    vacancy_soup = BeautifulSoup(vacancy_html_data, 'lxml')

    vacancy_city = vacancy_soup.find('p', data='vacancy-view-location')
    vacancy_company = vacancy_soup.find('span', class_='vacancy-company-name').text.strip().replace('\xa0', ' ')
    vacancy_pay = vacancy_soup.find('span', class_='bloko-header-section-2 bloko-header-section-2_lite').text.strip().replace('\xa0', ' ')
    if vacancy_pay == vacancy_company:
        vacancy_pay = 'Не указана'

    vacancy_body = vacancy_soup.find('div', class_='g-user-content').text.strip()
    if any(keyword.lower() in vacancy_body.lower() for keyword in keywords):
        vacancy_info = {
            'link': vacancy_link,
            'company': vacancy_company,
            'city': vacancy_city,
            'pay': vacancy_pay
        }
        results.append(vacancy_info)

    with open('vacancies.json', 'w', encoding='utf-8') as file:
        json.dump(results, file, ensure_ascii=False, indent=4)