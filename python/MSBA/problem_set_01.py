#problem 01
def print_num():
    for x in range(6):
        print x,
    print "\n"

print_num()

#problem 02
def print_upto():
    for x in range(1, int(raw_input("Type in upper limit: "))+1):
        print x

print_upto()

#prlblem 03
def print_alphabet():
    for i in range(ord("A"), ord("Z")+1):
        if i == ord("Z"):
            print chr(i)
        else:
            print chr(i),

    for j in range(ord("a"), ord("z")+1):
        print chr(j),
    print "\n"

print_alphabet()

#problem 04
def beesnees():
    for i in range(1, 101):
        if i % 15 == 0:
            print "BEESNEES",
        elif i % 3 == 0:
            print "Bees",
        elif i % 5 == 0:
            print "Nees",
        else:
            print i,
    print "\n"

beesnees()

#problem 05
def towercash():
    sum = 0
    x = 0.11/1000
    day = 1
    while sum < 94:
        sum += x
        x *= 2
        print day, sum
        day += 1

    print day - 1

towercash()

#problem 06
def print_square_and_cube():
    num = int(raw_input("Type in a num between 1 and 9: "))
    if num > 9 or num < 1:
        print "Sorry!"
        return False
    for i in range(1, num+1):
        print "{:>5}{:>5}{:>5}".format(*[i, i**2, i**3])

print_square_and_cube()

#problem 07
def print_square_and_cube_loop():
    num = int(raw_input("Type in a num betwee 1 and 9: "))
    while num < 1 or num > 9:
        if num == 0:
            print "Stopping!"
            return False
        else:
            print "Sorry!"
            num = int(raw_input("Type in a num betwee 1 and 9: "))
    for i in range(1, num+1):
        print "{:>5}{:>5}{:>5}".format(*[i, i**2, i**3])

print_square_and_cube_loop()
