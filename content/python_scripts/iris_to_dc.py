
import pandas as pd
from sklearn import datasets

col_names=['SEPAL_LENGTH', 'SEPAL_WIDTH', 'PETAL_LENGTH', 'PETAL_WIDTH']

iris = datasets.load_iris()
iris_df = pd.DataFrame(iris.data, columns=col_names)

iris_df.to_json(orient='records')


