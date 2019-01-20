import json
import operator
from parallelize import *

def queryJobs(listOfRequests):
    listOfJobSearchResponses = parallelize_requests(search_indeed_jobs, listOfRequests)
    jobs = []
    full_job_links = []
    for response in listOfJobSearchResponses:
        jobs.extend(response)
        for job in response:
            full_job_links.append(job['link'])
    listOfJobDescResponses = parallelize_requests(get_description_for_given_job_url, full_job_links)
    for i in range(len(jobs)):
        jobs[i]['summary'] = listOfJobDescResponses[i]
    return jobs

def matchKeywords(keywords, jobs):
    words = set()
    for phr in keywords:
        for word in phr.strip().split(" "):
            words.add(word.lower())
    words = list(words)
    counts = []
    for job in jobs:
        count = 0
        for word in words:
            if word in job['job_title'].lower() or word in job['summary'].lower():
                count += 1
        counts.append(count)
    res = zip(jobs, counts)
    res.sort(key=operator.itemgetter(1))
    res = res[::-1]
    jobs, _ = zip(*res)
    return jobs

if __name__=="__main__":
    strings = [
        'Deep Learning', 'software engineer', 'test engineer', 'devops engineer', 'mechanical engineer', 'entrepreneur',
        'Deep Learning', 'software engineer', 'test engineer', 'devops engineer'
    ]
    listOfRequests = []
    for keyword in strings:
        listOfRequests.append({ "keyword": keyword, "location": "singapore" })
    start = time.time()
    jobs = queryJobs(listOfRequests)
    end = time.time()
    for job in jobs:
        print(json.dumps(job, indent=4, sort_keys=True))
        print("\n")
    print(end-start)
