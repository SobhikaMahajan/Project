import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import joblib
st.set_option('deprecation.showPyplotGlobalUse', False)
DATA_URL = ("with_loc.csv")

st.title('Data Analysis On Automotive Industry ')
st.text('This is my Microsoft Engage 2022 project. Let us have a look on the analysis')
st.text('of cars dataset.') 

st.write('')

cars = pd.read_csv('CarPrice_Assignment.csv')
cars.head()

#-----------------------------------------------------------------------------------------------
# DATA INSPECTION --------------------------------------------------------------------------------

cars.shape

cars.describe()

cars.info()

#-----------------------------------------------------------------------------------------------
# DATA CLEANING --------------------------------------------------------------------------------

#Splitting company name from CarName column
CompanyName = cars['CarName'].apply(lambda x : x.split(' ')[0])
cars.insert(3,"CompanyName",CompanyName)
cars.drop(['CarName'],axis=1,inplace=True)
cars.head()


# cars.CompanyName.unique()

cars.CompanyName = cars.CompanyName.str.lower()

def replace_name(a,b):
    cars.CompanyName.replace(a,b,inplace=True)

replace_name('maxda','mazda')
replace_name('porcshce','porsche')
replace_name('toyouta','toyota')
replace_name('vokswagen','volkswagen')
replace_name('vw','volkswagen')

cars.CompanyName.unique()

#Checking for duplicates
cars.loc[cars.duplicated()]

cars.columns

# ---------------------------------------------------------------------------------------------------
# 2. EXPLORATORY DATA ANALYSIS---------------------------------------------------------------------

st.header('Car Price')
st.text('Let us have a look on car price ditribution plot and car price spread of the')
st.text('    given dataset.')
fig1 = plt.figure(figsize=(16,8))

plt.subplot(1,2,1)
plt.title('Car Price Distribution Plot')
sns.distplot(cars.price)

plt.subplot(1,2,2)
plt.title('Car Price Spread')
sns.boxplot(y=cars.price)

plt.show()

st.write(fig1)

st.text('Inference :')

st.text('1. The plot seemed to be right-skewed, meaning that the most prices in the dataset')
st.text('are low(Below 15,000).')
st.text('2. There is a significant difference between the mean and the median of the price')
st.text(' distribution.')
st.text('3. The data points are far spread out from the mean, which indicates a high variance ')
st.text(' in the car prices.(85% of the prices are below 18,500, whereas the remaining')
st.text('15% are between 18,500 and 45,400.)')
st.write('')
st.write('')
st.write('')

st.header('Categorical Data')

st.text('- CompanyName')
st.text('- Symboling')
st.text('- fueltype')
st.text('- enginetype')
st.text('- carbody')
st.text('- doornumber')
st.text('- enginelocation')
st.text('- fuelsystem')
st.text('- cylindernumber')
st.text('- aspiration')
st.text('- drivewheel')



print(cars.price.describe(percentiles = [0.25,0.50,0.75,0.85,0.90,1]))
st.header('Most Favourable')
fig2 = plt.figure(figsize=(16, 8))

plt.subplot(1,3,1)
plt1 = cars.CompanyName.value_counts().plot(kind='bar')
plt.title('Most Favourable Company')
plt1.set(xlabel = 'Car company', ylabel='Frequency of company')

plt.subplot(1,3,2)
plt1 = cars.fueltype.value_counts().plot(kind='bar')
plt.title('Most Favourable Fuel Type')
plt1.set(xlabel = 'Fuel Type', ylabel='Frequency of fuel type')

plt.subplot(1,3,3)
plt1 = cars.carbody.value_counts().plot(kind='bar')
plt.title('Most Favourable Car Type')
plt1.set(xlabel = 'Car Type', ylabel='Frequency of Car type')

plt.show()
st.write(fig2)

st.text('Inference :')

st.text('1. Toyota seemed to be favored car company.')
st.text('2. Number of gas fueled cars are more than diesel.')
st.text('3. sedan is the top car type preferred.')
st.write('')
st.write('')
st.write('')

st.header('Symbolling')
st.text("Symbolling value shows how risky or safe a vehicle is, from an insurer's perspective.")
st.text('It can range from -3 to +3.')
st.text('-3 indicates a safe car while +3 denotes a risky one.')
fig3 = plt.figure(figsize=(20,8))

