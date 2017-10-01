# -*- coding: utf-8 -*-
import hashlib
import random
import binascii

cipher = '5616f5962674d26741d2810600a6c5647620c4e3d2870177f09716b2379012c342d3b584c5672195d653722443f1c39254360007010381b721c741a532b03504d2849382d375c0d6806251a2946335a67365020100f160f17640c6a05583f49645d3b557856221b2'


def my_unpack(string):
    # 'abc' --> '162636'
    ans = ''
    for i in range(len(string)):
        ans += binascii.hexlify(string[i])[::-1]
    return ans


def my_pack(string):
    # '162636' -> abc
    ans = ''
    cnt = 0
    for i in range(0, len(string), 2):
        ans += chr(int(string[i + 1] + string[i], 16))
        cnt += 1
    return ans


def my_pack_arr(string):
    # 162636 -> [97, 98, 99]
    ans = []
    for i in range(0, len(string), 2):
        ans.append(int(string[i + 1] + string[i], 16))
    return ans


def my_encrypt(flg, key):
    # flg, key ---> cipher
    key = hashlib.md5(key).hexdigest()
    msg = flg + '|' + key
    encrypted = chr(random.randint(0, 125))
    for i in range(len(msg)):
        encrypted += chr((ord(msg[i]) + ord(key[i % len(key)]) + ord(encrypted[i])) % 126)
    return my_unpack(encrypted)


def key_decrypt(key, tab, arr):
    key[6] = (arr[70] - ord('|')) % 126
    piv = key[6]
    piv_index = 6
    arr_index = 70

    while key.count('') != 0:
        for i in range(len(tab)):
            if piv_index == tab[i][1]:
                previous = piv_index
                piv_index = tab[i][2]
                arr_index = tab[i][0]
                # print 'key[', piv_index, '] = (arr[', arr_index, '] - key[', previous, ']) % 126'
                key[piv_index] = (arr[arr_index] - key[previous]) % 126
            else:
                pass


def my_decrypt(cipher):
    arr = my_pack_arr(cipher)
    arr.reverse()
    for i in range(len(arr) - 1):
        arr[i] = (arr[i] - arr[i + 1]) % 126
    arr.reverse()
    arr = arr[1:]
    flg = ['' for i in range(70)]
    key = ['' for i in range(32)]
    tab = [[i + 71, i % 32, (i + 7) % 32] for i in range(32)]
    key_decrypt(key, tab, arr)
    for i in range(70):
        flg[i] = chr((arr[i] - key[i % 32]) % 126)
    flg_ans = ''
    for i in range(len(flg)):
        flg_ans += flg[i]
    return flg_ans


if __name__ == '__main__':
    # << Confirmation 1: MD5 value and size >>
    # print 'MD5 VALUE: ', hashlib.md5('').hexdigest()
    # print 'MD5 SIZE: ', len(hashlib.md5('').hexdigest())

    # << Confirmation 2: Correctness of the 'unpack' and 'pack' >>
    # print 'MY_UNPACK('abc'): ', my_unpack('abc')
    # print 'MY_PACK('162636'): ', my_pack('162636')

    # << Confirmation 3: Correctness of the encryption >>
    # print 'MY CIPHER(FLAG='1', KEY='1') ', my_encrypt('1', '1')

    # << Confirmation 4: cipher size and flg size >>
    # print 'CIPHER SIZE: ' len(cipher)  # len(cipher) = 104
    str_1 = ''
    for i in range(100):
        str_1 = ''
        for j in range(i):
            str_1 += '1'
        if len(cipher) == len(my_encrypt(str_1, 'aaaa')):
            # print 'FLAG SIZE: ', len(str_1)  # len(flg) = 70
            break

    # << Confirmation 5: payload of the msg >>
    # print 'cipher(104 chars) = '
    # print 'first encrypted(1 chars) + '
    # print 'md5_hashed key(32 chars) + '
    # print "joint char '|'(1 chars) + "
    # print 'flg(70 chars)'

    # << WRITE UP  >>
    # [1st step]
    # cipher --> packed chipher
    #        --> array divided into 2 chars by 2 chars
    arr = my_pack_arr(cipher)
#    print 'ARRAY1:', arr
    # print len(arr)  # len(arr) = 104

    # [2ed step]
    # arr = [elm, elm, ... , elm]
    # elm = (msg's ascii code) + (key's ascii code cyclically) + (previous elm)
    # elm - (previous elm) = (msg's ascii code) + (key's ascii code cyclically)
    arr.reverse()
    for i in range(len(arr) - 1):
        arr[i] = (arr[i] - arr[i + 1]) % 126
    arr.reverse()
#    print 'ARRAY2:', arr
    arr = arr[1:]  # the first elm is the 'first encrypted(1 chars)'

    # [3rd step]
    key = ['' for i in range(32)]
    flg = ['' for i in range(70)]
    # reference table
    tab = [[i + 71, i % 32, (i + 7) % 32] for i in range(32)]
#    print 'TABLE:', tab
    # key decryption
    key_decrypt(key, tab, arr)
#    print 'KEY:', key
    # flag decryption
    for i in range(70):
        flg[i] = chr((arr[i] - key[i % 32]) % 126)
    ans = ''
    for i in range(len(flg)):
        ans += flg[i]
#    print 'FLAG:', ans

    # my decrypt function
    print my_decrypt(cipher)
