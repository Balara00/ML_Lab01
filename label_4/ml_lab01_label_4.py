# -*- coding: utf-8 -*-
"""ML_Lab01_label_4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1V8z3w9u4lXOgBO3b-ve6kpBc1eDkdWry

Import required packages and libraries
"""

import pandas as pd
import numpy as np

#constants
L1 = 'label_1'
L2 = 'label_2'
L3 = 'label_3'
L4 = 'label_4'

LABELS = [L1, L2, L3, L4]
AGE_LABEL = L2
FEATURES = [f"feature_{i}" for i in range (1,257)]

"""Importing dataset"""

from google.colab import drive
MOUNT_PATH='/content/drive'
drive.mount(MOUNT_PATH)

WORKING_DIR=f"{MOUNT_PATH}/MyDrive/ML_Lab 1"

train = pd.read_csv(f"{WORKING_DIR}/train.csv")
train.head()

valid = pd.read_csv(f"{WORKING_DIR}/valid.csv")
valid.head()

test = pd.read_csv(f"{WORKING_DIR}/test.csv")
test.head()

train[LABELS + [FEATURES[i] for i in range(0, 256, 32)]].describe()
train.info()

"""Scaling dataset"""

from sklearn.preprocessing import StandardScaler

x_train = {}
y_train = {}
x_valid = {}
y_valid = {}
x_test = {}
y_test = {}

for target_label in LABELS:
  train_ds = train[train['label_2'].notna()] if target_label == 'label_2' else train
  valid_ds = valid
  test_ds = test

  scaler = StandardScaler()
  x_train[target_label] = pd.DataFrame(scaler.fit_transform(train_ds.drop(LABELS, axis = 1)), columns=FEATURES)
  y_train[target_label] = train_ds[target_label]

  x_valid[target_label] = pd.DataFrame(scaler.transform(valid_ds.drop(LABELS, axis = 1)), columns=FEATURES)
  y_valid[target_label] = valid_ds[target_label]

  x_test[target_label] = pd.DataFrame(scaler.transform(test_ds.drop(LABELS, axis = 1)), columns=FEATURES)
  y_test[target_label] = test_ds[target_label]

y_train['label_2']

from sklearn.neighbors import KNeighborsClassifier

# Create a KNN classifier with a specified number of neighbors (e.g., n_neighbors=5)
clf = KNeighborsClassifier(n_neighbors=5)

# Fit the KNN model to the PCA-transformed features
clf.fit(x_train[L4], y_train[L4])

from sklearn import metrics

y_pred = clf.predict(x_valid[L4])
y_pred_test_before = clf.predict(x_test[L4])

print('Predicted labels before feature engineering:', y_pred_test_before)

print (metrics.confusion_matrix(y_valid[L4], y_pred))
print (metrics.accuracy_score(y_valid[L4], y_pred))
print (metrics.precision_score(y_valid[L4], y_pred, average="weighted"))
print (metrics.recall_score(y_valid[L4], y_pred, average="weighted"))

"""# Feature Engineering

### SelectKBest
"""

from sklearn.feature_selection import SelectKBest, f_classif

selector = SelectKBest(f_classif, k=75)
x_train_new = selector.fit_transform(x_train[L4], y_train[L4])
print("Shape: ", x_train_new.shape)

from sklearn.neighbors import KNeighborsClassifier

# Create a KNN classifier with a specified number of neighbors (e.g., n_neighbors=5)
clf = KNeighborsClassifier(n_neighbors=5)

# Fit the KNN model to the selected features
clf.fit(x_train_new, y_train[L4])


# Transform the validation data using the same feature selection
x_valid_selected = selector.transform(x_valid[L4])

# Make predictions on the validation set
y_pred = clf.predict(x_valid_selected)

# Evaluate the KNN classifier's performance
print(metrics.confusion_matrix(y_valid[L4], y_pred))
print(metrics.accuracy_score(y_valid[L4], y_pred))
print(metrics.precision_score(y_valid[L4], y_pred, average="weighted"))
print(metrics.recall_score(y_valid[L4], y_pred, average="weighted"))

"""### PCA"""

from sklearn.decomposition import PCA

pca = PCA(n_components=0.95, svd_solver='full')
pca.fit(x_train[L4])
x_train_trf = pd.DataFrame(pca.transform(x_train[L4]))
x_valid_trf = pd.DataFrame(pca.transform(x_valid[L4]))

print("Shape after PCA: ", x_train_trf.shape)

from sklearn.neighbors import KNeighborsClassifier

# Create a KNN classifier with a specified number of neighbors (e.g., n_neighbors=5)
clf = KNeighborsClassifier(n_neighbors=5)

