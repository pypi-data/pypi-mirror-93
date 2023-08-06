"""A collection of Data Science helper functions"""

# accessing libraries through pipenv
import pandas as pd
import numpy as np



def null_count(df):
    """ Check a dataframe for nulls and return the number of missing values."""
    
    null_count = [df.isnull().sum().sum()]
    return null_count
    

 def randomize(df, seed):
     """Develop a randomization function that randomizes all of a dataframes cells then returns that randomized dataframe. This function should also take a random seed for reproducible randomization."""
      for i, x in df.items():
    print (x)
    np.random.seed(x)
    #some random function
    randomize = np.random.randint(5, size=2)
    
    return randomize 