#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
import statsmodels.formula.api as smf


# In[2]:

def mil(a):



  car_df=pd.read_csv('auto-mpg.csv')


  car_df.horsepower.unique()


  # ## Observation: In the horsepower values ? mark is included whichmakes the variable as object
  # ### need to replace the values and convert horsepower variable to integer

  # In[7]:


  car_df['horsepower']=car_df['horsepower'].replace('?',np.nan)


  # In[8]:


  # here the ? mark vales are replaced with the nan values so will check how many records got replaced
  car_df['horsepower'].isnull().sum()


  # #### 6 values got replaced as nan in horsepower variable
  # 
  # ### now need to convert the horsepower variable to interger and fill the nan values with median value of horsepower

  # In[9]:


  car_df['horsepower']=car_df['horsepower'].astype('float64')


  # In[10]:


  car_df['horsepower'].dtype


  # In[11]:


  # fill the nan values with median values
  car_df['horsepower']=car_df['horsepower'].fillna(car_df['horsepower'].median())


  # In[12]:


  car_df['horsepower'].isnull().sum()


  # ### so now the hp variable got converted to integers and now we can proceed to check the correlation of the variables

  # In[13]:


  corr_table=car_df.corr()
  corr_table


  # ## Lets visualize the above values in the heat map

  # In[14]:


  plt.figure(figsize=(20,10))
  g=sns.heatmap(corr_table,annot=True)
  g.set(title='Correlation matrix of the car-mpg dataset')
  plt.show()          
            


  # ## Inferences:
  #  
  #  ### Mpg column is having good corelation on cyl,disp,wt
  #  
  #  ### cyl ,disp and wt  and hp are having negative corelation 
  #  
  #  ### next will check the data distribution using the pair plot

  # In[15]:


  sns.pairplot(car_df,diag_kind='kde')
  plt.show()


  # In[16]:


  car_df['cylinders'].value_counts()


  # # Next will be performing the statistical test to find the significance of variable so that we can reduce no.of variable 

  # In[17]:


  # for this we need to import statsmodels as shown below 
  import statsmodels.formula.api as smf


  # In[18]:


  test1=smf.ols('mpg~cylinders+displacement+horsepower+weight+acceleration+origin',car_df).fit()


  # In[19]:


  test1.summary()


  # ## Inference as in the above summary the p value of the acc is greater than 0.05 so we can remove the acc variable from the dataset

  # In[20]:


  car_df=car_df.drop('acceleration',axis=1)
  # car_df.head()


  # In[21]:


  # i am removing the car name variable as i has nothing to to here
  car_df=car_df.drop('car name',axis=1)
  # car_df.head()


  # ## Now we are good enough to train our regression model

  # In[22]:


  # importing the requried libaries for regression

  from sklearn.linear_model import LinearRegression
  from sklearn.model_selection import KFold
  from sklearn import metrics


  # ## now i am spliting my dataframe into dependent and independent variable i.e x and y

  # In[23]:


  y=car_df['mpg']
  # y.head()


  # In[24]:


  x=car_df.iloc[:,1:]



  # ## I am using here KFold method to train and test my model to get good metrices and performance

  # In[25]:


  kf=KFold(n_splits=5,shuffle=True,random_state=2)
  rmse=[]
  for train,test in kf.split(x,y):
      LR=LinearRegression()
      #print(train)
      xtrain=x.iloc[train]
      xtest=x.iloc[test]
      ytrain=y.iloc[train]
      ytest=y.iloc[test]
      LR.fit(xtrain,ytrain)
      ypredict=LR.predict(xtest)
      
      rmse.append(np.sqrt(metrics.mean_squared_error(ytest,ypredict)))
      

  print('Rmse error in the first test is :%1.3f'%(rmse[0]))
  print('Rmse error in the second test is:%1.3f'%(rmse[1]))
  print('Rmse error in the third test is :%1.3f'%(rmse[2]))
  print('Rmse error in the fourth test is:%1.3f'%(rmse[3]))
  print('Rmse error in the fifth test is :%1.3f'%(rmse[4]))

  print('Average mean rmse error i.e Bias error is: %1.3f'%(np.mean(rmse)))

  print('Variance of rmse error i.e Variance error is: %1.3f'%(np.var(rmse,ddof=1)))

      
      
      


  # In[26]:


  ## predicting the mileage values for new values 
  values=[[8,206,200,1900,70,2]]
  new_mileage=LR.predict(values)
  print('predicted new mileage for above values is %1.3f'%new_mileage)
  return LR.predict(values)


  # In[27]:

import streamlit as st 
st.title("Mileage Predictor")
st.markdown("##### Want to check mileage of you chosen car?\n##### So let's try evaluating the mileage ")
st.image("dashboard-digital-display-mileage-fuel-consumption-speed-modern-car-speedometer-new-colorful-light-indicators-isolatred-71989997.jpg")


a=st.text_input(label="What is the number of Cylinders? (in cc)")
b=st.text_input(label="What is the Displacement? (in cc)")
c=st.text_input(label="What is the Horsepower? (in watts)")
d=st.text_input(label="What is the Weight? (in Kg)")
if st.button('Predict'):
  out=mil([[a,b,c,d,70,20]])
  st.success("{} is the predicted mileage in kmpl".format(out[0]))
