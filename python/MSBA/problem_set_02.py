def print_multiplication_table():
    for i in range(1,13):
        for j in range(1, 13):
            if j == 12:
                print "{:>4}".format(i*j)
            else:
                print "{:>4}".format(i*j),

print_multiplication_table()

def pyramid():
    x = int(raw_input("Put in x: "))
    for n in range(1, x+1):
        print " " * (x-n) + "*" + " *" * (n-1)

pyramid()

def factorial():
    x = int(raw_input("Put in x: "))
    while x <= 0:
        print "Try again. "
        x = int(raw_input("Put in x: "))
    factorial = 1
    for i in range(1, x+1):
        factorial *= i
    print "%s!=%s" % (x, factorial)
    return factorial

factorial()

def fibonacci():
    x = raw_input("Type in x: ")
    y = int(x)
    
    while y < 0 or int(x) != float(x):
        x = raw_input("Try again.\nType in x: ")

    if y <= 2:
        for i in range(0, y):
            print i
    else:
        previous = 0
        current = 1
        next = previous + current
        print previous
        print current
        for i in range(2, y):
            print next
            previous = current
            current = next
            next = previous + current

fibonacci()

def tip_calculator(bill_amt):
    print "Your bill amount is %.2f" % bill_amt
    for tip in [10.00/100, 15.00/100, 20.00/100]:
        print "A %s percent tip: $%.2f totalling $%.2f" % (int(tip*100), bill_amt*tip, bill_amt*(1.00+tip) )
    print "An excellent tip: $%.2f totalling $%.2f" % (bill_amt, bill_amt*2)

bill_amt = round(float(raw_input("Type in bill amount: ")), 2)
tip_calculator(bill_amt)

def is_pythagorean(a, b, c):
    lst = [a, b, c]
    shortest = lst.pop(lst.index(min(lst)))
    second = lst.pop(lst.index(min(lst)))
    longest = lst.pop()
    if shortest**2 + second**2 == longest**2:
        print "IS PYTHAGOREAN"
        return True
    else:
        print "IS NOT PYTHAGOREAN"
        return False

a = float(raw_input("Type in a: "))
b = float(raw_input("Type in b: "))
c = float(raw_input("Type in c: "))
is_pythagorean(a, b, c)

def print_pythagoreans_under_100():
    count = 0
    for a in range(1, int((100**2/2)**0.5)+1):
        for b in range(a, int((100**2 - a**2)**0.5)+1):
            c = (a**2 + b**2)**0.5
            if c == int(c) and c < 100:
                c = int(c)
                print "{:>3}{:>3}{:>3}".format(*[a, b, c]),
                print "---->",
                print "{:>4} + {:>4} = {:>4}".format(*[a**2, b**2, c**2])
                count += 1
    print "total: %s" % count

print_pythagoreans_under_100()

def triangle_classifier():
    a = int(raw_input("Type in a: "))
    b = int(raw_input("Type in b: "))
    c = int(raw_input("Type in c: "))
    while a < 0 or b < 0 or c < 0:
        print "Please enter positive values."
        a = int(raw_input("Type in a: "))
        b = int(raw_input("Type in b: "))
        c = int(raw_input("Type in c: "))
    if a == 0 and b == 0 and c == 0:
        print "STOPPING"
        return False
    sides = [a, b, c]
    shortest = sides.pop(sides.index(min(sides)))
    second = sides.pop(sides.index(min(sides)))
    longest = sides.pop()
    if shortest + second < longest:
        print a, b, c, "NO"
    else:
        print "YES",
        if shortest == longest:
            print "EQUILATERAL",
        if second == longest:
            print "ISOSCELES",
        if shortest + second == longest:
            print "DEGENERATE",
        elif shortest**2 + second**2 == longest**2:
            print "PYTHAGOREAN"
    print "\n"

triangle_classifier()

