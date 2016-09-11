## Predict Salary Based on Job Description
+ Data source: http://www.kaggle.com/c/job-salary-prediction

#### Part A (basic text mining)   
  1. What are the top 5 parts of speech in this corpus of job descriptions? How frequently do they appear?   
  2. Does this corpus support Zipf’s law? Plot the most common 100 words in the corpus against the theoretical prediction of the law. For this question, do not remove stopwords. Also do not perform stemming or lemmatization.   
  3. If we remove stopwords and lemmatize the corpus, what are the 10 most common words? What is their frequency?

#### Part B (predict salary from job description)   
Predict high (75th percentile and above) or low (below 75th percentile) salary from the text contained in the job descriptions. Get the training data on kaggle.com (train_rev1) (do not use the validation data provided on kaggle.com). Use the Naïve Bayes classifier in Python to classify job descriptions into high and low salary categories (we will discuss the theory of Naïve Bayes later in this course).   
  1. Create a classification model with all words and the bag-of-words approach. How accurate is the model?   
  2. Create a classification model after lemmatization. Did the classification accuracy increase relative to B1?   
  3. Take out the stopwords (but do not lemmatize), build a classification model and check the accuracy, and compare with that in B1 & B2.
  Also show the top 10 words (excluding stopwords) that are most indicative of (i) high salary, and (ii) low salary.   
  4. Use the job descriptions without lemmatiztion and stopword removal. Add parts-of-speech bigrams to the bag-of-words, and run a new classification model. Does the accuracy increase over the results in B1?
