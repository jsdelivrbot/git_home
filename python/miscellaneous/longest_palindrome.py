#!/usr/bin/python3

def find_match(s, index):
    try:

        if s[index] == s[index+1]:
            a, b = index, index + 1

            while a > 0 and b+1 < len(s):
                if s[a-1] != s[b+1]:
                    break

                a -= 1
                b += 1

            s1 = s[a:b+1]

        else:
            s1 = s[index]
    except:
        return s[index] 

    try:
        if s[index] == s[index+2]:
            a, b = index, index + 2

            while a > 0 and b + 1 < len(s):
                if s[a-1] != s[b+1]:

                    break

                a -= 1
                b += 1

            s2 = s[a:b+1]

        else:

            s2 = s[index+1]
    except:
        s2 = s[index+1]

    return s1 if len(s1) >= len(s2) else s2

def find_longest_palindrome(s):

    mid = len(s)//2

    current = ''

    for i in range(mid+1):
        match = find_match(s, mid-i)

        if len(match) > len(current):
            current = match

        if len(current) > 2*(mid-i+1):

            break

    for j in range(mid+1, len(s)):
        match = find_match(s, j)

        if len(match) > len(current):

            current = match

        if len(current) > 2*(len(s)-j):
            break

    return current

def find_longest_palindrome2(s, a, b, known):

    mid = (a + b)//2

    if len(known) > 2*min(mid+1, len(s)-mid+1):
        return known

    current = find_match(s, mid)

    if len(current) > len(known):

        known = current

    l_str = find_longest_palindrome(s, a, mid, known)
    r_str = find_longest_palindrome(s, mid+1, b, known)

    return l_str if len(l_str)>len(r_str) else r_str

if __name__ == '__main__':

    test_cases = ['abcba',\
                  'dabcba',\
                  'dabcbae',\
                  'dabcbauvwxyzzyxwvu']

    for s in test_cases:
        print(find_longest_palindrome(s))
