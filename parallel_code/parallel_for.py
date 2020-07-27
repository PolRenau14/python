import numpy as np
import pandas as pd
import datetime
import multiprocessing
from joblib import Parallel, delayed
import time

num_cores = multiprocessing.cpu_count()

def myFunction(par: bool):
    if par:
        time.sleep(10)
    else:
        time.sleep(5)
    dfaux = df[(df.A%2 == par) & (df.A < 6)]
    return dfaux


# Create my own mook data
todays_date = datetime.datetime.now().date()
index = pd.date_range(todays_date-datetime.timedelta(10), periods=10, freq='D')

columns = ['A','B', 'C']
data = np.array([np.arange(10)]*3).T
df = pd.DataFrame(data, index=index, columns=columns)

# parallelize calculations into two groups:
# par and impar elements of DataFrame
start = time.time()
results = Parallel(n_jobs=num_cores)(delayed(myFunction)(i) for i in [0,1])
# As we are working on DataFrame objects, the parallelize function returns a list
# where every position is  one of Dataframes, then we should concatene them
results = pd.concat(results)
end = time.time()
print(results)
print(type(results))
print("Total time expended {}".format(end-start))
# The most expensive function (par) will  overhead all time.
