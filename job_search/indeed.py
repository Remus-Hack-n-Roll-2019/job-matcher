import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time

def extract_job_title_from_result(soup):
  jobs = []
  for div in soup.find_all(name="div", attrs={"class":"row"}):
    for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
      jobs.append(a["title"])
  return(jobs)

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

def extract_summary_from_result(soup):
  summaries = []
  spans = soup.findAll("span", attrs={"class": "summary"})
  for span in spans:
    summaries.append(span.text.strip())
  return(summaries)

def search_by_keyword(keyword, location, limit):
  # url = "https://www.indeed.com.sg/jobs?q=software+engineer&l=Singapore&start=10"
  # &as_phr=b&as_any=c&as_not=d&as_ttl=e&as_cmp=f&as_src=g&sort=&psf=advsrch
  url = "https://www.indeed.com.sg/jobs?as_and=" + keyword.lower().strip().replace(" ", "+") + "&l=" + location.lower().strip() + "&limit=" + str(limit) + "&jt=all&radius=10&fromage=7"
  page = requests.get(url)
  # print(url)
  soup = BeautifulSoup(page.text, "html.parser")
  job_titles = extract_job_title_from_result(soup)
  companies = extract_company_from_result(soup)
  locations = extract_location_from_result(soup)
  salaries = extract_salary_from_result(soup)
  summaries = extract_summary_from_result(soup)
  jobs = []
  for i in range(len(job_titles)):
    job = {}
    job['job_title'] = job_titles[i]
    job['company'] = companies[i]
    job['location'] = locations[i]
    # job['salary'] = salaries[i]
    job['summary'] = summaries[i]
    jobs.append(job)
  if len(jobs) > limit:
      jobs = jobs[:limit]
  return jobs

# jobs = search_by_keyword("data scientist", "Singapore", 10)
# for job in jobs:
#     print(job['company'])
