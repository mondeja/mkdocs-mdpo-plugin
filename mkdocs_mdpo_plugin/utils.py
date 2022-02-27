def readable_float(number):
    if str(number).endswith('.0'):
        number = int(number)
    round_number = str(round(number, 2))
    if len(round_number) != len(str(number)):
        round_number = f'~{round_number}'
    return round_number


def removesuffix(s, suf):
    if suf and s.endswith(suf):
        return s[:-len(suf)]
    return s
