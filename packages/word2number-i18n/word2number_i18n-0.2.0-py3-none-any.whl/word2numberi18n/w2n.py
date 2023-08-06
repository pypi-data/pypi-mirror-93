# SPDX-FileCopyrightText: 2016 - Akshay Nagpal <akshaynagpal@user.noreplay.github.com>
# SPDX-FileCopyrightText: 2020-2021 - Sebastian Ritter <bastie@users.noreply.github.com>
# SPDX-License-Identifier: MIT

import os
import locale
import codecs
import re

# the fallback number system is using of no files can be loaded
number_system_fallback = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'eleven': 11,
    'twelve': 12,
    'thirteen': 13,
    'fourteen': 14,
    'fifteen': 15,
    'sixteen': 16,
    'seventeen': 17,
    'eighteen': 18,
    'nineteen': 19,
    'twenty': 20,
    'thirty': 30,
    'forty': 40,
    'fifty': 50,
    'sixty': 60,
    'seventy': 70,
    'eighty': 80,
    'ninety': 90,
    'hundred': 100,
    'thousand': 1000,
    'million': 1000000,
    'billion': 1000000000,
    'point': '.'
}

#
lang = locale.getlocale()[0]
if "w2n.lang" in os.environ:
    lang = os.environ["w2n.lang"]
if lang is None:
    lang = locale.getdefaultlocale()[0]
if lang is None or lang[0] is None:
    lang = None
    if "LANGUAGE" in os.environ:
        lang = os.environ["LANGUAGE"]
if lang is None:
    lang = "en"  # fallback
lang = lang[:2]

filebased_number_system = {}
data_file = os.path.dirname(__file__)+os.sep+"data"+os.sep+"number_system_"+lang+".txt"
with codecs.open(data_file, "rU", encoding="utf-8") as number_system_data:
    for line in number_system_data:
        if line.startswith('#'):
            pass
        else:
            (key, val) = line.split()
            if "point" != key:
                val = int(val)
            filebased_number_system[key] = val

number_system = filebased_number_system


decimal_words = list(number_system.keys())[:10]


"""
function to form numeric multipliers for million, billion, thousand etc.

input: list of strings
return value: integer
"""


def number_formation(number_words):
    numbers = []
    for number_word in number_words:
        numbers.append(number_system[number_word])
    if lang == "ru":
        if len(numbers) > 3:
            if numbers[0] < 100:
                numbers[0] = numbers[0] * 100

        if len(numbers) == 4:
            return (numbers[0] * numbers[1]) + numbers[2] + numbers[3]
        elif len(numbers) == 3:
            return numbers[0]+numbers[1]+numbers[2]
        elif len(numbers) == 2:
            return numbers[0]+numbers[1]
        else:
            return numbers[0]
    else:
        if len(numbers) == 4:
            return (numbers[0] * numbers[1]) + numbers[2] + numbers[3]
        elif len(numbers) == 3:
            return numbers[0] * numbers[1] + numbers[2]
        elif len(numbers) == 2:
            if 100 in numbers:
                return numbers[0] * numbers[1]
            else:
                return numbers[0] + numbers[1]
        else:
            return numbers[0]


"""
function to convert post decimal digit words to numerial digits
it returns a string to prevert from floating point conversation problem
input: list of strings
output: string
"""


def get_decimal_string(decimal_digit_words):
    decimal_number_str = []
    for dec_word in decimal_digit_words:
        if(dec_word not in decimal_words):
            return 0
        else:
            decimal_number_str.append(number_system[dec_word])
    final_decimal_string = ''.join(map(str, decimal_number_str))
    return final_decimal_string


"""
function to normalize input text
input: string
output: string
"""


def normalize(number_sentence):
    if lang == "fr":
        # do not remove '-' but add minus
        number_sentence = number_sentence.replace('vingt et un', 'vingt-et-un')
        number_sentence = number_sentence.replace('trente et un', 'trente-et-un')
        number_sentence = number_sentence.replace('quarante et un', 'quarante-et-un')
        number_sentence = number_sentence.replace('cinquante et un', 'cinquante-et-un')
        number_sentence = number_sentence.replace('soixante et un', 'soixante-et-un')
    else:
        number_sentence = number_sentence.replace('-', ' ')
    number_sentence = number_sentence.lower()  # converting input to lowercase
    return number_sentence


"""
function to check false redundant input
input: string[]
output: none
raise: if redundant input error
"""


