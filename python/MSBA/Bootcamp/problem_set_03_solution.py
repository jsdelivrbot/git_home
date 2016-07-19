import re

#--------------------------------------------------
def upper(str1, str2):
    return str1.upper(), str2.upper()

print
print
print upper("a", 'b')
print upper("woot", "this is great")
print
print


#--------------------------------------------------
def pad(filler, repeat):
    return filler * repeat


print
print
print pad('-', 10)
print pad('?', 20), pad(':',5), pad(';)', 5)
print
print


#--------------------------------------------------
def summer(number_list):
    total = 0
    for i in number_list:
        total += i
    return total


print
print
my_list = [10, 20, 30]
print summer(my_list)

print summer( [1, 2, 3, 4, 5] )

total = summer( [20, 200] )
print total
print
print


#--------------------------------------------------
def adder(number_list, increment):
    new_list = []
    for num in number_list:
        new_list.append(num + increment)
    return new_list


print
print
print adder([1, 2, 3], 10)
beg_list = [10, 20, 30]
print "beg_list BEFORE function call", beg_list
end_list = adder(beg_list, 100)
print "beg_list AFTER function call", beg_list
print "end_list AFTER function call", end_list
print
print


#--------------------------------------------------
def return_dictionary(list_of_tuples):
    dictionary = dict()
    for name, age in list_of_tuples:
        dictionary[name] = age
    return dictionary


print
print
my_tuple_list = [('aa', 10), ('bb', 20), ('cc', 15)]

print return_dictionary(my_tuple_list)
# OR
print my_tuple_list, '--dict-->', return_dictionary(my_tuple_list)
print
print


#--------------------------------------------------
def return_list_items(list_of_tuples):
    return_list = []
    for name, age in list_of_tuples:
        return_list.append(name)
        return_list.append(age)
    return return_list


print
print
my_tuple_list = [('aapl', 93.40), ('goog', 675.22)]

print return_list_items(my_tuple_list)
# OR
print my_tuple_list, '--list-->', return_list_items(my_tuple_list)
print
print


#--------------------------------------------------
def print_enumerated_stock_prices(stock_list, stock_price):
    for idx, (stock, price) in enumerate(zip(stock_list, stock_price), start=1):
        print "{:>2} {:4} {:>7}".format(idx, stock, price)


print
print

stock_list = ["AA", "COKE", "LUV", ]
stock_price = [9.38, 140.59, 38.31]
print_enumerated_stock_prices(stock_list, stock_price)

print
print


#--------------------------------------------------
def highlight_word(text, highlight):
    result = ""
    words = re.split('\s', text)
    for word in words:
        if word == highlight:
            result += word.upper() + " "
        else:
            result += word + " "
    return result

print
print
print highlight_word('This is a test and only a test', "test")
print
print


#--------------------------------------------------
def basic_stats(number_list):

    count = len(number_list)
    stats = {}
    
    if count < 2:
        stats["error"] = "List should contain more than one number."

    else:
        number_list.sort()
        total = 0
        for num in number_list:
            total += num
        mean = float(total) / float(count)

        middle = count / 2
        if count % 2 == 0:
            median = float( ( number_list[middle-1] ) + float( number_list[middle] ) ) / 2
        else:
            median = float( number_list[middle] )

        max = number_list[-1]
        min = number_list[0]
        range = max - min

        stats["total"] = total
        stats["mean"] = mean
        stats["median"] = median
        stats["min"] = min
        stats["max"] = max
        stats["range"] = range    

    return "{:15} {:4} {}".format(number_list, "--->", stats)


print
print

number_list = [5]
print basic_stats(number_list)

number_list = [10, 2]
print basic_stats(number_list)

number_list = [5, 4, 3, 2, 1]
print basic_stats(number_list)

print
print

#--------------------------------------------------
