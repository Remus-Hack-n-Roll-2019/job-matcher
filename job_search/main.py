import json
from job_search.parallelize import *

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

# if __name__=="__main__":
#     strings = [
#         'Deep Learning', 'software engineer', 'test engineer', 'devops engineer', 'mechanical engineer', 'entrepreneur',
#         'Deep Learning', 'software engineer', 'test engineer', 'devops engineer'
#     ]
#     listOfRequests = []
#     for keyword in strings:
#         listOfRequests.append({ "keyword": keyword, "location": "singapore" })
#     start = time.time()
#     jobs = queryJobs(listOfRequests)
#     end = time.time()
#     for job in jobs:
#         print(json.dumps(job, indent=4, sort_keys=True))
#         print("\n")
#     print(end-start)