plt.subplot(1,2,1)
plt.title('Symboling Histogram')
sns.countplot(cars.symboling, palette=("cubehelix"))

plt.subplot(1,2,2)
plt.title('Symboling vs Price')
sns.boxplot(x=cars.symboling, y=cars.price, palette=("cubehelix"))

plt.show()
st.write(fig3)

st.text('Inference :')

st.text('1. It seems that the symboling with 0 and 1 values have high number of rows')
st.text('(i.e. They are most sold.)')
st.text('2. The cars with -1 symboling seems to be high priced (as it makes sense too,')
st.text('insurance risk rating -1 is quite good). But it seems that symboling with 3 value')
st.text(' has the price range similar to -2 value.There is a dip in price at symboling 1')
st.write('')
st.write('')
st.write('')


st.header('Engine')
st.text('Let us look on the most favourable engine type and compare the price.')
fig4 = plt.figure(figsize=(18,6))

plt.subplot(1,2,1)
plt.title('Engine Type Histogram')
sns.countplot(cars.enginetype, palette=("Blues_d"))

plt.subplot(1,2,2)
plt.title('Engine Type vs Price')
sns.boxplot(x=cars.enginetype, y=cars.price, palette=("PuBuGn"))
plt.show()
st.write(fig4)
# st.write(fig4)

df = pd.DataFrame(cars.groupby(['enginetype'])['price'].mean().sort_values(ascending = False))
df.plot.bar(figsize=(18,6))
plt.title('Engine Type vs Average Price')
st.pyplot()

st.text('Inference :')

st.text('1. ohc Engine type seems to be most favored type.')
st.text('2. ohcv has the highest price range (While dohcv has only one row),')
st.text('ohc and ohcf have the low price range.')
st.write('')
st.write('')
st.write('')

st.header('Average Price')
fig5 = plt.figure(figsize=(18,6))

df = pd.DataFrame(cars.groupby(['CompanyName'])['price'].mean().sort_values(ascending = False))
df.plot.bar(figsize=(18,6))
plt.title('Company Name vs Average Price')
plt.show()
st.pyplot()

df = pd.DataFrame(cars.groupby(['fueltype'])['price'].mean().sort_values(ascending = False))
df.plot.bar(figsize=(18,6))
plt.title('Fuel Type vs Average Price')
plt.show()
st.pyplot()

df = pd.DataFrame(cars.groupby(['carbody'])['price'].mean().sort_values(ascending = False))
df.plot.bar(figsize=(18,6))
plt.title('Car Type vs Average Price')
plt.show()
st.pyplot()

# st.write(fig5)
st.text('Inference :')

st.text('1. Jaguar and Buick seem to have highest average price.')
st.text('2. Diesel has higher average price than  gas.')
st.text('3. Hardtop and convertible have higher average price.')
st.write('')
st.write('')
st.write('')

st.header('Doors')
fig6 = plt.figure(figsize=(15,5))

plt.subplot(1,2,1)
plt.title('Door Number Histogram')
sns.countplot(cars.doornumber, palette=("plasma"))

plt.subplot(1,2,2)
plt.title('Door Number vs Price')
sns.boxplot(x=cars.doornumber, y=cars.price, palette=("plasma"))

plt.show()
st.write(fig6)
st.text('Inference :')
st.text('1. Mostly people prefer 4 door wheelers.')
st.text('2. Doornumber variable is not affacting the price much. There is no sugnificant')
st.text('difference between the categories in it.')
st.write('')
st.write('')
st.write('')

st.header('Aspiration')
fig7 = plt.figure(figsize=(15,5))

plt.subplot(1,2,1)
plt.title('Aspiration Histogram')
sns.countplot(cars.aspiration, palette=("plasma"))

plt.subplot(1,2,2)
plt.title('Aspiration vs Price')
sns.boxplot(x=cars.aspiration, y=cars.price, palette=("plasma"))

plt.show()
st.write(fig7)
st.text('It seems aspiration with turbo have higher price range than the std (though it')
st.text('has some high values outside the whiskers.)')
st.write('')
st.write('')
st.write('')

