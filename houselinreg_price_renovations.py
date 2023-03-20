# -*- coding: utf-8 -*-
"""HouseLinReg-Price-Renovations.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11UbtXijUMJ29XMZ6QsbWPY1gM0wkunRw
"""

import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

data = pd.read_csv('/content/raw_house_data.csv')

"""#Check data is loaded"""

print(data.head())

print(data.shape)

"""#Check missing values"""

# Check for missing values
missing_values = data.isnull().sum()

# Print the number of missing values for each column
print(missing_values)

"""#Fill missing values"""

# Fill in missing values in lot_acres with the median
median_lot_acres = data['lot_acres'].median()
data['lot_acres'].fillna(median_lot_acres, inplace=True)

# Fill in missing values in fireplaces with the mode
mode_fireplaces = data['fireplaces'].mode()[0]
data['fireplaces'].fillna(mode_fireplaces, inplace=True)

"""#Verify missing values are filled"""

# Verify that there are no more missing values
missing_values = data.isnull().sum()
print(missing_values)

"""###Double verification"""

print(data.isnull().sum())

"""#Check Data types"""

data.dtypes

"""#Created a class to treat data

##How to use:

Standard usage for my library:

**To instantiate the class**

- preprocessor = DataPreprocessor()

**Using the convert_to_int method**

 - preprocessor.convert_to_int(**dataframe**, '**column**')

 - By default this should also run the **check_non_numeric** as a sub method.

**Using the resolve_categorical method**

- preprocessor.resolve_categorical(**dataframe**, '**existing_column_name**')

- existing_column_name = dataframe['existing_column_name'].unique()

- data['new_column_name'] = data['existing_column_name'].map({feature: i for i, feature in enumerate(kitchen_features)})

**Using the round floats method**

- preprocessor.round_floats(**dataframe**, '**column**')

**Using scale_features**
- data_scaled = preprocessor.scale_features(**dataframe**, **list_of_columns**)

**Using remove_outliers**

- data_no_outliers = preprocessor.remove_outliers(**data_scaled_dataframe**, **list_of_columns**k, threshold=3)

**Using display_correlation_matrix method**

- data_processor.display_correlation_matrix(**list_of_columns**)
"""

#import pandas as pd
#import numpy as np
#import math
#import matplotlib.pyplot as plt

