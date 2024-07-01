import requests
from bs4 import BeautifulSoup
import pandas as pd

# Fungsi untuk mengumpulkan data dari satu halaman
def get_jobs_from_page(page_number):
    url = f'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=as&searchTextText=%22Data+Analyst%22&txtKeywords=%22Data+Analyst%22&txtLocation=&sequence={page_number}&startPage={page_number}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    jobs = []

    # Temukan semua job listing di halaman ini
    job_listings = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

    for job in job_listings:
        title_tag = job.find('h2')
        title_link = title_tag.find('a')
        title = ' '.join(tag.get_text() for tag in title_link.find_all('strong', class_='blkclor'))
        link = title_link['href']  # Ambil atribut href dari tag a

        company = job.find('h3', class_='joblist-comp-name').get_text(strip=True)
        company = company.replace('(More Jobs)', '').strip()

        key_skills = job.find('span', class_='srp-skills').get_text(strip=True)
        key_skills = ' '.join(key_skills.split())

        jobs.append({
            'title': title,
            'company': company,
            'skills': key_skills,
            'link': link
        })

    return jobs

# Fungsi utama untuk mengumpulkan data dari beberapa halaman
def get_all_jobs(pages):
    all_jobs = []
    for page in range(1, pages + 1):
        all_jobs.extend(get_jobs_from_page(page))
    return all_jobs

# Tentukan jumlah halaman yang ingin dikumpulkan
number_of_pages = 20  # Misalnya, 20 halaman
jobs = get_all_jobs(number_of_pages)

# Simpan hasil ke dalam file CSV menggunakan pandas
csv_file = 'DataAnalyst_TimesJobs.csv'

# Membuat DataFrame dari daftar pekerjaan
df = pd.DataFrame(jobs)

# Menyimpan DataFrame ke file CSV
df.to_csv(csv_file, index=False, encoding='utf-8')

print(f"{len(jobs)} jobs have been saved to {csv_file}")
