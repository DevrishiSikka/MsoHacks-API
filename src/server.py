from fastapi import FastAPI, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from .auth import AuthHandler
from .schema import AuthDetails, AdminCreation, InternshipCreation, LoginDetails, ContactMe, ApplyJob, ApplyInternship, \
    UserProfile
import pymongo
import src.settings as settings
import datetime
from twilio.rest import Client
from fastapi.middleware.cors import CORSMiddleware

client = pymongo.MongoClient(
    f"mongodb+srv://{settings.mongo_username}:{settings.mongo_password}@mesohacks.fpga0pp.mongodb.net/?retryWrites=true&w=majority")
app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "13.233.145.108",
    "13.233.145.108:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = client["MesoHacks"]
collection = db['users']
collection_jobs = db['jobs']
collection_internships = db['internships']
collection_message = db['messages']
collection_contact = db['contact']
collection_applied = db['applied']

auth_handler = AuthHandler()

client = Client(settings.account_sid, settings.auth_token)


@app.post('/register', status_code=201)
def register(auth_details: AuthDetails):
    if collection.find_one({'username': auth_details.username}):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    collection.insert_one({
        'username': auth_details.username,
        'password': hashed_password,
        'created_on': datetime.datetime.utcnow(),
        'isAdmin': auth_details.isAdmin,
        'name': auth_details.name,
        'emailId': auth_details.emailId,
        'phone': auth_details.phone,
        'address': auth_details.address,
        'college': auth_details.college,
        'course': auth_details.course,
        'currentYear': auth_details.currentYear
    })
    return


