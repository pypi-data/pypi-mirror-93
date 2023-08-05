# ml_prepare
Repository containing functions for preprocessing data for machine learning projects.

# Installation

```pip install mlprep-ls```

# Import module

```import mlprepare as mlp``` 

# How to use it

```
data = {'PassengerId': {0: 1, 1: 2, 2: 3, 3: 4, 4: 5},
                 'Survived': {0: 0, 1: 1, 2: 1, 3: 1, 4: 0},
                 'Sex': {0: 'male', 1: 'female', 2: 'female', 3: 'female', 4: 'male'},
                 'Age': {0: 22.0, 1: 38.0, 2: 26.0, 3: 35.0, 4: 35.0},
                 'Cabin': {0: np.NaN, 1: 'C85', 2: np.NaN, 3: 'C123', 4: np.NaN},
                 'Fake_date': {0: '1995-04-01T00:00:00.000000000',
                  1: '1998-10-27T00:00:00.000000000',
                  2: '1997-03-05T00:00:00.000000000',
                  3: '1999-11-30T00:00:00.000000000',
                  4: '1994-02-01T00:00:00.000000000'}}

df = pd.DataFrame(data)

date_type = ['Fake_date']
continuous_type = ['Age', 'PassengerId']
categorical_type = ['Sex', 'Cabin', 'Survived']

ml_instance = mlp.MLPrepare()
result = ml_instance.df_to_type(df, date_type, continuous_type, categorical_type)
```