st.header('Engine Location, Cylinder Number, Fuel System, Drive Wheel')
def plot_count(x,fig):
    plt.subplot(4,2,fig)
    plt.title(x+' Histogram')
    sns.countplot(cars[x],palette=("magma"))
    plt.subplot(4,2,(fig+1))
    plt.title(x+' vs Price')
    sns.boxplot(x=cars[x], y=cars.price, palette=("magma"))
    
fig8 = plt.figure(figsize=(15,20))

plot_count('enginelocation', 1)
plot_count('cylindernumber', 3)
plot_count('fuelsystem', 5)
plot_count('drivewheel', 7)

plt.tight_layout()
st.write(fig8)

st.text('Inference :')

st.text('1. Very few datapoints for enginelocation categories to make an inference.')
st.text('2. Most common number of cylinders are four, six and five. Though eight')
st.text('cylinders have the highest price range.')
st.text('3. mpfi and 2bbl are most common type of fuel systems. mpfi and idi having')
st.text('the highest price range. But there are few data for other categories to derive any')
st.text('meaningful inference')
st.text('4. A very significant difference in drivewheel category. Most high ranged cars seems')
st.text('to prefer rwd drivewheel.')
st.write('')
st.write('')
st.write('')


st.header('Numerical Data')
st.header('Car Length,Car Width,Car Height, Curb Weight')
def scatter(x,fig):
    plt.subplot(5,2,fig)
    plt.scatter(cars[x],cars['price'])
    plt.title(x+' vs Price')
    plt.ylabel('Price')
    plt.xlabel(x)

fig9 = plt.figure(figsize=(10,20))

scatter('carlength', 1)
scatter('carwidth', 2)
scatter('carheight', 3)
scatter('curbweight', 4)

plt.tight_layout()
st.write(fig9)

st.text('Inference :')

st.text('1. Carwidth, carlength and curbweight seems to have a poitive correlation with price.')
st.text('2. Carheight does not show any significant trend with price.')
st.write('')
st.write('')
st.write('')

st.header('Engine Size, Bore Ratio, Stroke, Compression Ratio, Horsepower, Peak rpm, Wheelbase, City mpg, Highway mpg')

def pp(x,y,z):
    sns.pairplot(cars, x_vars=[x,y,z], y_vars='price',size=4, aspect=1, kind='scatter')
    # plt.show()
    st.pyplot()

pp('enginesize', 'boreratio', 'stroke')
pp('compressionratio', 'horsepower', 'peakrpm')
pp('wheelbase', 'citympg', 'highwaympg')


st.text('Inference :')

st.text('1. Enginesize, boreratio, horsepower, wheelbase - seem to have a significant')
st.text('positive correlation with price.')
st.text('2. Citympg, highwaympg - seem to have a significant negative correlation with price.')
st.write('')
st.write('')
st.write('')

np.corrcoef(cars['carlength'], cars['carwidth'])[0, 1]

#Fuel economy
cars['fueleconomy'] = (0.55 * cars['citympg']) + (0.45 * cars['highwaympg'])

#Binning the Car Companies based on avg prices of each Company.
cars['price'] = cars['price'].astype('int')
temp = cars.copy()
table = temp.groupby(['CompanyName'])['price'].mean()
temp = temp.merge(table.reset_index(), how='left',on='CompanyName')
bins = [0,10000,20000,40000]
cars_bin=['Budget','Medium','Highend']
cars['carsrange'] = pd.cut(temp['price_y'],bins,right=False,labels=cars_bin)

fig10 = plt.figure(figsize=(10,4))
st.header('Fuel Economy')
plt.title('Fuel economy vs Price')
sns.scatterplot(x=cars['fueleconomy'],y=cars['price'],hue=cars['drivewheel'])
plt.xlabel('Fuel Economy')
plt.ylabel('Price')

plt.show()
plt.tight_layout()
st.write(fig10)

st.text('Inference :')

st.text('1. Fuel economy has an obvios negative correlation with price and is significant.')
st.write('')
st.write('')
st.write('')


st.header('Car Range')
df = pd.DataFrame(cars.groupby(['fuelsystem','drivewheel','carsrange'])['price'].mean().unstack(fill_value=0))
df.plot.bar(figsize=(10,4))
plt.title('Car Range vs Average Price')
plt.show()
st.pyplot()

st.text('Inference :')

st.text('1. High ranged cars prefer rwd drivewheel with idi or mpfi fuelsystem.')

