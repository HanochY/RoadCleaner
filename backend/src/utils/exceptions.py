class ObjectNotFoundError(Exception):
    def __init__(self, object_name='Object'):
       self.message = f'{object_name} does not exist!'

class ObjectAlreadyExistsError(Exception):
    def __init__(self, object_name='Object'):
       self.message = f'{object_name} already exists!'

class ObjectEmptyError(Exception):
    def __init__(self, object_name='Object'):
       self.message = f'{object_name} is empty!'

class ObjectUnnamedError(Exception):
    def __init__(self, object_name='Object'):
       self.message = f'{object_name} is unnamed!'
