initialjamo = {
'b' : 7,
'bb' : 8,
'b̥' : 7,
'c' : 12,
'cc' : 13,
'ch' : 14,
'cʰ' : 14,
'cː' : 13,
'c̥' : 12,
'd' : 3,
'dd' : 4,
'd̥' : 3,
'g' : 0,
'gg' : 1,
'g̊' : 0,
'h' : 18,
'j' : 12,
'jh' : 14,
'jj' : 13,
'k' : 0,
'kh' : 15,
'kk' : 1,
'kʰ' : 15,
'kː' : 1,
'l' : 5,
'm' : 6,
'n' : 2,
'n̟' : 2,
'p' : 7,
'ph' : 17,
'pp' : 8,
'pʰ' : 17,
'pː' : 8,
'r' : 5,
's' : 9,
'ss' : 10,
'sʰ' : 10,
'sː' : 10,
't' : 3,
'tch' : 13,
'th' : 16,
'ts' : 12,
'tsh' : 14,
'tss' : 13,
'tt' : 4,
'tʰ' : 16,
'ɕ' : 9,
'ɾ' : 5,
""""ch'"]""" : 14,
""""ch’"]""" : 14,
""""k'"]""" : 15,
""""k’"]""" : 15,
""""p'"]""" : 17,
""""p’"]""" : 17,
""""t'"]""" : 16,
""""t’"]""" : 16
}

medialjamo = {
    'a' : 0,
    'ae' : 1,
    'ai' : 1,
    'ay' : 1,
    'e' : 5,
    'eo' : 4,
    'eu' : 18,
    'eui' : 19,
    'ey' : 5,
    'i' : 20,
    'ja' : 2,
    'je' : 3,
    'jo' : 12,
    'ju' : 17,
    'jɔ' : 6,
    'jɛ' : 7,
    'o' : 8,
    'oe' : 11,
    'oi' : 11,
    'oy' : 11,
    'u' : 13,
    'ue' : 10,
    'ui' : 19,
    'uy' : 19,
    'uɑ' : 9,
    'uɔ' : 14,
    'uɛ' : 15,
    'wa' : 9,
    'wae' : 10,
    'wai' : 10,
    'way' : 10,
    'we' : 15,
    'weo' : 14,
    'wey' : 15,
    'wi' : 16,
    'wo' : 14,
    'wu' : 13,
    'wä' : 10,
    'wø' : 14,
    'wŏ' : 14,
    'y' : 16,
    'ya' : 2,
    'yae' : 3,
    'yai' : 3,
    'yay' : 3,
    'ye' : 7,
    'yeo' : 6,
    'yey' : 7,
    'yo' : 12,
    'yu' : 17,
    'yä' : 3,
    'yø' : 6,
    'yŏ' : 6,
    'ä' : 1,
    'ö' : 11,
    'ø' : 4,
    'ŏ' : 4,
    'ŭ' : 18,
    'ŭi' : 19,
    'ɑ' : 0,
    'ɔ' : 4,
    'ɛ' : 5,
    'ɨ' : 18,
    'ɨi' : 19,
    'ɯ' : 18,
    'ʉ' : 18,
    'ʉi' : 19
}

finaljamo = {
    'b' : 17,
    'bs' : 18,
    'b̥' : 17,
    'c' : 22,
    'ch' : 23,
    'cʰ' : 23,
    'c̥' : 22,
    'd' : 7,
    'd̥' : 7,
    'g' : 1,
    'gg' : 2,
    'gs' : 3,
    'g̊' : 1,
    'h' : 27,
    'j' : 22,
    'jh' : 23,
    'k' : 1,
    'kh' : 24,
    'kk' : 2,
    'ks' : 3,
    'kʰ' : 24,
    'kː' : 2,
    'l' : 8,
    'lb' : 11,
    'lg' : 9,
    'lh' : 15,
    'lk' : 9,
    'lm' : 10,
    'lp' : 11,
    'lph' : 14,
    'lpʰ' : 14,
    'ls' : 12,
    'lt' : 13,
    'lth' : 13,
    'ltʰ' : 13,
    'm' : 16,
    'n' : 4,
    'nc' : 5,
    'nch' : 6,
    'ncʰ' : 6,
    'ng' : 21,
    'nh' : 6,
    'nj' : 5,
    'nɟ' : 5,
    'n̟' : 4,
    'p' : 17,
    'ph' : 26,
    'ps' : 18,
    'pʰ' : 26,
    'r' : 8,
    's' : 19,
    'ss' : 20,
    'sʰ' : 20,
    'sː' : 20,
    't' : 7,
    'th' : 25,
    'ts' : 22,
    'tsh' : 23,
    'tʰ' : 25,
    'ŋ' : 21,
    'ɕ' : 19,
    'ɾ' : 8,
    """"ch'"]""" : 23,
    """"ch’"]""" : 23,
    """"k'"]""" : 24,
    """"k’"]""" : 24,
    """"p'"]""" : 26,
    """"p’"]""" : 26,
    """"t'"]""" : 25,
    """"t’"]""" : 25
}

other_special = {
    '-':'',
    '\\-':'-',
    '.':'',
    '\\.':'.'
}

def convert(x):
    maxlen = 3
    romanized = x.lower() + " "
    hangul = ""
    jamo_first = -1
    jamo_middle = -1
    jamo_last = -1
    pos = 0
    while pos < len(romanized):
        if jamo_first == -1:
            leng = maxlen
            if (len(romanized) - pos < leng):
                leng = len(romanized) - pos
            while leng > 0 and jamo_first == -1:
                sp = romanized[pos:pos+leng]
                if sp in initialjamo.keys():
                    jamo_first = initialjamo[sp]
                    pos += leng
                leng -= 1
            if jamo_first == -1:
                leng = maxlen
                if len(romanized) - pos < leng:
                    leng = len(romanized) - pos
                while leng > 0 and jamo_middle == -1:
                    sp = romanized[pos:pos+leng]
                    if sp in medialjamo.keys():
                        jamo_middle = medialjamo[sp]
                        pos += leng
                    leng -= 1
                if jamo_middle != -1:
                    jamo_first = 11
            if jamo_first == -1:
                found = False
                leng = maxlen
                if len(romanized) - pos < leng:
                    leng = len(romanized) - pos
                while leng > 0 and not found:
                    sp = romanized[pos:pos+leng]
                    if sp in other_special.keys():
                        hangul += other_special[sp]
                        pos += leng
                        found = True
                    leng -= 1
                if not found:
                    hangul += romanized[pos]
                    pos += 1
        elif jamo_middle == -1:
            leng = maxlen
            if len(romanized) - pos < leng:
                leng = len(romanized) - pos
            while leng > 0 and jamo_middle == -1:
                sp = romanized[pos:pos+leng]
                if sp in medialjamo.keys():
                    jamo_middle = medialjamo[sp]
                    pos += leng
                leng -= 1
            if jamo_middle == -1:
                hangul += romanized[pos-1]
                jamo_first = -1
        else:
            leng = maxlen
            if len(romanized) - pos < leng:
                leng = len(romanized) - pos
            while leng > 0 and jamo_last == -1:
                sp = romanized[pos:pos+leng]
                if sp in finaljamo.keys():
                    jamo_last = finaljamo[sp]
                    pos += leng
                leng -= 1

            sv = jamo_last if jamo_last != -1 else 0
            hangul += chr(jamo_first * 588 + jamo_middle * 28 + 44032 + sv)

            jamo_first = -1
            jamo_middle = -1
            jamo_last = -1
    
    return hangul[:-1]