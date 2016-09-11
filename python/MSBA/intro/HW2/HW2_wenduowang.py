
# coding: utf-8

# In[1]:

from pandas import Series, DataFrame
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
get_ipython().magic(u'pylab inline')


# # NYC Restaurants

# ### Read in data from csv, and check column names to keep in mind.

# In[2]:

restaurants = pd.read_csv("NYC_Restaurants.csv", dtype=unicode)
for index, item in enumerate(restaurants.columns.values):
    print index, item


# ## Question 1: Create a unique name for each restaurant

# 1. Select `DBA`, `BUILDING`, `STREET` and `ZIPCODE` columns as a dataframe
# 2. Apply `apply()` function on the selected dataframe, which takes in the series of the dataframe.
#     + inside the `apply()` function, use placeholders to indicate that 4 series will be taken at the same time.
#     + it is possible to select each column and concatenate them together, though looks not DRY.

# In[3]:

#use .apply() method to combine the 4 columns to get the unique restaurant name
restaurants["RESTAURANT"] = restaurants[["DBA", "BUILDING", "STREET", "ZIPCODE"]].                                        apply(lambda x: "{} {} {} {}".format(x[0], x[1], x[2], x[3]), axis=1)

#incase that the RESTAURANT names contain spaces or symbols, strip off them
restaurants["RESTAURANT"] = restaurants["RESTAURANT"].map(lambda y: y.strip())
print restaurants["RESTAURANT"][:10]


# ## Question 2: How many restaurants are included in the data?

# Since each `RESTAURANT` appears appears only once in `value_count()` series, therefore applying `len()` will return the number of restaurants in the whole dataset.

# In[4]:

print "There are", len(restaurants.drop_duplicates(subset="RESTAURANT")["RESTAURANT"].value_counts()), "restaurants in the data."


# ## Question 3: How many chains are there?

# "Chains" are brands having at least 2 different `RESTAURANT`. After `drop_duplicates(subset="RESTAURANT")`, extracting`value_count()` on `DBA` will give how many `RESTAURANT` each `DBA` has. Converting each value into logical with evaluation `value_count()>=2` and then summing up the how series will give the number of `True` records, which is the number of chains.

# In[5]:

num_chain = sum(restaurants.drop_duplicates(subset="RESTAURANT")["DBA"].value_counts()>=2)
print "There are", num_chain, "chain restaurants."


# ## Question 4: Plot a bar graph of the top 20 most popular chains.

# "Popularity" is here understood as number of `RESAURANT` of each `DBA`.
# 1. Extract the chain `DBA` 
# 2. Define a helper function `chain` to identify if a given `DBA` is a chain.
# 3. Use the helper function to make a mask to select the chain `DBA`.
# 4. Apply the mask to the whole dataframe, and drop duplicate `RESTAURANT`, the `value_counts()` will give the number of locations of each `DBA`

# In[6]:

chains = restaurants.drop_duplicates(subset="RESTAURANT")["DBA"].value_counts()[: num_chain].index.values
def chain(restaurant):
     return (restaurant in chains)
mask = restaurants["DBA"].map(chain)
restaurants[mask].drop_duplicates(subset="RESTAURANT")["DBA"].value_counts()[:20].plot(kind="bar")


# ## Question 5: What fraction of all restaurants are chains?

# To calculate the faction of chains among all restaurants, we use an inline mask on `DBA`(`True` if is chain). Summing up `True` values gives the number of chains. It is divided by the total number of unique `RESTAURANT` to get the fraction.

# In[7]:

print "The percentage of chain restaurants is",
print "{:.2%}".format(sum(restaurants.drop_duplicates(subset="RESTAURANT")["DBA"].value_counts()>=2)/float(len(restaurants["RESTAURANT"].value_counts())))


# ## Question 6: Plot the number of non-chain restaurants in each boro.

# 1. In case "missing" is spelt differently, a helper function `lower_case` is defined to convert the string into lower case.
# 2. Use the `chain` helper function to make a mask selecting chains. Negative of this mask will return non-chains.
# 3. Use the `lower_case` function to select missing `BORO`.
# 4. Use the "negative" mask to select non-chains and remove duplicate `RESTAURANT`, and then remove missing `BORO`, `value_counts()` gives number of non-chains in each borough.

# In[8]:

def lower_case(X):
    return X.lower()

