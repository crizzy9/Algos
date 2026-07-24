# Coding

```python
# public interface ComplexNumber {
#      // @return true if this ComplexNumber holds a single integer, rather than a nested list.
#      public boolean isInteger();
#
#      // @return the single integer that this ComplexNumber holds, if it holds a single integer
#      // Return null if this ComplexNumber holds a nested list
#      public Integer getInteger();
#
#      // @return the nested list that this ComplexNumber holds, if it holds a nested list
#      // Return empty list if this ComplexNumber holds a single integer
#      public List<ComplexNumber> getList();
#  }

# Example 1: [[1,2], 3, [4,5]]
# sum = 1 * 2 + 2 * 2 + 3 * 1 + 4 * 2 + 5 * 2 = 27

# Example 2: [1,[2,[3]]]
# sum = 1 * 1 + 2 * 2 + 3 * 3 = 14

# def sum_of_complex_numbers(clist: ComplexNumber, level=1, sum=0):
#   for c in clist:
#     if not c.isIngeger():
#       sum += sum_of_complex_numbers(c.getList(), level+1, sum)
#     else:
#       sum += c.getInteger() * level
#
#   return sum

```

# System Design

Job Board System for remote software engineers

Engineers can search, apply for jobs
Java, Python, C++
Companies (employers) can search for candidates in each job, do some filters, sort candidates:
Python yoe >= 5
React yoe >=3

Frontend, Backend, Database

Functional Requirements:
Able to Search for Jobs
Able to Apply for Jobs
Able to create a profile
Companies can post jobs
Companies can search for candidates for a given job
Companies can apply filters and sort for candidates for a given job

Non Functional requirements:
Should be able to scale to 1000s of companies
Support 1m customers

Database

User Table
userId - PK
Password_hash
Email
phoneNumber

Profile
User_id - FK
Type - Enum (Experience, Education, Skill, Certifications,...)
Title
Description
Start Date
End Date

Profile Table
123, Skill, Python, null, 2 years ago, null
123, Skill, Java, null, 5 years ago, null

Company
companyId - PK
companyName

JobPosting
jobId - PK
companyId - FK
jobDescription - String
Qualifications - String
Compensation - String

JobPostingRequirements
jobId - FK
skillName - (python, etc)
Yoe - 5 yrs

skillName (Python)
Jobs - []
Years of Experience - 1
Jobs-[]
YOE - 2

JobApplications
applicationId - PK
jobId - FK
companyId - FK
userId - FK

Apartment Rental System

Users
Office space rental for companies
Short term rentals (1-3 months) (People who travel for jobs like nurses, etc)
Luxury Rentals (Short Term + Long Term)

Persona:
People who travel for jobs
Nurses
Lawyers
Doctors
Engineers
Bankers
Consulting
Diplomatic Travel
People inbetween jobs - Working in multiple cities
People with low income (?)
MVP vs Long term product

2 month timeline

A set of cities that we launch in (San Jose, Los Angeles, San Diego)
A set of starting apartments - 15 in each city - 45 apartments

KYC - Know your customer
Browsing Platform - Allows browsing of apartments in a given area
Filter by cost, area, time period
Apartment Booking
Lease Generation - Signed by the user
Payment System - Monthly, LumpSum, etc
Support System - Maintenance Support, Emergency Support
Parking
Pets

Long Term

Support 50 cities
Have atleast 100 apartments in 1 city
Updating browsing platform - Recommendations
Update Apartment Booking - AirBnB style bookings
More Payment Options - Weekly/Monthly Installment
Better Support System with AI
Just Parking Rentals

Platform (Web vs Mobile)
Mobile first

Supply vs Demand
Focus on Supply - Allow People to add their own apartments with us managing billing, maintenance etc
Get Demand via marketing

Sales points
1-3 month rental
Parking rentals
Fully managed rentals
Fully Furnished rentals

Success metrics
Number of Monthly Active Users
Number of Current Rentals
Low Empty Apartments
Total number of Apartments
Number of Cities/Countries
Total Revenue / Profit
Low Insurance Claims