def check_double_input(clean_numbers):
    if lang == "de":
        if clean_numbers.count('tausend') > 1 or clean_numbers.count('million') > 1 or clean_numbers.count('milliarde') > 1 or clean_numbers.count('billion') > 1 or clean_numbers.count('komma') > 1:
            raise ValueError("Redundantes Nummernwort! Bitte gebe ein zulässiges Nummernwort ein (z.B. zwei Millionen Dreiundzwanzigtausend und Neunundvierzig)")
    elif lang == "fr":
        if clean_numbers.count('mille') > 1 or clean_numbers.count('million') > 1 or clean_numbers.count('milliard') > 1 or clean_numbers.count('billion') > 1 or clean_numbers.count('point') > 1:
            raise ValueError("Redundant number word! Please enter a valid number word (eg. two million twenty three thousand and forty nine)")
    elif lang == "hi":
        pass
    elif lang == "pt":
        if clean_numbers.count('mil') > 1 or clean_numbers.count('milhão') > 1 or clean_numbers.count('bilhão') > 1 or clean_numbers.count('point') > 1:
            raise ValueError("Redundant number word! Please enter a valid number word (eg. two million twenty three thousand and forty nine)")
    elif lang == "ru":
        if clean_numbers.count('тысяча') > 1 or clean_numbers.count('миллион') > 1 or clean_numbers.count('миллиард') > 1 or clean_numbers.count('целых') > 1 or clean_numbers.count('целая') > 1:
            raise ValueError("Избыточное числовое слово! Введите правильное числовое слово (например, два миллиона двадцать три тысячи сорок девять)")
    else:  # fallback
        # Error if user enters million,billion, thousand or decimal point twice
        if clean_numbers.count('thousand') > 1 or clean_numbers.count('million') > 1 or clean_numbers.count('billion') > 1 or clean_numbers.count('point') > 1:
            raise ValueError("Redundant number word! Please enter a valid number word (eg. two million twenty three thousand and forty nine)")


"""
function to get billion index
"""


def get_billion_index(clean_numbers):
    if lang == "de":
        billion_index = clean_numbers.index('milliarde') if 'milliarde' in clean_numbers else -1
        if billion_index == -1:
            billion_index = clean_numbers.index('milliarden') if 'milliarden' in clean_numbers else -1
    elif lang == "fr":
        billion_index = clean_numbers.index('milliard') if 'milliard' in clean_numbers else -1
    elif lang == "hi":
        pass
    elif lang == "pt":
        billion_index = clean_numbers.index('bilhão') if 'bilhão' in clean_numbers else -1
    elif lang == "ru":
        billion_index = clean_numbers.index('миллиард') if 'миллиард' in clean_numbers else -1
        if billion_index == -1:
            billion_index = clean_numbers.index('миллиарда') if 'миллиарда' in clean_numbers else -1
    else:  # fallback
        billion_index = clean_numbers.index('billion') if 'billion' in clean_numbers else -1
    return billion_index


"""
function to get million index
"""


def get_million_index(clean_numbers):
    if lang == "de":
        million_index = clean_numbers.index('million') if 'million' in clean_numbers else -1
        if million_index == -1:
            million_index = clean_numbers.index('millionen') if 'millionen' in clean_numbers else -1
    elif lang == "fr":
        million_index = clean_numbers.index('million') if 'million' in clean_numbers else -1
    elif lang == "hi":
        pass
    elif lang == "pt":
        million_index = clean_numbers.index('milhão') if 'milhão' in clean_numbers else -1
    elif lang == "ru":
        million_index = clean_numbers.index('миллион') if 'миллион' in clean_numbers else -1
        if million_index == -1:
            million_index = clean_numbers.index('миллиона') if 'миллиона' in clean_numbers else -1
    else:  # fallback
        million_index = clean_numbers.index('million') if 'million' in clean_numbers else -1
    return million_index


"""
function to get thousand index
"""


def get_thousand_index(clean_numbers):
    if lang == "de":
        thousand_index = clean_numbers.index('tausend') if 'tausend' in clean_numbers else -1
    elif lang == "fr":
        thousand_index = clean_numbers.index('mille') if 'mille' in clean_numbers else -1
    elif lang == "hi":
        pass
    elif lang == "pt":
        thousand_index = clean_numbers.index('mil') if 'mil' in clean_numbers else -1
    elif lang == "ru":
        thousand_index = clean_numbers.index('тысяча') if 'тысяча' in clean_numbers else -1
        if thousand_index == -1:
            thousand_index = clean_numbers.index('тысячи') if 'тысячи' in clean_numbers else -1
    else:  # fallback
        thousand_index = clean_numbers.index('thousand') if 'thousand' in clean_numbers else -1
    return thousand_index


