import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def loaddata():

    df = pd.read_csv(PROJECT_DIR+"\\cropandyield\\AgrcultureDataset.csv")
    # ================================================================
    states = df['State_Name']
    states = states.drop_duplicates()

    # ================================================================
    seasons = df['Season']
    seasons = seasons.drop_duplicates()

    # ================================================================
    crops = df['Crop']
    crops = crops.drop_duplicates()

    return states,seasons,crops

def forecast(State_Name,Season,Crop,Area):

    test = pd.DataFrame({"State_Name": [State_Name],
                         "Season": [Season],
                         "Crop": [Crop],
                         "Area": [Area]})

    print(test)
    test = pd.get_dummies(test)
    print(test)

    df = pd.read_csv(PROJECT_DIR+"\\cropandyield\\\\AgrcultureDataset.csv")

    print(df.shape)
    df['Production'] = pd.to_numeric(df['Production'], errors='coerce')
    data = df.dropna()
    print(df.shape)

    sum_maxp = data["Production"].sum()
    data["percent_of_production"] = data["Production"].map(lambda x: (x / sum_maxp) * 100)

    print(df.shape)

    data1 = data.drop(["District_Name", "Crop_Year"], axis=1)
    data_dum = pd.get_dummies(data1)

    x = data_dum.drop("Production", axis=1)
    y = data_dum[["Production"]]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)

    print("x_train :", x_train.shape)
    print("x_test :", x_test.shape)
    print("y_train :", y_train.shape)
    print("y_test :", y_test.shape)

    def common_member(x_train, x_test):
        a_set = set(x_train.columns.tolist())
        b_set = set(x_test.columns.tolist())
        if (a_set & b_set):
            return list(a_set & b_set)

    com_fea = common_member(x_train, test)
    print(len(com_fea))

    model = RandomForestRegressor()
    model.fit(x_train[com_fea], y_train)
    preds = model.predict(test[com_fea])
    print(preds)

    return preds[0]