class DataPreprocessor:
    def __init__(self, data):
        self.data = data

    def remove_negative_sign(self, X):
        """
        Removes negative sign from numerical data.
        """
        X_copy = X.copy()
        if isinstance(X_copy, pd.Series):
            X_copy = X_copy.to_numpy().reshape(-1, 1)
        for i in range(X_copy.shape[1]):
            if np.issubdtype(X_copy[:, i].dtype, np.number):
                X_copy[:, i] = np.abs(X_copy[:, i])
        return X_copy

    def scale_features(self, data, columns, method='standardization'):
        """
        Scales or normalizes the features of a DataFrame.

        Parameters:
        - data: Pandas DataFrame containing the data.
        - columns: list of columns to scale or normalize.
        - method: scaling method to use. Can be 'standardization' or 'min-max'.

        Returns:
        - Pandas DataFrame with the scaled or normalized features.
        """
        # Make a copy of the data to avoid modifying the original DataFrame
        data_scaled = data.copy()

        # Scale or normalize the selected columns
        if method == 'standardization':
            for col in columns:
                data_scaled[col] = (data_scaled[col] - data_scaled[col].mean()) / data_scaled[col].std()

        elif method == 'min-max':
            for col in columns:
                data_scaled[col] = (data_scaled[col] - data_scaled[col].min()) / (data_scaled[col].max() - data_scaled[col].min())

        return data_scaled

    def remove_outliers(self, data, columns, threshold=2):
        """
        Removes outliers from a DataFrame using the z-score method.

        Parameters:
        - data: Pandas DataFrame containing the data.
        - columns: list of columns to check for outliers.
        - threshold: number of standard deviations from the mean to consider an outlier.

        Returns:
        - Pandas DataFrame without the outliers.
        """
        # Make a copy of the data to avoid modifying the original DataFrame
        data_clean = data.copy()

        # Iterate over the columns and remove outliers using the z-score method
        for col in columns:
            z_scores = np.abs((data_clean[col] - data_clean[col].mean()) / data_clean[col].std())
            data_clean = data_clean[z_scores <= threshold * data_clean[col].std()]

        return data_clean

    @staticmethod
    def check_non_numeric(data, column):
        # Select all rows in the column that cannot be converted to a numeric type
        non_numeric = data[pd.to_numeric(data[column], errors='coerce').isna()]

        # Check if there are any non-numeric values in the selected rows
        if len(non_numeric) > 0:
            # If there are non-numeric values, print them out
            print(f"Found non-numeric values in column '{column}':")
            print(non_numeric)
        else:
            # If there are no non-numeric values, print a message indicating so
            print(f"No non-numeric values found in column '{column}'")
            
    @staticmethod
    def resolve_categorical(data, column):
        # Check if the column has any missing values
        if data[column].isna().sum() > 0:
            # If there are missing values, drop them
            data.dropna(subset=[column], inplace=True)
        
        # Replace "None" with 0
        data[column] = data[column].replace("None", 0)
        
        # Count the categorical values
        cat_counts = data[column].value_counts().to_dict()

        # Replace the original values with their counts
        data[column] = data[column].map(cat_counts)

        # Verify the result
        print(data[column].unique())


    def convert_to_int(self, data, column):
        # Check for non-numeric values
        DataPreprocessor.check_non_numeric(data, column)

        # Replace "None" with NaN
        data[column] = data[column].replace("None", 0)

        # Convert the column to string
        data[column] = data[column].astype(str)

        # Remove commas from numbers
        data[column] = data[column].str.replace(",", "")

        # Convert the column to float
        data[column] = data[column].astype(float)

        # Replace NaN with 0
        data[column] = data[column].fillna(0)

        # Round down to the nearest integer
        data[column] = data[column].apply(lambda x: math.floor(x))

        # Convert to int
        data[column] = data[column].astype(int)

        # Verify the result
        print(data[column].unique())
        
    def convert_to_float(self, data, column):
        # Check for non-numeric values
        DataPreprocessor.check_non_numeric(data, column)

        # Replace "None" with NaN
        data[column] = data[column].replace("None", 0)


        # Convert the column to string
        data[column] = data[column].astype(str)

        # Remove commas from numbers
        data[column] = data[column].str.replace(",", "")

        # Check for non-numeric values
        DataPreprocessor.check_non_numeric(data, column)
        
        # Replace "None" with NaN
        data[column] = data[column].replace("None", np.nan)

        # Convert the column to float
        data[column] = data[column].astype(float)

        # Replace NaN with 0
        data[column] = data[column].fillna(0)

        # Verify the result
        print(data[column].unique())

    def round_floats(self, data, column):
        # Check if the column has any missing values
        if data[column].isna().sum() > 0:
            # If there are missing values, drop them
            data.dropna(subset=[column], inplace=True)
        
        # Round floats to 2 decimal points or add 0 if only one
        data[column] = data[column].apply(lambda x: '{:.2f}'.format(x) if isinstance(x, float) and x.is_integer() == False else '{:.2f}0'.format(x) if isinstance(x, float) and x.is_integer() else x)
        
        # Verify the result
        print(data[column].unique())

    def display_correlation_matrix(self, columns_to_check):
      
        # Calculate the correlation matrix
        correlation_matrix = self.data[columns_to_check].corr()

        fig, ax = plt.subplots(figsize=(10, 8))
        im = ax.imshow(correlation_matrix, cmap='coolwarm')

        # Display the colorbar
        cbar = ax.figure.colorbar(im, ax=ax)

        # Set the tick labels and axis labels
        ax.set_xticks(np.arange(len(columns_to_check)))
        ax.set_yticks(np.arange(len(columns_to_check)))
        ax.set_xticklabels(columns_to_check, fontsize=12)
        ax.set_yticklabels(columns_to_check, fontsize=12)
        ax.set_xlabel('Features', fontsize=14)
        ax.set_ylabel('Features', fontsize=14)

        # Rotate the tick labels and set their alignment
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
                 rotation_mode="anchor")

        # Display the correlation values in the heatmap
        for i in range(len(columns_to_check)):
            for j in range(len(columns_to_check)):
                text = ax.text(j, i, f'{correlation_matrix.iloc[i, j]:.2f}', ha="center", va="center", color="w", fontsize=10)

        # Set the title of the plot
        ax.set_title("Correlation Matrix", fontsize=16)

        # Show the plot
        plt.show()

"""#Instantiate Preprocessor"""

preprocessor = DataPreprocessor(data)

"""#Treating Data with preprocessor class

## remove minus values in sold price
"""

data['sold_price'] = preprocessor.remove_negative_sign(data['sold_price'])

"""##Price"""

preprocessor.round_floats(data, 'sold_price')

preprocessor.convert_to_float(data, 'sold_price')

"""##Year built"""

preprocessor.convert_to_int(data, 'year_built')

