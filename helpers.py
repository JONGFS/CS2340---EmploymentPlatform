def parse_skills_string(skills_string):
    if '\n' in skills_string:
        skills_list = set(skill.strip().lower() for skill in skills_string.split('\n') if skill.strip())
    elif ',' in skills_string:
        skills_list = set(skill.strip().lower() for skill in skills_string.split(',') if skill.strip())
    else:
        skills_list = set([skills_string.strip().lower()]) if skills_string.strip() else set()
    return skills_list
def is_match(profile, job):
    profile_skills = getattr(profile, 'skills', '') or ''
    user_skills = parse_skills_string(profile_skills)
    job_skills_string = job.skills
    job_skills = parse_skills_string(job_skills_string)
    return bool(user_skills & job_skills)