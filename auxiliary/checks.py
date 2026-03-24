from datetime import datetime

def strIsEmail (strg: str) -> int:
    """Checks whether a string is an email. If so, it returns 0; if not, it returns an error code."""
    isEmail = 0
    dog_poz = strg.find('@', 0, len(strg))
    if (dog_poz != -1) and (strg.find('@', dog_poz+1, len(strg)) == -1):
        namePart = strg[0:dog_poz]
        domenPart = strg[dog_poz+1:]
        if (ord(namePart[0]) == 45) or (ord(namePart[-1]) == 45) or\
            (ord(namePart[0]) == 46) or (ord(namePart[-1]) == 46) or\
            (ord(namePart[0]) == 95) or (ord(namePart[-1]) == 95):
            isEmail = 2
        else:
            for i in range(len(namePart)):
                if (ord(namePart[i]) != 45) and\
                    (ord(namePart[i]) != 46) and\
                    (ord(namePart[i]) != 95) and\
                    (ord(namePart[i]) < 48 or ord(namePart[i]) > 57) and\
                    (ord(namePart[i]) < 97 or ord(namePart[i]) > 122):
                    isEmail = 3
                    break    
        if (ord(domenPart[0]) == 45) or (ord(domenPart[-1]) == 45) or\
            (ord(domenPart[0]) == 46) or (ord(domenPart[-1]) == 46) or\
            (ord(domenPart[0]) == 95) or (ord(domenPart[-1]) == 95):
            isEmail = 4
        else:
            for i in range(len(domenPart)):
                if (ord(domenPart[i]) != 45) and\
                    (ord(domenPart[i]) != 46) and\
                    (ord(domenPart[i]) < 48 or ord(domenPart[i]) > 57) and\
                    (ord(domenPart[i]) < 97 or ord(domenPart[i]) > 122):
                    isEmail = 5
                    break
                else:
                    dot_poz = domenPart.find('.', 0, len(domenPart))
                    if (dot_poz == -1) or (domenPart.find('.', dot_poz+1, len(domenPart)) != -1):
                        isEmail = 6
    else: isEmail = 1
    return(isEmail)

def strIsTel (strg: str) -> int:
    isTel = 0
    if len(strg) != 11:
        isTel = 1
    elif not strg.isdigit():
        isTel = 2

    return(isTel)

def date_normalize(text: str) -> str | None:
    """Converts a string to the format 'DD.MM.YYYY HH:MM'.
       If the month and year are not specified, the function will append the current month and year to the string.
       If the minutes are not specified, the function will append :00 to the string.
       In fact, you could pass the string '24 12' to the function.
       It will recognize that 24 is the 24th of the current month, and 12 is 12:00, and will append the necessary data."""
    tmp = text.split()
    date = tmp[0].split('.')
    time = tmp[1].split(':')
    

    result_date = None
    month = datetime.now().strftime('%m')
    year = datetime.now().strftime('%Y')
    if len(date) == 1:
        tmp[0] = f'{tmp[0]}.{month}.{year}'
    elif len(date) == 2:
        tmp[0] = f'{tmp[0]}.{year}'
    else:
        if len(date[2]) == 2:
            tmp[0] = f'{date[0]}.{date[1]}.20{date[2]}'
    
    if len(time) < 2:
        tmp[1] = f'{time[0]}:00'
    
    result_dt = f'{tmp[0]} {tmp[1]}'

    return result_dt
