
"""
Process data for internal requirements
"""
import json
import string
import Functions.Generate_Insights as Insights
import datetime



date = str(datetime.date.today())

with open('Data/%s/M0200_profile_summaries.json' % date,  encoding="UTF-8") as file:
    linkedIn_profiles = json.load(file)

final_result = []

redo_profiles = []

for profile in linkedIn_profiles:

    if "Error scrapping this profile" in profile:
        redo_profiles.append(profile.split("Error scrapping this profile: ")[1])
        continue

    error_detection1 = profile['schools']

    error_detection2 =  profile['work_exp']

    if isinstance(error_detection1, str) or isinstance(error_detection2, str):

        if error_detection1 == 'No education section' and error_detection2 =='No work experience section':
            redo_profiles.append(profile['LinkedIn url'])
            continue

    a = Insights.primary_institution(profile)

    b = Insights.primary_job(profile)

    if b == 'None':
        b = [0,'None']

    if profile['schools'] == 'No schools':
        additional_info = 'None'
    else:
        additional_info =  profile['schools'][3]

    school_analysis = Insights.school_status(profile)

    insight = {
        
        'Name': profile['summary'][0] + ', ' + profile['summary'][1],
        'Languages': profile['languages_spoken'],
        'Primary institution': a,
        'Years of experience': Insights.years_of_exp(profile, a, b[1]),
        'International school?': school_analysis['target'],
        'School country': school_analysis['target_country'],
        'School primary curriculum': school_analysis['target_type'],
        'More Details': school_analysis['type'],
        'Interested in mentoring?' : profile["potential_mentor"],
        'Location': profile['summary'][-1],
        'LinkedIn url': profile["LinkedIn url"],
        'Full info': profile
        
    }

    final_result.append(insight)

with open('Data/%s/M0300_profile_insights.json' %date, 'w', encoding="UTF-8") as file:
    file.write(json.dumps(final_result, ensure_ascii=False))
    file.close()

# For profile that need to be redone.
with open('Data//%s/M0101_search_results.json' %date, 'w', encoding="UTF-8") as file:
    file.write(json.dumps(redo_profiles, ensure_ascii=False))
    file.close()

