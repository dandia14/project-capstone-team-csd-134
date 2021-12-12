# -*- coding: utf-8 -*-
"""Project_Capstone_134.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vOblb5SbWTkvPjPX8pvNKcs-iB_0zyrC

# Model Algoritma Sistem Diagnosa Penyakit Diabetes pada Wanita

## Tema Proyek

Dalam proyek kali ini, kita memilih tema Kesehatan Diri dan Mental. Adapun latar belakang kenapa Kita memilih tema ini, antara lain :
- Bidang kesehatan sering dijumpai dalam kegiatan sehari-hari terutama dalam pelayanan kesehatan.
- Dalam pelayanan kesehatan juga sangat berkaitan dengan data-data pasien untuk mendiagnosis penyakit.
- Dari data-data pasien tersebut, kita dapat mengetahui bagaimana cara memastikan jenis penyakit diabetes dengan cepat dan tepat.

## Business Understanding

Diabetes adalah penyakit kronis yang terjadi baik ketika pankreas tidak menghasilkan cukup insulin atau ketika tubuh tidak dapat secara efektif menggunakan insulin atau hormon yang mengatur gula darah yang dihasilkannya. Berdasarkan data WHO pada tahun 2019, diabetes merupakan penyebab kematian kesembilan dengan perkiraan 1,5 juta kematian secara langsung disebabkan oleh diabetes. Melalui penelitian yang dilakukan oleh BMJ Diabetes Research & Care, wanita yang bekerja 45 jam atau lebih dalam seminggu dikaitkan dengan risiko diabetes.

Bayangkan jika Anda seorang petugas medis yang bertugas untuk mengecek data pasien di sebuah perusahaan yang bergerak di bidang jasa pelayanan kesehatan. Pekerjaan ini berhubungan dengan banyak data-data pasien, sehingga memerlukan waktu untuk memastikan pasien benar-benar terjangkit penyakit diabetes. Untuk efisiensi, kami ingin menerapkan automasi pada sistem dalam memprediksi penyakit diabetes dengan teknik predictive modelling.

### Problem Statement

- Teknik predictive apakah yang tepat untuk menentukan penyakit diabetes?
- Apakah dengan dibuatkan sistem diagnosa penyakit diabetes ini hasil akhirnya akan akurat untuk mendiagnosis penyakit ?

### Goals

- Membuat model machine learning yang dapat memprediksi penyakit diabetes dengan tepat.
- Mengetahui bagaimana hasil akhir sistem diagnosa penyakit diabetes.

### Solution statements

- **Boosting Algorithm**, Metode ini bekerja dengan membangun model dari data latih. Kemudian ia membuat model kedua yang bertugas memperbaiki kesalahan dari model pertama. Model ditambahkan sampai data latih terprediksi dengan baik atau telah mencapai jumlah maksimum model untuk ditambahkan.

- **Decision Tree**, adalah salah satu algoritma supervised learning yang dapat dipakai untuk masalah klasifikasi dan regresi. Decision tree merupakan algoritma yang powerful alias mampu dipakai dalam masalah yang kompleks.

- **K-Nearest Neighbor**, adalah algoritma yang relatif sederhana dibandingkan dengan algoritma lain. Algoritma KNN menggunakan ‘kesamaan fitur’ untuk memprediksi nilai dari setiap data yang baru. Dengan kata lain, setiap data baru diberi nilai berdasarkan seberapa mirip titik tersebut dalam set pelatihan.

- **Random Forest**, salah satu algoritma supervised learning. Ia dapat digunakan untuk menyelesaikan masalah klasifikasi dan regresi. Random forest juga merupakan algoritma yang sering digunakan karena cukup sederhana tetapi memiliki stabilitas yang mumpuni.

- **Support Vector Machines (SVM)**, adalah model ML multifungsi yang dapat digunakan untuk menyelesaikan permasalahan klasifikasi, regresi, dan pendeteksian outlier. Termasuk ke dalam kategori supervised learning, SVM adalah salah satu metode yang paling populer dalam machine learning.

## Data Understanding
"""

# Commented out IPython magic to ensure Python compatibility.
# library yang di butuhkan
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# %matplotlib inline
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import mean_squared_error, accuracy_score
import pickle

# load the dataset
url = 'https://raw.githubusercontent.com/dandia14/project-capstone-team-csd-134/ml/dataset/diabetes.csv'
diabetes = pd.read_csv(url)
diabetes.head()

# Mengecek informasi dataset dengan fungsi info()
diabetes.info()

# Mengecek deskripsi statistik data dengan fitur describe()
diabetes.describe()

"""### Menangani Missing Value"""

diabetes.isnull().sum()

# Mengetahui missing value
glucose = (diabetes.Glucose == 0).sum()
bloodPressure = (diabetes.BloodPressure == 0).sum()
skinThickness = (diabetes.SkinThickness == 0).sum()
insulin = (diabetes.Insulin == 0).sum()
bmi = (diabetes.BMI == 0).sum()
diabetesPedigreeFunction = (diabetes.DiabetesPedigreeFunction == 0).sum()
age = (diabetes.Age == 0).sum()

