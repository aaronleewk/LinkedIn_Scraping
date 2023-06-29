
from bs4 import BeautifulSoup
import json

#Get data
def personal_details(html):

    soup = BeautifulSoup(html, "lxml")
    to_delete = soup.findAll('span', {'id':'visually-hidden'})
    for each in to_delete:
        each.decompose()

    name_tag = soup.find('h1')
    personal_details = name_tag.parent.parent.parent

    personal_details_separated = personal_details.findChildren(recursive=False)

    name_and_occupation = personal_details_separated[0].findChildren(recursive=False)

    name = name_and_occupation[0].find('h1').text
    occupation = name_and_occupation[1].text

    if personal_details.find('ul'):
        company_and_uni = personal_details_separated[1].findChildren(recursive=False)
        location = personal_details_separated[2].findChildren(recursive=False)

        company = company_and_uni[0].text
        try:
            education = company_and_uni[1].text
        except:
            education = ''
            
        location = location[0].text

        all_details = name + occupation + company + education + location
    else:

        location =  personal_details_separated[1].findChildren(recursive=False)
        location = location[0].text

        all_details = name + occupation + location

    all_details = all_details.split('\n')
    all_details = [each.strip() for each in all_details]
    all_details = list(filter(None, all_details))

    return (all_details)


def languages_list(html):

    soup = BeautifulSoup(html, "lxml")
    to_delete = soup.findAll('span', {'class': 'visually-hidden'})
    for each in to_delete:
        each.decompose()

    try:
        languages_tag = soup.find('div', {'id': 'languages'})

        languages_section = languages_tag.parent

        langList= languages_section.find('ul').get_text()

        str_list = langList.replace('\n', '')

        str_list = str_list.split(' ')

        str_list = list(filter(None, str_list))

        to_remove = ['elementary','limited','full','professional','native', 'or', 'bilingual','working','proficiency']

        all_languages  = [word for word in str_list if word.lower() not in to_remove]    
    except:
        all_languages = 'No languages'

    return all_languages


def education_list(html):
    soup = BeautifulSoup(html, "lxml")
    to_delete = soup.findAll('span', {'class': 'visually-hidden'})


    for each in to_delete:
        each.decompose()

    to_delete = soup.findAll('div', {'class': 'visually-hidden'})

    for each in to_delete:
        each.decompose()

    
    education_tag = soup.find('div', {'id': 'education'})
    

    if str(education_tag) == 'None':
        print('No education section found')
        return 'No education section'
        
    education_section = education_tag.parent
    education_list = education_section.find('ul')


    education_list_separated = education_list.findChildren(
        'li', recursive=False)

    #Get school details
    school_bio = []
    for count, value in enumerate(education_list_separated):
        if value.find('ul'):
            description = value.find('ul')
            school_bio.append(description.text)
            description.decompose()
        else:
            school_bio.append('No description')

        school = value.text
        school_items = school.split('\n')

        school_items = [each.strip() for each in school_items]
        education_list_separated[count] = list(filter(None, school_items))
    
    #Clean up the description section beneath school details
    for count, value in enumerate(school_bio):
        bio_items = value.split('\n')
        bio_items = [each.strip() for each in bio_items]
        school_bio[count] = ' '.join(filter(None, bio_items))

    school_names = []
    school_qualification = []
    school_dates = []

    for each in education_list_separated:
        try:
            school_names.append(each[0])
        except:
            school_names.append('No school name')

        count = 1
        try:
            numbers = [i.isdigit() for i in each[count]]
            if numbers.count(True) > 5:
                raise
            else:
                school_qualification.append(each[count])
                count += 1
        except:
            school_qualification.append('No qualification specification')

        try:
            school_dates.append(each[count])
        except:
            school_dates.append('No school date')

    return [school_names, school_qualification, school_dates, school_bio]


def work_exp_list(html):

    soup = BeautifulSoup(html, "lxml")
    to_delete = soup.findAll('span', {'class': 'visually-hidden'})
    for each in to_delete:
        each.decompose()
    
    to_delete = soup.findAll('div', {'class': 'visually-hidden'})
    for each in to_delete:
        each.decompose()

    experience_tag = soup.find('div', {'id': 'experience'})
    if str(experience_tag) == 'None':
        print('No work experience section found')
        return 'No work experience section'

    experience_section = experience_tag.parent
    experience_list = experience_section.find('ul')
    experience_list_separated = experience_list.findChildren('li', recursive=False)
       
    company_position = []
    company_names = []
    company_dates = []
    other_locations = []

    company_bio = []
    for count, value in enumerate(experience_list_separated):

        if value.find('ul'):
            description = value.find('ul')
            company_bio.append(description.text)
            description.decompose()
        else:
            company_bio.append('No description')

        company = value.text

        try:
            company = company.split('See all')[0]
        except:
            continue
        
        company_items = company.split('\n')
        company_items = [each.strip() for each in company_items]
        experience_list_separated[count] = list(filter(None, company_items))

    #Clean up the description section beneath school details
    for count, value in enumerate(company_bio):
        bio_items = value.split('\n')
        bio_items = [each.strip() for each in bio_items]
        company_bio[count] = ' '.join(filter(None, bio_items))

    for each in experience_list_separated:
        if len(each) > 2:
        
            company_position.append(each[0])
            company_names.append(each[1])
            company_dates.append(each[2])
        else:
            company_position.append('Multiple positions')
            company_names.append(each[0])     
            company_dates.append(each[1])   

        try:
            other_locations.append(each[3])
        except:
            other_locations.append('No location')

    return [company_position, company_names, company_dates, other_locations, company_bio]



















#Comments: No package folder
