#problem_01
def upper(a, b):
    return (a.upper(), b.upper())

print upper("abc", "def")

#problem_02
def pad(filler, repeat):
    return filler * repeat

print pad("?", 10)

#problem_03
def summer(lst):
    return sum(lst)

print summer([1, 2, 3])

#problem_04
def adder(lst, increment):
    result = []
    for x in lst:
        result.append(x + increment)
    return result

def adder_mod(lst, increment):
    for i in range(0, len(lst)):
        lst[i] += increment
    return lst

print adder([1, 2, 3], 1)
print adder_mod([1, 2, 3], 1)

#problem_05
def return_dictionary(list_of_tuples):
    dict = {}
    for tpl in list_of_tuples:
        if tpl[0] not in dict:
            dict[tpl[0]] = tpl[1]
        else:
            if type(dict[tpl[0]]) != type(tpl[1]):
                dict[tpl[0]] = str(dict[tpl[0]])+ str(tpl[1])
            else:
                dict[tpl[0]] += tpl[1]
    return dict
        
print return_dictionary([("a", "b"), ("b", "c")])
print return_dictionary([("a", 1), ("a", 2)])
print return_dictionary([("a", 1), ("a", "2")])

#problem_06
def return_list_items(list_of_tuples):
    lst = []
    for item in list_of_tuples:
        lst.append(item[0])
        lst.append(item[1])
    return lst

print return_list_items([("No 1", 1),("No 2", 2),("No 3", 3)])

#problem_07
def print_enumerated_stock_prices(stock_ticker_list, stock_price_list):
    x = len(stock_ticker_list)
    y = len(stock_price_list)
    
    if x < y:
        for i in range(0, y - x):
            stock_price_list.pop()

    if x > y:
        for j in range(0, x - y):
            stock_ticker_list.pop()

    for k in range(0, min(x, y)):
        print "{:<4}{:<6}{:>8.2f}".format((k+1), stock_ticker_list[k], stock_price_list[k])
    
stocks = ["AAPL", "AMZN", "IBM", "GOOG"]
prices = [100, 80, 45, 96]
print_enumerated_stock_prices(stocks, prices)

#problem_08
def highlight_word(text, highlight):
    import re
    lst =  re.split(highlight+"( |,|.)", text)
    new_text = ""

    if "" not in lst:
        print "Key word not found in \"{}\"".format(text)
        return False
    else:
        for item in lst:
            if item == "":
                new_text = "".join([new_text, highlight.upper()])
            else:
                new_text = "".join([new_text, item])
        print new_text

    return new_text
        
highlight_word("hello world.", "hello")
highlight_word("hello  world.", "hello")
highlight_word("hello,world.", "hello")
highlight_word("hell o,world.", "hello")