# Fit the KNN model to the selected features
clf.fit(x_train_new, y_train[L4])


# Transform the validation data using the same feature selection
x_valid_selected = selector.transform(x_valid[L4])

# Make predictions on the validation set
y_pred = clf.predict(x_valid_selected)

# Evaluate the KNN classifier's performance
print(metrics.confusion_matrix(y_valid[L4], y_pred))
print(metrics.accuracy_score(y_valid[L4], y_pred))
print(metrics.precision_score(y_valid[L4], y_pred, average="weighted"))
print(metrics.recall_score(y_valid[L4], y_pred, average="weighted"))

"""### PCA with SelectKBest"""

from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.decomposition import PCA

# Step 1: Feature selection with SelectKBest
selector = SelectKBest(f_classif, k=50)
x_train_new = selector.fit_transform(x_train[L4], y_train[L4])

# Step 2: Apply PCA to the selected features
pca = PCA(n_components=0.95, svd_solver='full')
x_train_pca = pca.fit_transform(x_train_new)

print("Shape after PCA: ", x_train_pca.shape)

# Create a validation set with the same feature transformations
x_valid_new = selector.transform(x_valid[L4])
x_valid_pca = pca.transform(x_valid_new)

x_test_new = selector.transform(x_test[L4])
x_test_pca = pca.transform(x_test_new)

from sklearn.neighbors import KNeighborsClassifier

# Create a KNN classifier with a specified number of neighbors (e.g., n_neighbors=5)
clf = KNeighborsClassifier(n_neighbors=5)

# Fit the KNN model to the PCA-transformed features
clf.fit(x_train_pca, y_train[L4])

# Make predictions on the validation set
y_pred = clf.predict(x_valid_pca)

# Evaluate the KNN classifier's performance
print(metrics.confusion_matrix(y_valid[L4], y_pred))
print(metrics.accuracy_score(y_valid[L4], y_pred))
print(metrics.precision_score(y_valid[L4], y_pred, average="weighted"))
print(metrics.recall_score(y_valid[L4], y_pred, average="weighted"))

y_pred_test_after = clf.predict(x_test_pca)
print('Predicted labels before feature engineering:', y_pred_test_after)

"""**Output**"""

# output_df = pd.DataFrame({
#     'Predicted labels before feature engineering': y_pred_test_before,
#     'Predicted labels after feature engineering': y_pred_test_after,
#     'No. of new features': x_test_pca.shape[1]
# })


# for i in range(257):  # Looping from 0 to 256 inclusive
#     column_name = f'new_feature_{i+1}'  # Construct the column name

#     # Check if the feature exists in x_test_pca
#     if i < x_test_pca.shape[1]:
#         output_df[column_name] = x_test_pca[:, i]  # Fill with the feature data
#     else:
#         output_df[column_name] = None  # Fill with blank or NaN values


# output_df.head()

# Create the base DataFrame
output_df = pd.DataFrame({
    'Predicted labels before feature engineering': y_pred_test_before,
    'Predicted labels after feature engineering': y_pred_test_after,
    'No of new features': [x_test_pca.shape[1]] * len(y_pred_test_before)
})

# List to store all the new feature Series
new_features = []

# Extract new features from x_test_pca
for i in range(min(256, x_test_pca.shape[1])):
    column_name = f'new_feature_{i+1}'
    new_features.append(pd.Series(x_test_pca[:, i], name=column_name))

# If there are any remaining columns to reach 256, fill them with NaN
for i in range(x_test_pca.shape[1], 256):
    column_name = f'new_feature_{i+1}'
    new_features.append(pd.Series([None] * len(output_df), name=column_name))

# Concatenate all the new feature columns to output_df
output_df = pd.concat([output_df] + new_features, axis=1)

output_df.head()

# Save the DataFrame to the specified CSV file path
output_df.to_csv(f"{WORKING_DIR}/190572L_label_4_final.csv", index=False)

"""**Co-relation Matrix**"""

# Convert the PCA-transformed features (x_train_pca) to a Pandas DataFrame
x_train_pca_df = pd.DataFrame(x_train_pca)

# Calculate the correlation matrix
corr_matrix = x_train_pca_df.corr()
corr_matrix

import matplotlib.pyplot as plt
import seaborn as sns

corr_treshold = 0.5
filterred_correlation_matrix = corr_matrix[(corr_matrix > corr_treshold) | (corr_matrix < -corr_treshold)]
plt.figure(figsize=(10,8))
sns.heatmap(filterred_correlation_matrix, annot=True, cmap='coolwarm', center = 0)