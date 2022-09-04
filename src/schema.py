from pydantic import BaseModel, EmailStr
from typing import Optional, List


class AuthDetails(BaseModel):
    username: str
    password: str
    isAdmin: Optional[bool] = False
    name: str
    emailId: str
    phone: str
    address: str
    college: str
    course: str
    currentYear: int


class LoginDetails(BaseModel):
    username: str
    password: str
    isAdmin: bool


class AdminCreation(BaseModel):
    isAdmin: bool = False
    companyName: str
    education: str
    experience_start_year: str
    experience_end_year: str
    industry: str
    job_description: str
    job_location: str
    job_title: str
    no_of_positions: str
    payrate: str
    skills_required: str
    company_logo: Optional[str] = "https://i.postimg.cc/47sqnkZf/VPlace1.png"


class InternshipCreation(BaseModel):
    isAdmin: bool = False
    companyName: str
    internship: str
    location: str
    start_date: str
    duration: str
    stipend: str
    apply_by: str
    company_logo: Optional[str] = "https://i.postimg.cc/47sqnkZf/VPlace1.png"


class ContactMe(BaseModel):
    username: str
    name: str
    mobileNo: str
    message: str


class ApplyJob(BaseModel):
    Jobid: int
    username: str


class ApplyInternship(BaseModel):
    InternshipId: int
    username: str


class UserProfile(BaseModel):
    username: str
