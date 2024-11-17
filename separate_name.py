import re
# Define patterns
formats = {
    'Other Name': r'(?=,*[a-zA-Z])^[a-zA-Z0-9]+',  # Pattern to capture the name part before digits
    'date_time': r'(?<!\d)(\d{4}[-_.]?\d{2}[-_.]?\d{2})[ -_.](\d{2}[-_.]?\d{2}[-_.]?\d{2})?(?!\d)',
    'App Name': r'(?=,*[a-zA-Z])[a-zA-Z0-9 ]+$',  # Pattern to capture alphanumeric text ending with a letter
    'number': r'(\d{11,}$)|(^\d{11,})'
}


def extract(file_name):
    """Segregates or extra"""
    final_name = {}
    for name, expression in formats.items():
        word = re.search(expression, file_name)
        if word:
            word = word.group()
            # Remove spaces, underscores, and hyphens for date and time
            cleaned_word = re.sub(r'[ _-]', '', word)
            if name == 'App Name':
                if 'WA' in cleaned_word:
                    cleaned_word = 'Whatsapp'
            elif name == 'date_time':
                s = cleaned_word
                if len(s) == 14:  #     YYYY  -   MM   -   DD       H H   :   M  M   :   S  S
                                   #  1234  -   56   -   78       9 10  :   11 12  :   13 14
                    cleaned_word = f'{s[:4]}-{s[4:6]}-{s[6:8]} {s[8:10]}:{s[10:12]}:{s[12:14]}'
                elif len(s) == 8:#    YYYY  -   MM   -   DD
                                   #  1234  -   56   -   78
                    cleaned_word = f'{s[:4]}-{s[4:6]}-{s[6:8]} 00:00:00'
                else:
                    cleaned_word = ''
            if cleaned_word:
                final_name[name] = cleaned_word
    return final_name