"""##Taxes"""

preprocessor.round_floats(data, 'taxes')

preprocessor.convert_to_float(data, 'taxes')

"""##Bathroom"""

preprocessor.convert_to_int(data, 'bathrooms')

"""##Garage"""

preprocessor.convert_to_int(data, 'garage')

"""##Sqrt_ft"""

preprocessor.convert_to_int(data, 'sqrt_ft')

"""##kitchen_features"""

# check the unique values present in the column and investigate if there are any non-numeric values
data['kitchen_features'].unique()

"""In the code below, we first assign the unique values of the kitchen_features column to the kitchen_features variable. Then we create a dictionary with the feature names as keys and their corresponding index as values. Finally, we use the map() method to replace each feature name with its index."""

# Example usage on kitchen_features column
preprocessor.resolve_categorical(data, 'kitchen_features')
kitchen_features = data['kitchen_features'].unique()
data['kitchen_features_values'] = data['kitchen_features'].map({feature: i for i, feature in enumerate(kitchen_features)})

"""##floor_covering"""

# check the unique values present in the column and investigate if there are any non-numeric values
data['floor_covering'].unique()

# Example usage on kitchen_features column
preprocessor.resolve_categorical(data, 'floor_covering')
floor_covering = data['floor_covering'].unique()
data['floor_covering_values'] = data['floor_covering'].map({feature: i for i, feature in enumerate(floor_covering)})

"""##HOA"""

preprocessor.convert_to_int(data, 'HOA')

"""#Checking data types after conversions"""

data.dtypes

"""#Check NaN

This line of code computes the number of missing (or NaN) values for each column in a pandas DataFrame called data.

First, the .isna() method is used to create a Boolean DataFrame where True indicates that the value in the original DataFrame is NaN, and False indicates that the value is not NaN.

Then, the .sum() method is called on the Boolean DataFrame, which will count the number of True values (i.e., the number of NaN values) for each column in the original DataFrame. The result is a Series object where each column name is associated with the number of NaN values in that column.
"""

data.isna().sum()

"""## Data types end

#Data description and dupes
"""

data.describe()

data.duplicated().sum()

"""#Column_definitions"""

# Specify the columns to check for outliers
columns_to_check = ['sold_price', 'lot_acres', 'taxes', 'bedrooms', 'bathrooms', 'sqrt_ft', 'garage', 'kitchen_features', 'fireplaces', 'floor_covering', 'HOA', 'kitchen_features_values', 'floor_covering_values']

# Scale or normalize the features
columns_to_scale = ['sold_price', 'lot_acres', 'taxes', 'year_built', 'sqrt_ft', 'fireplaces', 'floor_covering_values', 'bathrooms', 'bedrooms', 'garage']
data_scaled = preprocessor.scale_features(data, columns_to_scale)

"""#Visualise columns checked"""

fig, axs = plt.subplots(ncols=len(columns_to_check), figsize=(35,5))
for i, col in enumerate(columns_to_check):
  axs[i].boxplot(data[col].values)
  axs[i].set_title(col)

plt.show()

"""#Scale data"""

data_scaled = preprocessor.scale_features(data, columns_to_scale)

"""#Check for outliers start"""

data_scaled.info()

"""##Correlation Matrix prior to removing outliers"""

data_processor = DataPreprocessor(data_scaled)

data_processor.display_correlation_matrix(columns_to_check)

"""##Removing outliers"""

data_no_outliers = preprocessor.remove_outliers(data_scaled, columns_to_check, threshold=3)

"""##Checking outliers after outliers are removed"""

data_processor = DataPreprocessor(data_no_outliers)

data_processor.display_correlation_matrix(columns_to_scale)

print(data_no_outliers.info())

"""#Split the data in to train and test sets"""

import random
import matplotlib.pyplot as plt

#import random
#import matplotlib.pyplot as plt

def split_data(data_clean, train_pct):
    """
    Splits the data into training and testing sets.

    Parameters:
    - data: Pandas DataFrame containing the data.
    - train_pct: percentage of data to use for training (between 0 and 1).

    Returns:
    - tuple containing the training set and testing set as Pandas DataFrames.
    """
    # Shuffle the indices of the data
    indices = list(data_clean.index)
    random.shuffle(indices)

    # Split the indices into training and testing sets
    train_size = int(len(data_clean) * train_pct)
    train_indices = indices[:train_size]
    test_indices = indices[train_size:]

    # Split the data into training and testing sets using the indices
    train_data = data_clean.loc[train_indices]
    test_data = data_clean.loc[test_indices]

    return train_data, test_data

