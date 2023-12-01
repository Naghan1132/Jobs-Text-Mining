class Job:
    def __init__(self, title,type,description, salary, location, company, source,date_publication):
        self.title = title
        self.type = type # CDD, CDI etc...
        self.description = description # => details
        self.salary = salary
        self.location = location
        self.company = company
        self.source = source # indeed, apec, etc...
        self.date_publication = date_publication # ???
    
