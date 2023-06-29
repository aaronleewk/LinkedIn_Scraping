

from bs4 import BeautifulSoup
import random
import pandas as pd
import datetime
import itertools

#Data insights
def primary_institution(profile):

    bachelor_keywords = ['Bachelor','bachelor','undergraduate','Undergraduate','2:1',"BS","BSc", 'BA','BFA', 'B.A.','LLB', 'undergrad','Undergrad']

    if profile['schools'] == 'No education section':
        return 'No education section'

    schools = profile['schools'][0]
    
    school_qualification = profile['schools'][1]
   
    list_of_bachelors = list(filter(lambda x: True in [word in x for word in bachelor_keywords], school_qualification))

    #Only 1 bachelor
    if len(list_of_bachelors) == 1:
       
        position = school_qualification.index(list_of_bachelors[0])

        return schools[position]
   
    #print(profile)
    #Multiple bachelors
    periods = profile['schools'][2]

    if len(list_of_bachelors) > 1:
        
        period_in_school = {}

        for each in list_of_bachelors:

            position = school_qualification.index(each)

            period_in_school[periods[position]] = each

        list_of_dates = {}

        for value in list(period_in_school.keys()):
    
            start_and_end = value.split('-')

            if start_and_end == ['No school date']:
                list_of_dates[(0, -1)] =  value

            else:
                
                try:
                    #print(profile)
                    start_and_end_int = [int(each) for each in start_and_end]

                except:

                    for num, each in enumerate(start_and_end):
                        try:

                            int(each)

                            start_and_end[num] = 'filler ' + each
                        except:
                            pass
  
                    if len(start_and_end) > 1:
                        dates = [each.strip().split(' ') for each in start_and_end]
                        
                        start_and_end_int = [int(dates[0][1]),int(dates[1][1])]
                    else:
                        dates = start_and_end[0].strip().split(' ') 

                        start_and_end_int = [int(dates[1]), int(dates[1])]

                list_of_dates[tuple(start_and_end_int)] = value
 
        years_in_school = {}
 
        for each in list(list_of_dates.keys()):  
            
            if len(each) > 1:
    
                if each[1] - each[0] == 0:
                    years_in_school[1] = each

                else:
                    if not each[1] - each[0] < 0:
                        years_in_school[each[1] - each[0]] =  each
            else:
                years_in_school[1] = each[0]

        if bool(years_in_school):
            
            max_value = max(list(years_in_school.keys()))

            start_and_end_int = years_in_school[max_value]
            #print(profile)
            value = list_of_dates[start_and_end_int]
            
            school = period_in_school[value]

            position = school_qualification.index(school)
        
            return schools[position]
            
        else:
            primary_qualification = random.choice(list_of_bachelors)
            position = school_qualification.index(primary_qualification)
            return schools[position]

    #if no bachelor indicator
    uni_keywords = ['university', 'University', 'Universidad', 'universidad', 'M.S.', 'Masters', 'masters', "Master's", "master's", 'Université', 'université', 'phd','PhD','Doctor of Philosophy','M.A.',]

    list_of_unis_by_name = list(filter(lambda x: True in [word in x for word in uni_keywords], schools))

    list_of_unis_by_degree = list(filter(lambda x: True in [word in x for word in uni_keywords], school_qualification))

    for each in list_of_unis_by_degree:

        position = school_qualification.index(each)

        list_of_unis_by_name.append(schools[position])

    list_of_unis = list(set(list_of_unis_by_name))

    if len(list_of_unis) == 1:
        return list_of_unis[0]
    
    if len(list_of_unis) > 1:
        
        try:
            period_in_school = []

            for each in list_of_unis:

                position = schools.index(each)

                dates = periods[position]

                period_in_school.append(dates)

            start_date = []

            for counter, value in enumerate(period_in_school):
            
                if value != 'No school date':
                    start_and_end_str = value.split('-')

                    start = int(start_and_end_str[0])

                    start_date.append(start)
   
            min_value = min(start_date)

            for each in period_in_school:
                if str(min_value) in each:
                    dates = each
        
            position = periods.index(dates)

            earliest_uni= schools[position]

            return earliest_uni

        except:

            return random.choice(schools)

    #if no bachelor and no university
    return random.choice(schools)


def primary_job(profile):

    work_section = profile['work_exp']

    if work_section == 'No work experience section':
        return 'No work experience'

    jobs = work_section[0]

    company = work_section[1]
    dates = work_section[2]
    locations = work_section[3]
    description = work_section[4]

    intern = ['summer','intern','research', 'volunteer']
    internship_keywords = get_variants(intern)
 
    jobs.reverse()

    professional_jobs = []

    for each in jobs:
        if not (True in [word in each for word in internship_keywords]):
            professional_jobs.append(each)

    if len(professional_jobs) > 0:
        job_role = professional_jobs[0]
    else:
        return 'None'
    
    jobs.reverse() 
    
    position = jobs.index(job_role)

    job_company = company[position]

    job_dates = dates[position]

    return [job_company, job_role, job_dates]