@app.post('/login')
def login(auth_details: LoginDetails):
    if (collection.find_one({'username': auth_details.username}) is None) or (
            not auth_handler.verify_password(auth_details.password,
                                             collection.find_one({'username': auth_details.username})['password'])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(collection.find_one({'username': auth_details.username})['username'])
    admin_val = collection.find_one({'username': auth_details.username})['isAdmin']
    return {'token': token,
            'isAdmin': admin_val}


@app.get('/get-job/{id}')
def get_jobs(id: str):
    answer = []
    for i in collection_jobs.find({"_id": id}):
        answer.append(i)
    return answer


@app.get('/get-jobs/{start}/{end}')
def get_job_list(start: int, end: int):
    answer = []
    for i in collection_jobs.find({'id': {'$gte': start, '$lte': end}}):
        answer.append(i)
    return answer


@app.post('/create-job/', status_code=201)
def create_job(admin_create: AdminCreation):
    if admin_create.isAdmin:
        last_id = 0
        last_document = collection_jobs.find().sort('id', -1).limit(1)
        for i in last_document:
            last_id = i['id']
        data_upload = {"_id": (last_id + 1),
                       "isAdmin": admin_create.isAdmin,
                       "companyName": admin_create,
                       "education": admin_create.education,
                       "experience_start_year": admin_create.experience_start_year,
                       "experience_end_year": admin_create.experience_end_year,
                       "industry": admin_create.industry,
                       "job_description": admin_create.job_description,
                       "job_location": admin_create.job_location,
                       "job_title": admin_create.job_title,
                       "no_of_positions": admin_create.no_of_positions,
                       "payrate": admin_create.payrate,
                       "skills_required": admin_create.skills_required,
                       "company_logo": admin_create.company_logo,
                       "id": (last_id + 1)
                       }
        collection_jobs.insert_one(jsonable_encoder(data_upload))
        return HTTPException(status_code=201, detail="Job listing created")
    return HTTPException(status_code=401, detail="User not admin")


@app.get('/get-intern/{id}')
def get_internships(id: str, protected = Depends(auth_handler.auth_wrapper)):
    answer = []
    for i in collection_internships.find({"_id": id}):
        answer.append(i)
    return answer


@app.get('/get-intern/{start}/{end}')
def get_internship_list(start: int, end: int):
    answer = []
    for i in collection_internships.find({'id': {'$gte': start, '$lte': end}}):
        answer.append(i)
    return answer


@app.post('/create-intern/', status_code=201)
def create_internship(internship_create: InternshipCreation):
    if internship_create.isAdmin:
        last_id = 0
        last_document = collection_internships.find().sort('id', -1).limit(1)
        for i in last_document:
            last_id = i['id']
        data_upload = {"_id": (last_id + 1),
                       "isAdmin": internship_create.isAdmin,
                       "companyName": internship_create.companyName,
                       "internship": internship_create.internship,
                       "company_logo": internship_create.company_logo,
                       "location": internship_create.location,
                       "start_date": internship_create.start_date,
                       "duration": internship_create.duration,
                       "stipend": internship_create.stipend,
                       "apply_by": internship_create.apply_by,
                       "id": (last_id + 1)
                       }
        collection_internships.insert_one(jsonable_encoder(data_upload))
        return HTTPException(status_code=201, detail="Internship listing created")
    return HTTPException(status_code=401, detail="User not admin")


@app.post('/contact-us')
def contact_us(contact: ContactMe):
    last_id = 0
    last_document = collection_message.find().sort('id', -1).limit(1)
    for i in last_document:
        last_id = i['id']
    data_upload = {
        "_id": (last_id + 1),
        "id": (last_id + 1),
        "username": contact.username,
        "mobileNo": contact.mobileNo,
        "message": contact.message,
        "queryTime": datetime.datetime.utcnow()
    }
    collection_message.insert_one(jsonable_encoder(data_upload))
    message = client.messages.create(
        messaging_service_sid='MG99394372cc3b7cffa4ff61000172c878',
        body='Your message has been recorded and we\'ll get back to you soon!',
        to=contact.mobileNo
    )
    return HTTPException(status_code=201, detail="Done!")


@app.post('/apply/jobs')
def apply_for_job(job: ApplyJob):
    last_id = 0
    last_document = collection_applied.find().sort('id', -1).limit(1)
    for i in last_document:
        last_id = i['id']
    data_upload = {
        "_id": (last_id + 1),
        "id": (last_id + 1),
        "username": job.username,
        "jobId": job.Jobid,
        "appliedOn": datetime.datetime.utcnow(),
        "type": "job"
    }
    collection_applied.insert_one(jsonable_encoder(data_upload))
    message = client.messages.create(
        messaging_service_sid='MG99394372cc3b7cffa4ff61000172c878',
        body=f'Hurray!🎉 You have successfully applied for an Internship role at {collection_jobs.find_one({"id": job.Jobid})["company"]}, You\'ll definitely bag the role, keep it up 🥳.',
        to=collection.find_one({"username": job.username})['phone']
    )
    return HTTPException(status_code=201, detail="Done!")


@app.post('/apply/internship')
def apply_for_internship(job: ApplyInternship):
    last_id = 0
    last_document = collection_applied.find().sort('id', -1).limit(1)
    for i in last_document:
        last_id = i['id']
    data_upload = {
        "_id": (last_id + 1),
        "id": (last_id + 1),
        "username": job.username,
        "jobId": job.InternshipId,
        "appliedOn": datetime.datetime.utcnow(),
        "type": "internship"
    }
    collection_applied.insert_one(jsonable_encoder(data_upload))
    message = client.messages.create(
        messaging_service_sid='MG99394372cc3b7cffa4ff61000172c878',
        body=f'Hurray!🎉 You have successfully applied for an Internship role at {collection_internships.find_one({"id": job.InternshipId})["company"]}, You\'ll definitely bag the role, keep it up 🥳.',
        to=collection.find_one({"username": job.username})['phone']
    )
    return HTTPException(status_code=201, detail="Done!")


@app.post('/user/jobs')
def user_profile_get_applied_jobs(user_profile: UserProfile):
    data = []
    for i in collection_applied.find({"type": "job", "username": user_profile.username}):
        data.append(i)
    return data


@app.post('/user/internships')
def user_profile_get_applied_jobs(user_profile: UserProfile):
    data = []
    for i in collection_applied.find({"type": "internship", "username": user_profile.username}):
        data.append(i)
    return data