mask_1 = restaurants["DBA"].map(chain)
mask_2 = restaurants["BORO"].map(lower_case) != "missing"
restaurants[-mask_1].drop_duplicates(subset="RESTAURANT")[mask_2]["BORO"].value_counts().sort_values(ascending=False).plot(kind="bar")


# ## Question 7: Plot the fraction of non-chain restaurants in each boro.

# The goal is to calculate the ratio of $\frac{N_{non-chain}}{N_{total}}$ within each borough.
# 
# This fraction can be done between two series-`value_counts()` of non-chains of `BORO` (not missing) and `value_counts()` of all unique `RESTAURANT` of `BORO`.
# 
# Depending on which borough has the highest ratio, a message will pop out to compare if it is the same with the borough with the most non-chains.

# In[9]:

series_tmp_1 = restaurants[mask_2].drop_duplicates(subset="RESTAURANT")["BORO"].value_counts()
series_tmp_2 = restaurants[-mask_1][mask_2].drop_duplicates(subset="RESTAURANT")["BORO"].value_counts()
series_tmp_ratio = series_tmp_2/series_tmp_1
series_tmp_ratio.sort_values(ascending=False).plot(kind="bar")
print "The highest non-chain/total ratio is:", "{:0.2%} ({})".format(series_tmp_ratio.sort_values(ascending=False)[0],                                                                     series_tmp_ratio.sort_values(ascending=False).index.values[0])
if series_tmp_ratio.sort_values(ascending=False).index.values[0] !=restaurants[-mask_1].drop_duplicates(subset="RESTAURANT")[mask_2]["BORO"].value_counts().sort_values(ascending=False).index.values[0]:
    print "It is not the same borough."
else:
    print "It is the same borough."


# ## Question 8: Plot the popularity of cuisines.

# Drop duplicate `RESTAURANT` and plot on the top 20 of sorted `value_counts()` of `CUISINE DESCRIPTION.`

# In[10]:

restaurants.drop_duplicates(subset="RESTAURANT")["CUISINE DESCRIPTION"].value_counts()                                                                .sort_values(ascending=False)[:20].plot(kind="bar")


# ## Question 9: Plot the cuisines among restaurants which never got cited for violations.

# Here we used a mask to sift out the restaurants whose `VIOLATION CODE` is missing.

# In[18]:

non_clean_restaurants = restaurants[-restaurants["VIOLATION CODE"].isnull()]["RESTAURANT"].value_counts().index.values
def is_clean(restaurant, blacklist=non_clean_restaurants):
    return restaurant not in blacklist
mask_clean = restaurants["RESTAURANT"].map(is_clean)
restaurants[mask_clean]["CUISINE DESCRIPTION"].value_counts().sort_values(ascending=False)[:20].plot(kind="bar")


# ## Question 10: What cuisines tend to be the “cleanest”?

# 1. Make a series of all cuisines with 20 or more serving records in non-duplicate restaurants.
# 2. Define a helper function to determine if a given cuisine is in the series above.
# 3. Make a mask for the most served cuisines.
# 4. Apply that mask and the "non violation" mask in Q9 to produce a `value_counts()` series, containing the non-violation records for those cuisines.
# 5. Apply the newly defined mask to the whole DataFrame and produce another `value_counts()` containing how many inspections were done for the most served cuisines.
# 6. Divide the two series and get a new series of the format $cuisine:\ \frac{N_{non-violation}}{N_{total\ inspection}}$.
# 7. Plot the first 10 elements.

# In[12]:

top_cuisine_series = restaurants.drop_duplicates(subset=["RESTAURANT","CUISINE DESCRIPTION"])["CUISINE DESCRIPTION"].value_counts()
def is_top_cuisine(cuisine):
    return top_cuisine_series[cuisine]>=20
mask_3 = restaurants["VIOLATION CODE"].isnull()
mask_4 = restaurants["CUISINE DESCRIPTION"].map(is_top_cuisine)
series_tmp_3 = restaurants[mask_4][mask_3]["CUISINE DESCRIPTION"].value_counts()
series_tmp_4 = restaurants[mask_4]["CUISINE DESCRIPTION"].value_counts()
(series_tmp_3/series_tmp_4).sort_values(ascending=False)[:10].plot(kind="bar")


# ## Question 11: What are the most common violations in each borough?

# 1. Use `crosstab` to create a dataframe with `VIOLATION DESCRIPTION` as index, and `BORO` (without "Missing" boroughs) as columns. `dropna` is set `True` so `NaN` will not be recorded.
# 2. Every cell in the `crosstab` is the number of occurences of a violation in a certain borough. `idxmax()` method is applied to automatically retrieve the max occurence for each `BORO`.

