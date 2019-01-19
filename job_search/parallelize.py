import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time
from gevent.pool import Pool
from gevent import monkey; monkey.patch_all() # patches stdlib
import sys
import logging
from http.client import HTTPSConnection
from timeit import default_timer as timer
info = logging.getLogger().info

def connect(hostname):
    info("connecting %s", hostname)
    h = HTTPSConnection(hostname, timeout=2)
    try: h.connect()
    except(IOError, e):
        info("error %s reason: %s", hostname, e)
    else:
        info("done %s", hostname)
    finally:
        h.close()

def extract_job_title_from_result(soup):
  job_titles = []
  job_links = []
  for div in soup.find_all(name="div", attrs={"class":"row"}):
    for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
      job_titles.append(a["title"])
      job_links.append("https://www.indeed.com.sg" + a["href"])
  return job_titles, job_links

def extract_company_from_result(soup):
  companies = []
  for div in soup.find_all(name="div", attrs={"class":"row"}):
    company = div.find_all(name="span", attrs={"class":"company"})
    if len(company) > 0:
      for b in company:
        companies.append(b.text.strip())
    else:
      sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
      for span in sec_try:
        companies.append(span.text.strip())
  return(companies)

def extract_location_from_result(soup):
  locations = []
  spans = soup.findAll(attrs={"class": "location"})
  for span in spans:
    locations.append(span.text)
  return(locations)

def extract_salary_from_result(soup):
  salaries = []
  for div in soup.find_all(name="div", attrs={"class":"row"}):
    try:
      salaries.append(div.find("nobr").text)
    except:
      try:
        div_two = div.find(name="div", attrs={"class":"sjcl"})
        div_three = div_two.find("div")
        salaries.append(div_three.text.strip())
      except:
        salaries.append("Not available")
  return(salaries)

def search_indeed_jobs(keyword):
  location = "singapore"
  limit = 10
  # url = "https://www.indeed.com.sg/jobs?q=software+engineer&l=Singapore&start=10"
  # &as_phr=b&as_any=c&as_not=d&as_ttl=e&as_cmp=f&as_src=g&sort=&psf=advsrch
  url = "https://www.indeed.com.sg/jobs?as_and=" + keyword.lower().strip().replace(" ", "+") + "&l=" + location.lower().strip() + "&limit=" + str(limit) + "&jt=all&radius=10&fromage=7"
  page = requests.get(url)
  # print(url)
  soup = BeautifulSoup(page.text, "html.parser")
  job_titles, job_links = extract_job_title_from_result(soup)
  companies = extract_company_from_result(soup)
  locations = extract_location_from_result(soup)
  salaries = extract_salary_from_result(soup)
  # summaries = extract_summary_from_result(soup)
  jobs = []
  for i in range(len(job_titles)):
    job = {}
    # job['link'] = job_links[i]
    job['job_title'] = job_titles[i]
    job['company'] = companies[i]
    job['location'] = locations[i]
    # job['salary'] = salaries[i]
    # job['summary'] = get_description_for_given_job_url(job_links[i])
    jobs.append(job)
  if len(jobs) > limit:
      jobs = jobs[:limit]
  return jobs

def parallelize_requests(listOfRequests):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    # info("getting hostname list")
    # hosts_file = sys.argv[1] if len(sys.argv) > 1 else "hosts.txt"
    # hosts_list = open(hosts_file).read().splitlines()
    info("spawning jobs")
    pool = Pool(20) # limit number of concurrent connections
    start = timer()
    listOfResponses = pool.map(search_indeed_jobs, listOfRequests)
    # for _ in pool.imap(search_indeed_jobs, listOfRequests):
    #     pass
    info("%d hosts took us %f seconds", len(listOfRequests), timer() - start)
    return listOfResponses

