# Job Matcher

## Inspiration
A lot of university students face difficulties finding the right job for a career. This tool takes in your professional experience and extracts keywords relevant to your previous experience and skill set, which are then matched to online job listings on various job portals.

## Functionality
The current prototype takes in a linkedin generated pdf document summarizing your profile (linkedin resume) as input and parses it to extract keywords such as your top skills and previous job titles. It then runs a keyword matching algorithm against various job listings posted on Indeed (only jobs posted in last 7 days are considered) and ranks the job results according to frequency of occurrence of keywords. This list of job results are displayed in ordered tabular format with a link to the job portal for each job where the candidate may submit their job application!

## Tools and Technologies Used
Front-end: React
Back-end: Flask

## Challenges
- Most of the open-source APIs we initially tried to use for various essential functions (such as converting pdf to text) where found to be broken. So, we had to take the best available option and modify their code to meet our requirement.

- We spent a lot of time trying to setup a LinkedIn authentication service on our app, with the intention that we would be able to scrape information directly from the user's LinkedIn profile upon logging in. However, we ran into several access issues as LinkedIn has recently severely limited access to its full_profile APIs and it also blocks any scrapers from making unauthenticated requests. In the end, we decided to parse resume file directly instead of retrieving the user's LinkedIn profile.

## Accomplishments
- We managed to learn several intricacies of web development and information retrieval.
- We successfully developed a Sign In with LinkedIn option on our web app, which gave us knowledge of how to develop a web login system using login from services like Google, Facebook, etc.

## Additional features
 - Add more custom filters to provide users with more flexibility in only getting job recommendations that match certain criteria (such as job location or job type such as Internship or full time jobs).
- Recommend jobs from more portals other than Indeed, such as Monster or LinkedIn.
- Another challenging improvement would be to use a deep learning technique to match jobs to resumes rather than using the currently implemented keyword matching approach, in order to provide even better recommendations.