print("Nilai 0 di kolom Glucose ada: ", glucose)
print("Nilai 0 di kolom BloodPressure ada: ", bloodPressure)
print("Nilai 0 di kolom SkinThickness ada: ", skinThickness)
print("Nilai 0 di kolom Insulin ada: ", insulin)
print("Nilai 0 di kolom BMI ada: ", bmi)
print("Nilai 0 di kolom DiabetesPedigreeFunction ada: ", diabetesPedigreeFunction)
print("Nilai 0 di kolom Age ada: ", age)

# Mengganti nilai 0 dengan NaN pada Glucose, Blood Pressure, Skin Thickness, Insulin, BMI
cols = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]
for col in cols:
    diabetes[col].replace(0,np.NaN,inplace=True)

# Mengganti nilai NaN dengan nilai median sesuai target Outcome
for col in diabetes.columns:
    diabetes.loc[(diabetes["Outcome"]==0) & (diabetes[col].isnull()),col] = diabetes[diabetes["Outcome"]==0][col].median()
    diabetes.loc[(diabetes["Outcome"]==1) & (diabetes[col].isnull()),col] = diabetes[diabetes["Outcome"]==1][col].median()

# Mengecek kembali missing value
glucose = (diabetes.Glucose == 0).sum()
bloodPressure = (diabetes.BloodPressure == 0).sum()
skinThickness = (diabetes.SkinThickness == 0).sum()
insulin = (diabetes.Insulin == 0).sum()
bmi = (diabetes.BMI == 0).sum()

print("Nilai 0 di kolom Glucose ada: ", glucose)
print("Nilai 0 di kolom BloodPressure ada: ", bloodPressure)
print("Nilai 0 di kolom SkinThickness ada: ", skinThickness)
print("Nilai 0 di kolom Insulin ada: ", insulin)
print("Nilai 0 di kolom BMI ada: ", bmi)

diabetes.head()

# Mengecek kembali deskripsi statik data maka akan terlihat berbeda dengan sebelumnya
diabetes.describe()

"""### Menangani Outliers"""

sns.boxplot(x=diabetes['Pregnancies'])

sns.boxplot(x=diabetes['Glucose'])

sns.boxplot(x=diabetes['BloodPressure'])

sns.boxplot(x=diabetes['SkinThickness'])

sns.boxplot(x=diabetes['Insulin'])

sns.boxplot(x=diabetes['BMI'])

sns.boxplot(x=diabetes['DiabetesPedigreeFunction'])

sns.boxplot(x=diabetes['Age'])

Q1 = diabetes.quantile(0.25)
Q3 = diabetes.quantile(0.75)
IQR=Q3-Q1
diabetes=diabetes[~((diabetes<(Q1-1.5*IQR))|(diabetes>(Q3+1.5*IQR))).any(axis=1)]
 
# Cek ukuran dataset setelah kita drop outliers
diabetes.shape

numerical_features = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"]
categorical_features = ['Outcome']

# Menampilkan jumlah sample pada outcome
feature = categorical_features[0]
count = diabetes[feature].value_counts()
percent = 100*diabetes[feature].value_counts(normalize=True)
df = pd.DataFrame({'jumlah sampel':count, 'persentase':percent.round(1)})
print(df)
count.plot(kind='bar', title=feature);

# Menampilkan berbagai fitur berdasarkan Outcome
cols = diabetes[numerical_features]
for col in cols:
  sns.catplot(x="Outcome", y=col, data=diabetes, kind="bar")

# mengamati hubungan antar fitur numerik dengan fungsi pairplot()
sns.pairplot(diabetes, diag_kind = 'kde')

plt.figure(figsize=(10, 8))
correlation_matrix = diabetes.corr().round(2)
# annot = True to print the values inside the square
sns.heatmap(data=correlation_matrix, annot=True, cmap='gray', linewidths=0.5, )
plt.title("Correlation Matrix untuk Fitur Numerik ", size=20)

diabetes.corr()["Outcome"].sort_values(ascending=False)

"""## Data Preparation"""

X = diabetes.drop(['Outcome'], axis=1)
y = diabetes['Outcome']

# Membagi dataset menjadi data latih (train) dan data uji (test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

"""Standarisasi dengan menggunakan teknik StandarScaler dari library Scikitlearn"""

scaler = StandardScaler()
X_train[numerical_features] = scaler.fit_transform(X_train.loc[:, numerical_features])
X_train[numerical_features].head()

X_train[numerical_features].describe().round(4)

"""Perhatikan tabel di atas, sekarang nilai mean = 0 dan standar deviasi = 1

## Modeling
"""

# Siapkan dataframe untuk analisis model
models = pd.DataFrame(index=['train_mse', 'test_mse'], 
                      columns=['DecisionTree', 'SVM', 'RandomForestClassification', 'KNeighborsClassification', 'AdaBoostClassifier'])

