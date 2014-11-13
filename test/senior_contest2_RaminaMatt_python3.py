#Matthew Ramina
#High Technology HS, Grade 10
#Senior 5
#13-14 Contest 2 "Print Formatting"

#ASSUMPTIONS: this wasn't a very well-defined problem, so i had to assume the following:
#rounding is done with 5 or more on any case
#unless there's a decimal point, i will get an int (behavior is undefined if this isn't true)
#i will not get fields with less characters than digits (except when there's a decimal involved)
#a comma and a decimal will not be together (verified by advisor)

#basically, ACSL should get better at specifying the input
#c.f. https://code.google.com/codejam/contest/189252/dashboard#s=p0 for examples of well-defined problems

import sys

def num_of_ands(form):
    return form.count('&')

def num_of_stars(form, value):
    return num_of_ands(form) - len(str(int(value)))

def normalize_float(s):
    if s.endswith('.0'):
        return s[:-2]
    else:
        return s.replace('.', '')

while True:
    try:
        raw = input('Input: ').replace(' ', '').split(',')
        value = float(raw[-1])
        form = ','.join(raw[:-1])
        dolla_dolla_bill_yall = form.startswith('$')
        insert_dolla_dolla_bill_yall = form.startswith('*$')
        if form.endswith('E'):
            digits = num_of_ands(form)
            str_value = normalize_float(str(value))
            exp = len(normalize_float(str(value))) - 1
            int_part = str(value)[:digits].replace('.', '').ljust(digits, '0')
            if len(str_value) > digits and int(str_value[digits]) >= 5:
                int_part = str(int(int_part) + 1)
                if len(int_part) > digits:
                    int_part = int_part[:-1]
            print(int_part[0] + '.' + int_part[1:] + 'E' + str(exp))
        elif ',' in form:
            if num_of_stars(form, value) >= 0:
                stars = '*'*num_of_stars(form, value) if not dolla_dolla_bill_yall else '$'
                if insert_dolla_dolla_bill_yall:
                    print(stars + "${:,}".format(int(value)))
                else:
                    print(stars + "{:,}".format(int(value)))
            else:
                print('invalid input')
        elif '.' in form:
            int_form, dec_form = tuple(form.split('.'))
            int_len, dec_len = num_of_ands(int_form), num_of_ands(dec_form)
            int_part, dec_part = tuple(str(value).split('.'))
            if int_len >= len(int_part):
                if dec_len > len(dec_part):
                    dec_part = dec_part + '0'*(dec_len - len(dec_part))
                elif dec_len < len(dec_part):
                    real_dec_part = dec_part[:dec_len]
                    if int(dec_part[dec_len]) >= 5:
                        real_dec_part = str(int(real_dec_part) + 1)
                        if len(real_dec_part) > dec_len:
                            real_dec_part = real_dec_part[1:]
                            int_part = str(int(int_part) + 1)
                    dec_part = real_dec_part
                stars = '*'*num_of_stars(int_form, int_part) if not dolla_dolla_bill_yall else '$'
                if insert_dolla_dolla_bill_yall:
                    print(stars + '$' + int_part + '.' + dec_part)
                else:
                    print(stars + int_part + '.' + dec_part)
            else:
                print('invalid input')
        else:
            if num_of_stars(form, value) >= 0:
                stars = '*'*num_of_stars(form, value)
                print(stars + str(round(value)))
            else:
                print('invalid input')
    except (KeyboardInterrupt, EOFError):
        sys.exit(0)
    except:
        print('invalid input or something')
