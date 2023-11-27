class Customer:
    def __init__(self, c_id: int, password: str, first_name: str, last_name: str, birthday):
        self.c_id = c_id
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday

    def validate_c_id(c_id):
        return True

