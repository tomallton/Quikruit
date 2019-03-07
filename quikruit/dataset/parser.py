import json
from pprint import pprint
import pdb
from core.models import QuikruitAccount
from applicants.models import *
from recruiters.models import JobListing
import parsedatetime as pdt
from datetime import datetime
import random
import sys

cal = pdt.Calendar()
job = JobListing.objects.get(title__contains="Full Stack")

sep = '===================================================='

def load():
    with open('dataset/cvDataset.json') as f:
        data = json.load(f)

    _ = input("start")
    while True:
        a = random.choice(data)
        print(a['Name'])
        email = '{}@quikruit.example'.format(a['Name'].replace(' ',''))
        
        account = QuikruitAccount()
        account.email = email
        account.set_password('cs261group25')
        account.is_active = True
        account.save()

        profile = ApplicantProfile()
        profile.account = account
        profile.name = a['Name']
        profile.save()

        sys.stdout.write('\u001b[2J')
        print(sep)

        degree = Degree()
        degree.applicant = profile
        degree.institution = a['University Attended']
        degree.qualification = a['Degree Qualification']
        degree.level_awarded = a['Degree Level']
        print(degree)
        degree.save()

        print(sep)

        for al in a['A-Level Qualifications']:
            alo = ALevel()
            alo.applicant = profile
            alo.subject = al['Subject']
            alo.grade = al['Grade']
            alo.save()
            print(alo)

        print(sep)

        for l in a['Languages Known']:
            try:
                lo = SkillHobby.objects.get(kind=SkillHobby.PROGRAMMING_LANGUAGE, name=l['Language'])
            except SkillHobby.DoesNotExist:
                lo = SkillHobby()
                lo.kind = lo.PROGRAMMING_LANGUAGE
                lo.name = l['Language']
                lo.save()

            lol = SkillHobbyLevel()
            lol.applicant = profile
            lol.skillhobby = lo
            lol.level = l['Expertise']
            lol.save()
            print(lol)

        print(sep)

        for l in a['Skills']:
            try:
                lo = SkillHobby.objects.get(kind=SkillHobby.SKILL, name=l['Skill'])
            except SkillHobby.DoesNotExist:
                lo = SkillHobby()
                lo.kind = lo.SKILL
                lo.name = l['Skill']
                lo.save()

            lol = SkillHobbyLevel()
            lol.applicant = profile
            lol.skillhobby = lo
            lol.level = l['Expertise']
            lol.save()
            print(lol)

        print(sep)

        for l in a['Hobbies']:
            try:
                lo = SkillHobby.objects.get(kind=SkillHobby.HOBBY, name=l['Name'])
            except SkillHobby.DoesNotExist:
                lo = SkillHobby()
                lo.kind = lo.HOBBY
                lo.name = l['Name']
                lo.save()

            lol = SkillHobbyLevel()
            lol.applicant = profile
            lol.skillhobby = lo
            lol.level = l['Interest']
            lol.save()
            print(lol)

        print(sep)

        for pe in a['Previous Employment']:
            peo = PriorEmployment()
            peo.applicant = profile
            peo.company = pe['Company']
            peo.position = pe['Position']
            diff = cal.parseDT(pe['Length of Employment'], sourceTime=datetime.min)[0] - datetime.min
            peo.employment_length = diff
            peo.save()
            print(peo)

        ja = JobApplication()
        ja.job_listing = job
        print(ja.job_listing)
        ja.applicant = profile

        while True:
            selection = input('(g) Good\n(n) Not Good\n(x) Exit\n>> ')
            if selection == 'g':
                ja.status = ja.OFFER_GIVEN
                ja.save()
                break
            elif selection == 'n':
                ja.status = ja.REJECTED
                ja.save()
                break
            else:
                break

        if selection == 'x':
            break;

        # degree = ja.applicant.degree.all()[0]
        # if (
        #     'Computer Science'          in degree.qualification or 
        #     'Mathematics'               in degree.qualification or
        #     'Engineering'               in degree.qualification or
        #     'Physics'                   in degree.qualification
        # ) and ja.applicant.degree.all()[0].level_awarded in ['1st', '2:1']:
        #     ja.status = ja.OFFER_GIVEN
        # else:
        #     ja.status = ja.REJECTED
        # ja.save()
