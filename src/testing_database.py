# # import pymongo
# # import src.settings as settings
# #
# # client = pymongo.MongoClient(
# #     f"mongodb+srv://{settings.mongo_username}:{settings.mongo_password}@mesohacks.fpga0pp.mongodb.net/?retryWrites=true&w=majority")
# # db = client["MesoHacks"]
# #
# # collection = db['users']
# # collection_jobs = db['jobs']
# #
# # for i in collection_jobs.find({'id': {'$gte': 1, '$lt': 2}}):
# #     print(i)
#
#
# docs = {
#   "company": "Sinai Global",
#   "education": "UG: B.Tech/B.E. - Any Specialization, Diploma - Any Specialization PG:Post Graduation Not Required Doctorate:Doctorate Not Required",
#   "experience": "2 - 4 yrs",
#   "industry": "IT-Software / Software Services",
#   "jobdescription": "Job Description Â  Send me Jobs like this We are looking for a skilled and passionate Full Stack (PHP) Developer. You should have 2+ years of experience working with multiple architectures and coding languages (front-end & back-end technologies). Apply now. Salary:INR 1,75,000 - 2,50,000 P.A Industry: IT-Software / Software Services Functional Area: IT Software - Application Programming , Maintenance Role Category:Programming & Design Role:Graphic/Web Designer Keyskills Web Technologies Web Application Full Stack Application Developer full stack web developer Desired Candidate Profile Please refer to the Job description above Education- UG: B.Tech/B.E. - Any Specialization, Diploma - Any Specialization PG:Post Graduation Not Required Doctorate:Doctorate Not Required Company Profile: Sinai Global Works on IT services related to Logistics Download PPT Photo 1 Â  View Contact Details",
#   "joblocation_address": "Bengaluru",
#   "jobtitle": "Full Stack Web Application (php) Developer",
#   "numberofpositions": "2",
#   "payrate": "1,75,000 - 2,50,000 P.A",
#   "postdate": "2016-10-13 16:20:55 +0000",
#   "skills": "IT Software - Application Programming",
#   "id": 5
# }
#
# experience = docs["experience"].split()
# start, end = experience[0], experience[2]
# print(start)
# print(end)

import requests
import json

r= requests.get('https://13.233.145.108/get-job/4')
print(r.content)
