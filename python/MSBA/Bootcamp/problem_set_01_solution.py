def print_num():
    for i in range(5+1):
        print i,


def print_upto():
    num = raw_input("Please enter a number: ")
    for i in range(1, int(num)+1):
        print i


def print_alphabet():
    for i in range(65, 91):
        print chr(i),
    print
    for i in range(97, 123):
        print chr(i),


def beesnees():
    for i in range(1, 101):
        if i % 3 == 0 and i % 5 == 0:
            print "BEESNEES",
        elif i % 3 == 0:
            print "Bees",
        elif i % 5 == 0:
            print "Nees",
        else:
            print i,

       
def towercash():
    stack_height = 0.00011/2
    counter = 0
    while True:
        counter +=1
        stack_height = stack_height * 2
        print counter, "\t", stack_height
        if stack_height > 94:
            break


def print_square_and_cube():
    num = raw_input("Please enter a number: ")
    int_num = int(num)
    if int_num < 1 or int_num > 9:
        print "Sorry!"
        return
    
    for i in range(1, int(num)+1):
        print "{:>4} {:>4} {:>4}".format(i, i ** 2, i ** 3)


def print_square_and_cube_loop():
    while True:
        num = raw_input("Please enter a number: ")
        int_num = int(num)
        if int_num == 0:
            print "Stopping!"
            break
    
        if int_num < 0 or int_num > 9:
            print "Sorry!"
            continue
    
        for i in range(1, int(num)+1):
            print "{:>4} {:>4} {:>4}".format(i, i ** 2, i ** 3)
    
print "\n\nFunction Created: print_num"
print_num()

print "\n\nFunction Created: print_upto"
print_upto()

print "\n\nFunction Created: print_alphabet"
print_alphabet()

print "\n\nFunction Created: beesnees"
beesnees()

print "\n\nFunction Created: towercash"
towercash()

print "\n\nFunction Created: print_square_and_cube"
print_square_and_cube()

print "\n\nFunction Created: print_square_and_cube_loop"
print_square_and_cube_loop()