def years_of_exp(profile, school, job):

    school_section = profile['schools']

    if job == 'None':
        return 0
    
    if school_section == 'No education section':
        school_list = [['No school name'],['No qualification specification'],['No school date']]
        period = school_list[2]
        position = 0
    else:

        school_list = school_section[0]

        period = profile['schools'][2]

        position = school_list.index(school)

        # if person went to the same uni for both 
        # undergrad and masters, then chances are the Masters
        # degree would be picked up first, e.g.
        '''
        California State University, Northridge
            Master's degree, English Language and Literature/Letters
            2017 - 2019

        California State University, Northridge
            Bachelor of Arts (B.A.), English Language and Literature, General
            2015 - 2017

        '''

    if period[position] == 'No school date':
        if profile['work_exp'] == 'No work experience section' or job == 'None':
            return 'No work experience'

        job_list = profile['work_exp'][0]
        period_work = profile['work_exp'][2]
        
        position = job_list.index(job)

        first_job_dates = period_work[position]

        #first job: 'may 2020'  vs '2020'
        beginning_date = first_job_dates.split('-')[0].split(' ')

        try:
            start = int(beginning_date[1])
        except:
            try:
                start = int(beginning_date[0])
                #print(profile)
            except:
                return "Error in categorisation. Check 'Full info' section"

    else:
        
        if '-' in period[position]:
            primary_school_dates = period[position].split('-')
      
            graduation_dates = primary_school_dates[1].strip()
        else:
            graduation_dates = period[position]

        try:
            #print(profile)
            int(graduation_dates)    #'may 2020' to integer not allowed; but '2020' -> 2020 is allowed
            start = int(graduation_dates)
        except:
            year = graduation_dates.split(' ') #'may 2020' -> ['may', '2020]
            
            start = int(year[1])
    
    this_year = datetime.datetime.now().year
    if start >= this_year:
        years = 0
    else: 
        years = this_year - start
    
    return years


def school_status(profile):

    result = {
        'target': False,
        'target_country': '',
        'target_type': '',
        'type': ''
    }

    british_keywords = ['A-level','A-levels','A-Level', 'A-Levels','A Levels','A levels', 'A Level','A level' 'Grammar School']

    IB_keywords = ['International Baccalaureate','International baccalaureate','international baccalaureate','Higher Level','Higher level','higher level','Standard Level','Standard level','standard level', 'Theory of Knowledge']
    american_keywords = ['American School','American school','american school']
    international_keywords = ['International School of', 'International School', 'British School']
    
    schools = profile['schools'][0]
    schools_qualification = profile['schools'][1]
    schools_bio = profile['schools'][3]
    schools_details = schools_qualification + schools_bio

    int_schools = [] # Custom international school database

    for each in schools_details:

        for word in british_keywords:
            if word in each:
                result['target'] = False
                result['type'] = 'A Levels present in profile' 

        for word in international_keywords:
            if word in each:
                result['target'] = True
                result['type'] = '\"International School\" present in profile'
    
        for word in IB_keywords:
            if word in each:
                result['target'] = True
                result['type'] = 'IB present in profile'

        for word in american_keywords:
            if word in each:
                result['target'] = True
                result['type'] = 'American School present in profile'    
    
        for school in int_schools:
            if school in each:
                result['target'] = True
                result['type'] = 'Internal database school name present in profile'

    for each in schools:

        for int in international_keywords:
            if int in each and result['type']=='':
                result['target'] = True
                result['type'] = '"International School\" present in school name' 

        for school in int_schools:
            if each == school:
                result['target'] = True
                result['type'] = 'Complete match in internal school database' 
                country = df[df['School Name'] == each]['Country'].iloc[0] #becuase there could be duplicate school names and we only want one 
                primary_source = df[df['School Name'] == each]['Primary source'].iloc[0]
                if pd.notna(country):
                    result['target_country'] = country
                if pd.notna(primary_source):
                    result['target_type'] = primary_source

    return result


def interested_mentoring(html):

    soup = BeautifulSoup(html, "lxml")

    interested_edu = False
    education_keywords = ['Mentor','Tutor','Teach','teaching assistant','EdTech','EduTech']
    whole_text = str(soup.find('main', {'id': 'main'}))
    for each in get_variants(education_keywords):
        if each in whole_text:
            interested_edu = True
            break

    return interested_edu


def get_variants(array):
    out = []
    for each in array:
        if len(each.split(' ')) == 1:
            out.append(each.lower())
            out.append(each.title())
        else:
            temp_cont = each.split(' ')
            combinations = list(itertools.product([0, 1], repeat=len(temp_cont)))
            for every in combinations:
                join = ""
                
                for i in range(len(temp_cont)):
                    if every[i]==0:
                        join+=(temp_cont[i].lower()+' ')
                    else:
                        join+=(temp_cont[i].title()+' ')
                out.append(join.strip())
        if each not in out:
            out.append(each)
    counter = 0
    for each in [idx for idx, val in enumerate(out) if val in out[:idx]]:
        del out[each-counter]
        counter+=1

    return out