if __name__=="__main__":
    # listOfRequests = [
    #     "https://www.indeed.com.sg/pagead/clk?mo=r&ad=-6NYlbfkN0AtITCNHI2lDy_Yg9zJSFM-u_EEBOug0_ouqPebedESnHeSHTdnjalfpuS9j-Bar3mz7txtJaE7jVWnwPItW44umfCn2kyCeDO42OIBaIQObmnfwdtaOQ9A5NTt_AKw8c4lGFs7pgo74w50vUvoQBXfVus9co4QwA2O7l4GYZ4lZZfNrcO6DS4szzY8iEkhCyKY9IcgrMSLw954uRGH2z6VrvphiXzRpX-JyHyRP0lMUlXtstYy0mNQBr-i0YK94d2NZv2bAcAzlMNTf-_dKDDf_DeFsDdWvgJKtKTChC5a7-25GDNWjcReRjxm3IVlE2Aazr3JI0H6s5cIhwr30zdkWjRLjAvxKQ9XtVPWWp4V47s59aG_PxGUyEaui6uFoWkNRFjgxaStjL6kefumCASw5VMY_UlQdk9ieCXhTryDysR-XUqGFgGxTxu2cXulvmvflT52jZft2gz_yYLtLWhG-f2Jq7hHoKq7ujPztj4Vc0Cb3_LM6xV5E0-WUfiqvah5e9vGUCIgafhST22m7vBF7ZU9HnJLABou_98uGPfth5ZpZWGhrsy8UUvfTEaXw9kt464s7gNF91ZUaEYIc_bNdJFZonOjRWA=&vjs=3&p=1&sk=&fvj=0",
    #     "https://www.indeed.com.sg/pagead/clk?mo=r&ad=-6NYlbfkN0DP7FivdRNK6lJXpdERgYl7dAxmnUA8p7Vypva9oZxgoOz0E0-VZPp3PNeWGZzi7OjR4HHs3gmu4E8bSd_Fz3Z5eY-RyW8bEHf_v5eqX7F3gexcZgQSejnuVVEvi4ejTZKs3_j4E2r5i3GzI-erAHLuCPIUxiJdw_efFlYKhBFumr-lVtFk4Yp-74pcgcJYcgLdMKsdu7d3nlwPNOlMEcdOhIX6DvNHE0MITa2ttojnWKZ9DrOOlY55mIxCI8BSHX_Q_JJkn24pr1VLkxL8l6x34vmvuJ58J3Bb8xWZapcuM0PodMfdTYP3UKDMv-NphlzRW1umP1-InnkWpGQ98Y-lRQ7MXSV0InbNHS12ixURy_s77pOfnmb4Gu8HUx3hVnB_4A_5zRp9qG-ka7yTZokMY0XKnYqqlPqJUejm8deA4g7kpiGV7CM-60VaEour6jhIWvPfRMHs3hjtFwxYnoUIcd8QqVbaX9htuM4HKFkJGSp7SME_04iWZy2i-h43SDSL3JP59-sbnW9cXTd91z1McKU0vLgKgM60ki5jrEGh6g==&vjs=3&p=2&sk=&fvj=0",
    #     "https://www.indeed.com.sg/pagead/clk?mo=r&ad=-6NYlbfkN0AtITCNHI2lDy_Yg9zJSFM-u_EEBOug0_ouqPebedESnHeSHTdnjalfpuS9j-Bar3mz7txtJaE7jQdqw2JAGvnBM1960zgMqSbzCS4yelZJYbZwKY-uGkQbeCn7XLkgJ9IAo_I6PGKYbsjoeixWS4DuAhDHcumxZ_1tL5O495M_wdRNTon6kyUmdC5MHfrD78qYKQ1buD0_sZfFHneAp5JxdRQWS9Nl9mmBtO-2Tm5Ur6v0BDn2m5LbY9GfB4G29I2V0RuAhb0gGspXOzWLaIynwEya3dx4r3_cQnGsJMKat5P6zdAulpEe-UPNPhr6v0zAyR819Y9NFAvmRvwFJK5eZkqQkDEYRfGspsTvi_fUjrc1zBhWKb2i27trRLqFvVKg4PiKDOTQp-u-vgj6MW3GMscicuLPKbuAtvGkHFG_DGTpn78qOE9mOZ-Ozu3eoFg79PYQj17DUAgE-IaFyo3y_7klFoXfvUnO3lWCkzVz927KtweGfkBJLdAAKJb1SzOxpCVDS5svw7D-oRVwGXtjIB8OuXohMpye6ySMPmOlERfeUtAJH19C-Q8R54QyEMlpG6Kyo9brijLLHmivJBzwSzP8xgeXP217EAaalcXehA==&vjs=3&p=3&sk=&fvj=0",
    #     "https://www.indeed.com.sg/pagead/clk?mo=r&ad=-6NYlbfkN0AtITCNHI2lDy_Yg9zJSFM-u_EEBOug0_ouqPebedESnHeSHTdnjalfpuS9j-Bar3mz7txtJaE7jUNeH07IbdtSzcP6ZEGpcd5Mq-huBua7aqRYecxC05hPUzAmu-BESxSGlXsdflMJKQNXxakeqd0_MSw-B2EU8FqyPl5iAnjO75prUT7KImMLJSxsMvlv6rTbxyQ1llt_mskxmTR3A6IKcJSjbm_U7a8_eOiDzpFEGxS8IOts7u4UfydP9fjmw5tOsGZZUMpuI5n_XFJk4zw0ZQZF6W5Mvvy9f2nb4K0fM5KWnX7lmyAY8hbD9THPLl-CCJNIj0vZVHkFe4BXIyNb0YuO0PLLVKLUw-j7SAnNhu5vX7yl-TbAXvvVTukPuuZCPdzyHFWMWRY3hUlCwD4okLx5R0FkMOILvfdU7S71KUQC4ZzoWDwBuYRAXf_SjRc3d2DBqAV35h5yXyLo6pSM-hZCKWBOR1AZY76XtfgVdvdSfetk7kVy3e3mGCIv1xHS8nL1kHWPwhbLBXUT6-iJDj0oTwcEv6JWb34Mn-IJlD9nPV33YpcKHGnawP2unKQyTppHaUyjN-j9EwFGE1BeTDGChBcgHmhb3nYFX33tPiD6aSOX7-FyRT1g3tBrrImEGK8aW0fzvQTYLoqgGpjP&vjs=3&p=4&sk=&fvj=0",
    #     "https://www.indeed.com.sg/rc/clk?jk=02d5e5e1d47f7365&fccid=2c27a35d679f26ae&vjs=3",
    #     "https://www.indeed.com.sg/rc/clk?jk=5f5afe3afc387b2e&fccid=595d42593839d3a2&vjs=3",
    #     "https://www.indeed.com.sg/rc/clk?jk=2b99d83d95940541&fccid=595d42593839d3a2&vjs=3",
    #     "https://www.indeed.com.sg/rc/clk?jk=22d2d18671660d37&fccid=b02ec3017e811140&vjs=3",
    #     "https://www.indeed.com.sg/rc/clk?jk=8ebf5616a486f07a&fccid=0918a251e6902f97&vjs=3",
    #     "https://www.indeed.com.sg/rc/clk?jk=fa961cb902baa5a0&fccid=de71a49b535e21cb&vjs=3"
    # ]
    listOfRequests = [
        'Deep Learning', 'software engineer', 'test engineer', 'devops engineer', 'mechanical engineer', 'entrepreneur',
        'Deep Learning', 'software engineer', 'test engineer', 'devops engineer'
    ]
    listOfResponses = parallelize_requests(listOfRequests)
    responses = []
    for response in listOfResponses:
        responses.extend(response)
    print(len(responses))
