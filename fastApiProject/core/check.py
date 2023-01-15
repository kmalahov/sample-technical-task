import re


async def check_login(login):
    if re.search(r'^[a-z\d.]{3,20}$', login):
        return login
    else:
        return None


async def check_email(email):
    if re.search(r'([A-Za-z\d]+[.])*[A-Za-z\d]+@[A-Za-z\d]+(\.[A-Z|a-z]{2,})+', email):
        return email
    else:
        return None


async def check_phone(phone):
    phone = phone.replace('-', '').replace('(', '').replace(')', '')
    if re.search(r'^((\+7)+(\d){10})$', phone):
        return phone
    else:
        return None
