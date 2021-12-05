class User:
    def __init__(self, name, surname, subdivision, last_name, tg_id,password,mail):
        self.name = name
        # Фамилия
        self.surname = surname
        # Отчество
        self.last_name = last_name
        # Подразделение
        self.subdivision = subdivision
        self.tg_id = tg_id
        self.password = password
        self.mail = mail
    def __init__(self) -> None:
        pass

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_last_name(self):
        return self.last_name
    def get_mail(self):
        return self.mail

    def set_mail(self,mail):
        self.mail = mail
        
    def set_last_name(self, last_name):
        self.last_name = last_name

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_surname(self):
        return self.surname

    def set_surname(self, surname):
        self.surname = surname

    def get_subdivision(self):
        return self.subdivision

    def set_subdivision(self, subdivision):
        self.subdivision = subdivision

    def __str__(self):
        return f'{self.name}, {self.surname}, {self.subdivision}'