# In[13]:

violation_boro_tab = pd.crosstab(
                        index=restaurants["VIOLATION DESCRIPTION"],
                        columns=restaurants[restaurants["BORO"]!="Missing"]["BORO"],
                        dropna=True
                    )
print "The most common violation in each borough is summarised below:"
violation_boro_tab.idxmax()


# ## Question 12: What are the most common violations per borough, after normalizing for the relative abundance of each violation?

# 1. Use `apply()` function to apply `lambda x: x.map(float)/violation_frequency_series, axis=0` on each column of the above `crosstab`. The resulting series gives _normalized_ violation frequency.
#     + `float()` ensures the division returns fraction.
#     + The denominator is a series of the `value_counts()` of all `VIOLATION DESCRIPTION`.

# In[14]:

violation_frequency_series = restaurants["VIOLATION DESCRIPTION"].value_counts()
violation_boro_norm_tab = violation_boro_tab.apply(lambda x: x.map(float)/violation_frequency_series, axis=0)
print "After normalization, the most common violation in each borough is summarised below:"
violation_boro_norm_tab.idxmax()


# ## Question 13: How many phone area codes correspond to a single zipcode?

# 1. Create a new column `AREA` to store the first 3 digits of `PHONE`, which is the area code.
# 2. Drop duplicate rows with the same combination of `AREA` and `ZIPCODE`.
# 3. By `value_counts()==1` each `AREA` with a single `ZIPCODE` will return `True`.
# 4. Sum up `True` values to return the total number of such area codes.

# In[15]:

restaurants["AREA"] = restaurants["PHONE"].map(lambda x: x[:3])
print "There are",
print sum(restaurants.drop_duplicates(subset=["AREA", "ZIPCODE"])["AREA"].value_counts() == 1),
print "area codes corresponding to only 1 zipcode"


# ## Question 14: Find common misspellings of street names

# 1. `map` `str.split()` function on `STREET` to breakdown the string into a list of words, and take the last word as `STREET TYPE`.
# 2. Take the remaining words and join them together as `STREET BASE`.
# 3. Concatenate `STREET BASE` and `STREET TYPE` together as `STREET BASE & ZIP`, spaced with empty space.
# 4. Create a new dataframe by `concat` the above 3 series. `axis=1` meaning concatenating horizontally.
# 5. Remove duplicate records from the new dataframe, where `STREET BASE` is not empty.
# 6. Merge the new dataframe with itself to get cross-matched `STREET TYPE`.
# 7. Only keep rows where the two `STREET TYPE` are different.
# 8. Make another `crosstab` on the merged dataframe with one `STREET TYPE` as index and the other as columns.
# 9. In the new `crosstab`, the occurences of alternative `STREET TYPE` are recorded in cells, whose max occurence can be obtained with `idxmax`.

# In[16]:

restaurants["STREET TYPE"] = restaurants["STREET"].map(lambda s: s.split()[-1])
restaurants["STREET BASE"] = restaurants["STREET"].map(lambda s: " ".join(s.split()[:-1]))
restaurants["STREET BASE & ZIP"] = restaurants["STREET BASE"].map(lambda s: s+" ") + restaurants["ZIPCODE"]
new_dataframe = pd.concat(
    [restaurants["STREET BASE"], restaurants["STREET TYPE"], restaurants["STREET BASE & ZIP"]],
    axis=1
)

new_dataframe = new_dataframe[new_dataframe["STREET BASE"].map(lambda s: len(s)>0)].drop_duplicates()

merged_new_dataframe = pd.merge(
                            new_dataframe,
                            new_dataframe,
                            left_on="STREET BASE & ZIP",
                            right_on="STREET BASE & ZIP",
                            suffixes=[" 1", " 2"]
                                )

merged_new_dataframe = merged_new_dataframe[merged_new_dataframe["STREET TYPE 1"] != merged_new_dataframe["STREET TYPE 2"]]

street_name = pd.crosstab(
    index=merged_new_dataframe["STREET TYPE 1"],
    columns=merged_new_dataframe["STREET TYPE 2"],
    dropna=True
)

print "The most common alias for each of the following street type is listed"
street_name.idxmax()[
    ["AVE", "ST", "RD", "PL", "BOULEARD", "BOULEVARD"]
]