"""
function to return integer for an input `number_sentence` string
input: string
output: int or double or None
"""


def word_to_num(number_sentence):
    if type(number_sentence) is not str:
        raise ValueError("Type of input is not string! Please enter a valid number word (eg. \'two million twenty three thousand and forty nine\')")

    number_sentence = normalize(number_sentence) 

    if(number_sentence.isdigit()):  # return the number if user enters a number string
        return int(number_sentence)

    split_words = re.findall(r'\w+', number_sentence)  # strip extra spaces and comma and than split sentence into words

    clean_numbers = []
    clean_decimal_numbers = []

    # removing and, & etc.
    for word in split_words:
        if word in number_system:
            clean_numbers.append(word)
        elif word == number_system['point']:
            clean_numbers.append(word)

    # Error message if the user enters invalid input!
    if len(clean_numbers) == 0:
        raise ValueError("No valid number words found! Please enter a valid number word (eg. two million twenty three thousand and forty nine)")

    check_double_input(clean_numbers)  # Error if user enters million,billion, thousand or decimal point twice

    # separate decimal part of number (if exists)
    point = filebased_number_system['point']
    point_count = clean_numbers.count(point)
    if point_count == 1:
        clean_decimal_numbers = clean_numbers[clean_numbers.index(point)+1:]
        clean_numbers = clean_numbers[:clean_numbers.index(point)]

    billion_index = get_billion_index(clean_numbers)  # clean_numbers.index('billion') if 'billion' in clean_numbers else -1
    million_index = get_million_index(clean_numbers)  # clean_numbers.index('million') if 'million' in clean_numbers else -1
    thousand_index = get_thousand_index(clean_numbers)  # clean_numbers.index('thousand') if 'thousand' in clean_numbers else -1

    if (thousand_index > -1 and (thousand_index < million_index or thousand_index < billion_index)) or (million_index > -1 and million_index < billion_index):
        raise ValueError("Malformed number! Please enter a valid number word (eg. two million twenty three thousand and forty nine)")

    total_sum = 0  # storing the number to be returned

    if len(clean_numbers) > 0:
        # hack for now, better way TODO
        if len(clean_numbers) == 1:
            total_sum += number_system[clean_numbers[0]]

        else:
            if billion_index > -1:
                billion_multiplier = number_formation(clean_numbers[0:billion_index])
                total_sum += billion_multiplier * 1000000000

            if million_index > -1:
                if billion_index > -1:
                    million_multiplier = number_formation(clean_numbers[billion_index+1:million_index])
                else:
                    million_multiplier = number_formation(clean_numbers[0:million_index])
                total_sum += million_multiplier * 1000000

            if thousand_index > -1:
                if million_index > -1:
                    thousand_multiplier = number_formation(clean_numbers[million_index+1:thousand_index])
                elif billion_index > -1 and million_index == -1:
                    thousand_multiplier = number_formation(clean_numbers[billion_index+1:thousand_index])
                else:
                    thousand_multiplier = number_formation(clean_numbers[0:thousand_index])
                total_sum += thousand_multiplier * 1000

            if thousand_index > -1 and thousand_index != len(clean_numbers)-1:
                hundreds = number_formation(clean_numbers[thousand_index+1:])
            elif million_index > -1 and million_index != len(clean_numbers)-1:
                hundreds = number_formation(clean_numbers[million_index+1:])
            elif billion_index > -1 and billion_index != len(clean_numbers)-1:
                hundreds = number_formation(clean_numbers[billion_index+1:])
            elif thousand_index == -1 and million_index == -1 and billion_index == -1:
                hundreds = number_formation(clean_numbers)
            else:
                hundreds = 0
            total_sum += hundreds

    # adding decimal part to total_sum (if exists)
    if len(clean_decimal_numbers) > 0:
        decimal_sum = get_decimal_string(clean_decimal_numbers)
        decimal_sum = str(total_sum)+"."+str(decimal_sum)
        total_sum = float(decimal_sum)

    return total_sum