class MVLinearRegression():
    def fit(self, X, y, eta=1e-3, epochs=1e3, show_curve=False):
        self.D = X.shape[1]
        epochs = int(epochs)
        N, D = X.shape
        self.D = D
        Y = y

        # Initialise the weights
        self.W = np.random.randn(D)

        J = np.zeros(epochs)

        for epoch in range(epochs):
            Y_hat = self.predict(X)
            J[epoch] = self.OLS(Y, Y_hat, N)
            # weight update Rule:
            self.W -= eta * (1/N) * (X.T @ (Y_hat - Y))

        if show_curve:
            plt.figure()
            plt.plot(J)
            plt.xlabel("epochs")
            plt.ylabel("$\mathcal{J}$")
            plt.title("Training Curve")
            plt.show()

    def predict(self, X, renovation_cost=0):
        if X.shape[1] != self.D:
            raise ValueError(f"Expected input matrix with {self.D} columns, but got {X.shape[1]}")
        return (X @ self.W) + renovation_cost

    def OLS(self, y, y_hat, n):
        return (1/n) * np.sum((y - y_hat)**2)

# Split the data into training and testing sets
train_data, test_data = split_data(data_no_outliers, 0.8)

myreg = MVLinearRegression()

# Select the 10 columns we want to use for training and testing
selected_cols = ['sold_price', 'lot_acres', 'taxes', 'year_built', 'sqrt_ft', 'fireplaces', 'floor_covering_values', 'bathrooms', 'bedrooms', 'garage']
train_data_selected = train_data[selected_cols]
test_data_selected = test_data[selected_cols]

# Separate the features and target variables for training and testing data
X_train = train_data_selected.drop('sold_price', axis=1).values
y_train = train_data_selected['sold_price'].values
X_test = test_data[selected_cols].values
y_test = test_data['sold_price'].values

# Train the model
myreg.fit(X_train, y_train, show_curve=True)

# Remove outliers from the input data
renovation_cost = 50000
X_test_renovated = X_test.copy()  # make a copy of the test data
X_test_renovated[0, -1] = 1  # set the renovated feature to 1 for the first property
X_test = np.array([[2, 3, 2000, 3, 2, 3, 100, 1, 1, 1]])

# Remove outliers from the input data
renovation_cost = 50000
X_test[0, -1] = 1  # set the renovated feature to 1 for the first property

# Remove the renovated feature column
X_test = X_test[:, :-1]

# Make a prediction for a property with renovations
predicted_price_with_renovations = myreg.predict(X_test, renovation_cost)

print(f"The predicted price for the first property with renovations is ${float(predicted_price_with_renovations):,.2f}")

# Define the renovation description
renovation_description = "kitchen and bathroom remodel"

# Add a column for price after renovations
test_data_selected['price_after_renovations'] = np.nan

# Populate the price_after_renovations column with the new total cost of the house projected
for i, row in test_data_selected.iterrows():
    X_test = row[selected_cols[:-1]].values.reshape(1, -1)
    predicted_price_with_renovations = myreg.predict(X_test, renovation_cost)
    test_data_selected.at[i, 'price_after_renovations'] = predicted_price_with_renovations

np.random.seed(42) # Set random seed for reproducibility
sample_data = None

# Loop until sample_data contains 3 houses with sold_price > 0
while sample_data is None or (sample_data['sold_price'] <= 0).sum() > len(sample_data) - 3:
    sample_indices = np.random.choice(test_data_selected.index, size=3, replace=False)
    sample_data = test_data_selected.loc[sample_indices]

house1 = sample_data.iloc[0]
house2 = sample_data.iloc[1]
house3 = sample_data.iloc[2]

sold_price = sample_data['sold_price'].values

fig, ax = plt.subplots(figsize=(6,4))

# Bar plot for original sold prices (green)
ax.bar(np.arange(len(sample_data)) - 0.2, sold_price, width=0.4, color='g', label='Sold Price')

ax.set_xticks(np.arange(len(sample_data)))
ax.set_xticklabels(['House ' + str(i+1) for i in range(len(sample_data))])
ax.set_ylabel('Price')
ax.set_title('Sold Prices of Sample Houses')
ax.set_ylim(bottom=0) # Set lower y-limit to zero
ax.legend()

plt.show()

np.random.seed(42) # Set random seed for reproducibility
sample_data = None

# Loop until sample_data contains 3 houses with sold_price > 0
while sample_data is None or (sample_data['sold_price'] <= 0).sum() > len(sample_data) - 3:
    sample_indices = np.random.choice(test_data_selected.index, size=3, replace=False)
    sample_data = test_data_selected.loc[sample_indices]

