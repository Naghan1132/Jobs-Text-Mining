class Job:
    def __init__(self, title,type_job,description, salary,skills,location, company, source,date_publication):
        self.title = title
        self.type_job = type_job # CDD, CDI etc...
        self.description = description # => details
        self.salary = salary
        self.skills = skills
        self.location = location
        self.company = company
        self.source = source # indeed, apec, etc...
        self.date_publication = date_publication # ???
    
