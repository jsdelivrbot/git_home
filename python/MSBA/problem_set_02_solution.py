import sys
#--------------------------------------------------
def print_multiplication_table():
    for x in range(1, 13):
        print
        for y in range(1, 13):
            print '{:>4}'.format(x * y),


print
print
print_multiplication_table()
print
print


#--------------------------------------------------
def pyramid():
    height = int(raw_input("\n\nPlease enter the height of the pyramid: "))
    for row in xrange(1, height+1):
        filler = ((height-row) * 3) * ' '
        sys.stdout.write(filler)
        for col in range(1, row + 1):
            sys.stdout.write('*     ')
        print


pyramid()
print
print
print


#--------------------------------------------------
# Note there are more graceful ways to write this
# but we will address that later.

def factorial():
    while True:
        x = int(raw_input("\n\nFACTORIAL: Please enter a positive number.  Or a negative number to stop. "))

        if x < 0:
            print "STOPPING"
            break
    
        elif x == 0:
            print 1

        else:    
            result = 1
            while x > 0:
                result = result * x
                x = x -1
            print result


factorial()
print
print


#--------------------------------------------------
# Note there are more graceful ways to write this
# but we will address that later.
def fibonacci():
    while True:
        x = int(raw_input("\n\nFIBONACCI: Please enter a positive number.  Zero or a negative number to stop. "))

        if x < 1:
            print "STOPPING"
            return
        else:
            a, b = 0, 1
            counter = 0
            while counter < x:
                print a,
                counter = counter + 1
                a, b = b, a+b

fibonacci()
print
print


#--------------------------------------------------
def tip_calculator(bill_amt):  
    print "Your bill amount is $%.2f" % (round(bill_amt, 2))
    print "A 10 percent tip: $%.2f" % round(bill_amt * 0.10, 2), "totalling $%.2f" % round(bill_amt * 0.10, 2)
    print "A 15 percent tip: $%.2f" % round(bill_amt * 0.15, 2), "totalling $%.2f" % round(bill_amt * 0.15, 2)
    print "A 20 percent tip: $%.2f" % round(bill_amt * 0.20, 2), "totalling $%.2f" % round(bill_amt * 0.20, 2)
    print "An excellent tip: $%.2f" % round(bill_amt, 2), "totalling $%.2f" % round(bill_amt * 2, 2)


while True:
    bill = float(raw_input("\n\nPlease enter your total bill or zero to stop: "))
    if bill <= 0:
        break
    tip_calculator(bill)

print
print


#--------------------------------------------------
def is_pythagorean(a, b, c):
    if a**2 + b**2 == c**2:
        print a, b, c, "IS PYTHAGOREAN"
    print a, b, c, "IS NOT PYTHAGOREAN"
    
print
print
is_pythagorean(3, 4, 6)
is_pythagorean(3, 4, 8)
print
print


#--------------------------------------------------
def print_pythagoreans_under_100():
    counter = 0
    for a in range (1,100):
        for b in range (a+1,100):
            for c in range (1, 100):
                    if a**2 + b**2 == c**2:
                        counter = counter + 1
                        print "{:>2} {:>2} {:>2} ----> {:>4} + {:>4} = {:>4}".format(a, b, c, a**2, b**2, c**2)


print
print
print
print
print_pythagoreans_under_100()
print
print
print
print


#--------------------------------------------------
def identify_triangle():
    while True:
        a = int(raw_input("\n\nPlease enter side a: "))
        b = int(raw_input("Please enter side b: "))
        c = int(raw_input("Please enter side c: "))

        if a < 0 or b < 0 or c < 0:
            print "Please enter positive values."
        elif a == 0 and b == 0 and c == 0:
            print "Stopping"
            break
        elif ( a > (b + c) ) or ( b > (a + c) ) or ( c > (a + b) ):
            print "{:>3} {:>3} {:>3} {:>3} {:>12}".format(a, b, c, "NO", "")
        else:
            if a == b == c:
                print "{:>3} {:>3} {:>3} {:>3} {}".format(a, b, c, "YES", "EQUILATERAL")
                continue
                
            if a**2 + b**2 == c**2:
                print "{:>3} {:>3} {:>3} {:>3} {}".format(a, b, c, "YES", "PYTHAGOREAN")
                continue

            if a == b or b == c or a == c:
                print "{:>3} {:>3} {:>3} {:>3} {}".format(a, b, c, "YES", "ISOSCELES")
                continue

            if (a == b + c) or (b == a + c) or (c == a + b):
                print "{:>3} {:>3} {:>3} {:>3} {}".format(a, b, c, "YES", "DEGENERATE")
                continue

            if not(specific):
                print "{:>3} {:>3} {:>3} {:>3} {}".format(a, b, c, "YES", "")



print
print
print
print
identify_triangle()
print
print
print
print
#--------------------------------------------------