# Get price after renovations for house1, house2, and house3
house1 = sample_data.iloc[0]['price_after_renovations']
house2 = sample_data.iloc[1]['price_after_renovations']
house3 = sample_data.iloc[2]['price_after_renovations']

price_after_renovations = [house1, house2, house3]

fig, ax = plt.subplots(figsize=(6,4))

# Bar plot for price after renovations (red)
ax.bar(np.arange(len(price_after_renovations)) - 0.2, price_after_renovations, width=0.4, color='r', label='Price after Renovations')

ax.set_xticks(np.arange(len(price_after_renovations)))
ax.set_xticklabels(['House 1', 'House 2', 'House 3'])
ax.set_ylabel('Price')
ax.set_title('Price After Renovations of Sample Houses')
ax.set_ylim(bottom=0) # Set lower y-limit to zero
ax.legend()

plt.show()

"""#Class example"""

from geopy import Nominatim

"""Give it user location"""

geolocator = Nominatim(user_agent = 'mAIstros')

"""variable name we are giving it"""

location = geolocator.geocode("1785 The Exchange SE, Atlanta")

"""Let's look at the location"""

location

"""look at the point"""

location.point

location = geolocator.geocode("10 Downing Street")

location

"""calc location point"""

print("Latitude: {}, Longitude: {}".format(location.point.latitude, location.point.longitude))

"""#Old code that is now object oriented"""

#non_numeric = data[pd.to_numeric(data['bathrooms'], errors='coerce').isna()]
#print(non_numeric)

#Replace "None" with NaN
#data['sqrt_ft'] = data['sqrt_ft'].replace("None", np.nan)

#Convert the columns to float
#data['sqrt_ft'] = data['sqrt_ft'].astype(float)

#Replace NaN with 0
#data['sqrt_ft'] = data['sqrt_ft'].fillna(0)

#Round down to the nearest integer
#data['sqrt_ft'] = data['sqrt_ft'].apply(lambda x: math.floor(x))

#Convert to int
#data['sqrt_ft'] = data['sqrt_ft'].astype(int)

#Replace "None" with NaN
#data['garage'] = data['garage'].replace("None", np.nan)

#Convert the columns to float
#data['garage'] = data['garage'].astype(float)

#Replace NaN with 0
#data['garage'] = data['garage'].fillna(0)

#Round down to the nearest integer
#data['garage'] = data['garage'].apply(lambda x: math.floor(x))

#Convert to int
#data['garage'] = data['garage'].astype(int)

# Replace "None" with NaN
#data['bathrooms'] = data['bathrooms'].replace("None", np.nan)

# Convert the 'bathrooms' column to float
#data['bathrooms'] = data['bathrooms'].astype(float)

# Replace NaN with 0
#data['bathrooms'] = data['bathrooms'].fillna(0)

# Round down to the nearest integer
#data['bathrooms'] = data['bathrooms'].apply(lambda x: math.floor(x))

# Convert to int
#data['bathrooms'] = data['bathrooms'].astype(int)

# Verify the result
#print(data['bathrooms'].unique())

#def kitchen_features_count(features):
#    return len(features.split(','))

#data['kitchen_features'].value_counts()

# Create a new column with the counts
#data['kitchen_features_count'] = data['kitchen_features'].map(kitchen_features_count)

# Calculate the correlation matrix
#correlation_matrix = data.corr()

#fig, ax = plt.subplots(figsize=(10, 8))
#im = ax.imshow(correlation_matrix, cmap='coolwarm')

# Display the colorbar
#cbar = ax.figure.colorbar(im, ax=ax)

# Set the tick labels and axis labels
#ax.set_xticks(np.arange(len(columns_to_check)))
#ax.set_yticks(np.arange(len(columns_to_check)))
#ax.set_xticklabels(columns_to_check, fontsize=12)
#ax.set_yticklabels(columns_to_check, fontsize=12)
#ax.set_xlabel('Features', fontsize=14)
#ax.set_ylabel('Features', fontsize=14)

# Rotate the tick labels and set their alignment
#plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         #rotation_mode="anchor")

# Display the correlation values in the heatmap
#for i in range(len(columns_to_check)):
    #for j in range(len(columns_to_check)):
      #text = ax.text(j, i, f'{correlation_matrix.iloc[i, j]:.2f}', ha="center", va="center", color="w", fontsize=10)

# Set the title of the plot
#ax.set_title("Correlation Matrix", fontsize=16)

# Show the plot
#plt.show()