# membuat model Decision Tree
decisiontree = DecisionTreeClassifier() 
# melakukan pelatihan model terhadap data
decisiontree.fit(X_train, y_train)
y_pred_decisiontree = decisiontree.predict(X_train)

# membuat model SVM
svm = SVC()
# melakukan pelatihan model terhadap data
svm.fit(X_train, y_train)
y_pred_svm = svm.predict(X_train)

# membuat model Random Forest Classification
rfc = RandomForestClassifier()
# melakukan pelatihan model terhadap data
rfc.fit(X_train, y_train)
models.loc['train_mse','RandomForestClassification'] = mean_squared_error(y_pred=rfc.predict(X_train), y_true=y_train)

# membuat model KNeighbors Classification
knnc = KNeighborsClassifier()
# melakukan pelatihan model terhadap data
knnc.fit(X_train, y_train)
y_pred_knnc = knnc.predict(X_train)

# membuat model AdaBoost Classifier
adaboost = AdaBoostClassifier()
# melakukan pelatihan model terhadap data                        
adaboost.fit(X_train, y_train)
models.loc['train_mse','AdaBoostClassifier'] = mean_squared_error(y_pred=adaboost.predict(X_train), y_true=y_train)

"""## Evaluation"""

# untuk proses scaling
X_test.loc[:, numerical_features] = scaler.fit_transform(X_test[numerical_features])

mse = pd.DataFrame(columns=['train', 'test'], index=['DecisionTree', 'SVM', 'RandomForestClassification', 'KNeighborsClassification', 'AdaBoostClassifier'])
model_dict = {'DecisionTree': decisiontree, 'SVM': svm, 'RandomForestClassification': rfc, 'KNeighborsClassification': knnc, 'AdaBoostClassifier':adaboost}
for name, model in model_dict.items():
    mse.loc[name, 'train'] = mean_squared_error(y_true=y_train, y_pred=model.predict(X_train))/1e3 
    mse.loc[name, 'test'] = mean_squared_error(y_true=y_test, y_pred=model.predict(X_test))/1e3
 
mse

fig, ax = plt.subplots()
mse.sort_values(by='test', ascending=False).plot(kind='barh', ax=ax, zorder=3)
ax.grid(zorder=0)

"""Dari gambar di atas, terlihat bahwa model Random Forest Classifier memberikan nilai eror yang paling kecil. Model inilah yang mungkin akan kita pilih sebagai model terbaik untuk melakukan prediksi penyakit diabetes."""

prediksi = X_test.iloc[30:35].copy()
pred_dict = {'y_true':y_test[30:35]}
for name, model in model_dict.items():
    pred_dict['prediksi_'+name] = model.predict(prediksi)
 
pd.DataFrame(pred_dict)

"""Dari gambar di atas, terlihat semua model memberikan hasil prediksi yang cukup tepat."""

score = pd.DataFrame(columns=['train', 'test'], index=['DecisionTree', 'SVM', 'RandomForestClassification', 'KNeighborsClassification', 'AdaBoostClassifier'])
model_dict = {'DecisionTree': decisiontree, 'SVM': svm, 'RandomForestClassification': rfc, 'KNeighborsClassification': knnc, 'AdaBoostClassifier':adaboost}
for name, model in model_dict.items():
    score.loc[name, 'train'] = model.score(X_train, y_train)
    score.loc[name, 'test'] = model.score(X_test, y_test)
 
score

fig, ax = plt.subplots()
score.sort_values(by='test').plot(kind='barh', ax=ax, zorder=3)
ax.grid(zorder=0)

"""## Tunning Parameter

"""

diabetes.head()

# Number of trees in random forest
n_estimators = [int(x) for x in np.linspace(start = 10, stop = 100, num = 10)]
# Number of faetures to consider at every split
max_features = ['auto', 'sqrt', 'log2']
# Maximun number of levels in tree
max_depth = [2, 4]
# Minimum number of samples required to split a node
min_samples_leaf = [1, 2]
# Method of selecting samples for training each tree
bootstrap = [True, False]

# Create the param grid
param_grid = {'n_estimators': n_estimators,
              'max_features': max_features,
              'max_depth': max_depth,
              'min_samples_leaf': min_samples_leaf,
              'bootstrap': bootstrap}
print(param_grid)

rfc_tunning = GridSearchCV(estimator = rfc, param_grid = param_grid, cv = 3, verbose = 2, n_jobs = -1)

rfc_tunning.fit(X_train, y_train)

rfc_tunning.best_params_

y_pred = rfc_tunning.predict(X_train)
print(accuracy_score(y_train, y_pred))

y_pred = rfc_tunning.predict(X_test)
print(accuracy_score(y_test, y_pred))

print(f'Train Score : {rfc_tunning.score(X_train, y_train):.3f}')
print(f'Test Score : {rfc_tunning.score(X_test, y_test):.3f}')