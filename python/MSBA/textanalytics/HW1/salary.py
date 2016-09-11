import numpy as np
import matplotlib.pyplot as plt
import math, pickle, re, time
import random as rd
from collections import Counter
from nltk import pos_tag, NaiveBayesClassifier, classify
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords as stpwds
from nltk.util import ngrams

def timer(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        print "{:>10}:{:>10.3f} seconds".format(func.__name__, t2-t1)
        return result
    return wrapper

def dump_object(obj, url):
    with open(url, "w") as f:
        pickle.dump(obj, f)
    return

def load_object(url):
    with open(url) as f:
        obj = pickle.load(f)
    return obj

def lmtz_init():
    lmtzr = WordNetLemmatizer()
    return lmtzr

def get_stopwords():
    stopwords = stpwds.words("english")
    return stopwords

def pruneJD(line):
    jd = line.decode("utf-8").split('"')
    if len(jd) < 2:
        return ""
    tokens = re.split("\W+", jd[1])
    while "" in tokens:
        tokens.remove("")
    return tokens

def get_pos(tuple_list):
    pos_list = []
    append = pos_list.append
    for tup in tuple_list:
        try:
            append(tup[1])
        except TypeError:
            continue
    return pos_list

def composeJD(tokens,
            lem=False,
            lmtzr=lmtz_init(),
            rm_stopwords=False,
            stopwords=get_stopwords(),
            bigram=False):
    if lem:
        lmtz = lmtzr.lemmatize
        tokens = map(lmtz, tokens)
        if rm_stopwords:
            tokens = [token for token in tokens if token not in stopwords]
    elif rm_stopwords:
        tokens = [token for token in tokens if token not in stopwords]

    if bigram:
        token_pos = pos_tag(tokens)
        token_pos = get_pos(token_pos)
        if len(token_pos) > 1:
            tokens += list(ngrams(token_pos, 2))

    return tokens 

@timer
def jd2pos(url, size=0, lem=False, rm_stopwords=False):
    if lem:
        lmtzr = lmtz_init()
        lmtz = lmtzr.lemmatize
    if rm_stopwords: stopwords = get_stopwords()
    pruneJDi = pruneJD
    word_dict = {}
    pos_dict = {}
    with open(url, "r") as f:
        next(f)
        count = 1
        for line in f:
            
            # read the first n lines specified by the user
            if size > 0:
                if count > size:
                    break
                else:
                    count += 1

            tokens = pruneJDi(line)
            if len(tokens) == 0:
                continue

            jd_pos = pos_tag(tokens)
            for word, pos in jd_pos:
                if lem:
                    word = lmtz(word)
                    if rm_stopwords:
                        if word in stopwords:
                            continue
                elif rm_stopwords:
                    if word in stopwords:
                        continue
                try:
                    word_dict[word] += 1
                except KeyError:
                    word_dict[word] = 1

                try:
                    pos_dict[pos] += 1
                except KeyError:
                    pos_dict[pos] = 1
                continue

    dump_object(word_dict, "data/word_dict_{}.txt".format(time.time()))
    dump_object(pos_dict, "data/pos_dict_{}.txt".format(time.time()))
    return word_dict, pos_dict

def dict2list(dic):
    lst = sorted(list(dic.items()), key=lambda tup: tup[1], reverse=True)
    return lst

def url2list(url):
    dic = load_object(url)
    lst = dict2list(dic)
    return lst

def top_terms(lst, n):
    for i in xrange(n):
        print "{:>15} x{:>6}".format(lst[i][0], lst[i][1])

def plot_wc(word_count, n=100):
    word = np.array([elem[0] for elem in word_count])
    count = np.array([elem[1] for elem in word_count])
    rank = np.array(range(1, len(word)+1))
    reverse = rank[::-1]
    reverse_log = np.array(map(np.log, np.abs(reverse)))

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.scatter(rank[:n], count[:n], color="g")
    ax2.scatter(rank[:n], reverse_log[:n], color="b")
    ax1.set_xlabel("Rank")
    ax1.set_ylabel("Frequency", color="g")
    ax2.set_ylabel("log(inverse rank)", color="b")
    plt.savefig("data/word_count_fig.png")
    # plt.show()

@timer
def salary_cutpoint(url, p=75):
    with open(url, "r") as f:
        salary_list = []
        append = salary_list.append
        next(f)
        for line in f:
            salary = line.split(",")[-2]
            if len(salary) > 0:
                append(int(salary))

        salary_array = np.array(salary_list)
    return np.percentile(salary_array, p)

@timer
def richJD(url, index, q, size=0, lem=False, rm_stopwords=False, bigram=False):
    if lem: lmtzr = lmtz_init()
    if rm_stopwords: stopwords = get_stopwords()
    token_dict = {}
    pruneJDi = pruneJD
    composeJDi = composeJD
    with open(url, "r") as f:
        next(f)
        count = 1

        for line in f:
            
            # read the first n lines specified by the user
            if size > 0:
                if count > size:
                    break
                elif count not in index:
                    count += 1
                    continue
                else:
                    count += 1

            # take salary and compare with cutpoint
            if int(line.split(",")[-2]) < q:
                continue
            # if salary >= cutpoint, tokenize JD
            tokens = pruneJDi(line)
            if len(tokens) == 0:
                continue
            # according to user, lemmatize or remove stopwords
            tokens = composeJDi(tokens, lem=lem, rm_stopwords=rm_stopwords, bigram=bigram)
            token_count = Counter(tokens)
            for token, n in token_count.items():
                try:
                    token_dict[token] += n
                except KeyError:
                    token_dict[token] = 1

    dump_object(token_dict, "data/token_dict_{}.txt".format(time.time()))
    return token_dict

@timer
def lowJD(token_dict_total, token_dict_high):
    token_dict_low = {}
    for key in token_dict_total:
        try:
            token_dict_low[key] = token_dict_total[key] - token_dict_high[key]
        except KeyError:
            token_dict_low[key] = token_dict_total[key]
    return token_dict_low

@timer
def term_prob(corpus, subset):
    prob_dict = {}
    N = sum([i for (_, i) in list(corpus.items())])
    for key in corpus:
        if key not in subset:
            prob_dict[key] = 1.0 / N
        else:
            prob_dict[key] = subset[key] + 1.0 / N
    return prob_dict

@timer
def log_prob(term_prob_high, term_prob_low):
    term_log_prob = {}
    log = math.log
    for key in term_prob_high:
        term_log_prob[key] = log(term_prob_high[key]/term_prob_low[key])
    return term_log_prob

@timer
def pred_salary(url, benchmark, q, p, index, size=0, train=True, lem=False, rm_stopwords=False, bigram=False):
    if lem:
        lmtzr = lmtz_init()
        lmtz = lmtzr.lemmatize
    if rm_stopwords: stopwords = get_stopwords()
    pruneJDi = pruneJD
    composeJDi = composeJD
    log = math.log
    with open(url, "r") as f:
        next(f)
        count = 1
        pred_list = []
        append = pred_list.append
        for line in f:
            
            if size > 0:
                if count > size:
                    break
                elif count not in index:
                    count += 1
                    continue
                else:
                    count += 1

            tokens = pruneJDi(line)
            if len(tokens) == 0:
                continue

            tokens =composeJDi(tokens,
                            lem=lem,
                            rm_stopwords=rm_stopwords,
                            bigram=bigram)

            term_freq = Counter(tokens)
            prob = 0
            for key in term_freq:
                try:
                    prob += term_freq[key] * benchmark[key]
                except KeyError:
                    prob += 0
            # add log(prior)
            prob += log(p/(1-p+0.00001))
            if prob > 0:
                pred = 1
            else:
                pred = 0
            if train:
                actual = 1 * (int(line.split(",")[-2]) >= q)
                append((pred, actual))
            else:
                append(pred)
        return pred_list

def pred_accuracy(pred_list):
    correct_list = [(pred[0] == pred[1]) for pred in pred_list]
    return sum(correct_list)*1.0/len(correct_list)

def pruneJD_df(jd):
    tokens = re.split("\W+", jd.decode("utf-8"))
    while "" in tokens:
        tokens.remove("")
    if len(tokens) == 0:
        return ""
    return tokens

def get_sense(word, stopwords):
    if word not in stopwords:
        return word

@timer
def jd2bow(jd_salary, option=1):
    '''This function reads a pandas DataFrame object with
    the FullDescription and SalaryNormalized columns and
    creates a dictionary of bag of words and also a list of
    token counts.
    
    option  lemmatize   rm_stopwords    include POS bigrams
    1       False       False           False
    2       True        False           False
    3       False       True            False
    3       False       False           True'''

    lem, rm_stopwords, bigram = False, False, False
    bag = {}
    data = []

    if option == 2:
        lem == True
    elif option == 3:
        rm_stopwords = True
        stopwords = get_stopwords()
    elif option == 4:
        bigram = True

    jd = list(jd_salary["FullDescription"].map(pruneJD_df))

    if lem:
        jd = [map(lmtzr.lemmatize, tokens) for tokens in jd]
    if rm_stopwords:
        jd = [map(get_sense(stopwords=stopwords), tokens) for tokens in jd]
    if bigram:
        token_pos = [map(pos_tag, tokens) for tokens in jd]
        token_pos = [map(get_pos, tokens) for tokens in token_pos]
        bigram_list = list(ngrams(token_pos, 2))
        jd = [jd[i] + token_pos[i] for i in range(len(jd))]
    
    jd = map(Counter, jd)
    jd_list = map(lambda dic: list(dic.items()), jd)
    data = zip(jd, list(jd_salary["SalaryNormalized"]))

    for tokens in jd_list:
        for token in tokens:
            if token[0] not in bag:
                bag[token[0]] = 1
            else:
                bag[token[0]] += token[1]

    return bag, data 

def sort_log_prob(dic):
    sort_log_prob = list(dic.items())
    sort_log_prob = sorted(sort_log_prob, key=lambda tup: tup[1], reverse=True)
    print "Top 10 high salary indicators:"
    print "{:<12}{:>8}".format("Token", "log_prob")
    for token, log_prob in sort_log_prob[:10]:
        print "{:<12}{:>8.4f}".format(token, log_prob)
    print "Top 10 low salary indicators:"
    print "{:<12}{:>8}".format("Token", "log_prob")
    for token, log_prob in sort_log_prob[::-1][:10]:
        print "{:<12}{:>8.4f}".format(token, log_prob)
    return

def partA(url, size=0, lem=False, rm_stopwords=False):
    word_dict, pos_dict = jd2pos(url,
                                size=size,
                                lem=lem,
                                rm_stopwords=rm_stopwords)

    pos_list = dict2list(pos_dict)
    top_terms(pos_list, 5)
    word_list = dict2list(word_dict)
    plot_wc(word_list, 100)
    return

def partB(url, size=0, train=1, lem=False, rm_stopwords=False, bigram=False):
    rd.seed(128)
    cutpoint = salary_cutpoint(url, p=75)

    if size == 0:
        n = 244769 - 1
    else:
        n = size

    train_index = rd.sample(xrange(1, n+1), int(math.ceil(n*train)))

    if train == 1:
        test_index = train_index
    else:
        test_index = list(set(xrange(1, size+1)) - set(train_index))

    token_freq_total = richJD(url,
                            q=0,
                            index=xrange(1, n+1),
                            size=size,
                            lem=lem,
                            rm_stopwords=rm_stopwords,
                            bigram=bigram)
    token_freq_high = richJD(url,
                            q=cutpoint,
                            index=train_index,
                            size=size,
                            lem=lem,
                            rm_stopwords=rm_stopwords,
                            bigram=bigram)
    token_freq_low = lowJD(token_freq_total, token_freq_high)
    token_prob_high = term_prob(token_freq_total, token_freq_high)
    token_prob_low = term_prob(token_freq_total, token_freq_low)
    token_log_prob = log_prob(token_prob_high, token_prob_low)
    sort_log_prob(token_log_prob)
    prediction = pred_salary(url=url,
                            benchmark=token_log_prob,
                            q=cutpoint,
                            p=0.25,
                            index=test_index,
                            size=size,
                            train=True,
                            lem=lem,
                            rm_stopwords=rm_stopwords,
                            bigram=bigram)
    accuracy = pred_accuracy(prediction)
    print accuracy

url = "data/Train_rev1.csv"
# line count in Train_rev1.csv
wc = 244769
size = 5000
partA(url=url, size=size, lem=False, rm_stopwords=False)
partB(url=url, size=size, train=0.7, lem=False, rm_stopwords=False, bigram=False)
