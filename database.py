import datetime

class Customer:
    def __init__(self, c_id: int, password: str, first_name: str, last_name: str, birthday: str):
        self.c_id = c_id
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday

    # def to_string(c_id, password, first_name, last_name, birthday)
    #     print(f'')

def validate_birthday(birthday):
        
    try:
        year, month, day = birthday.split('-')
        
        if len(month) != 2 or len(day) != 2:
            return False

        birthday = datetime.date(int(year), int(month), int(day))
    except ValueError:
        return False
    return True