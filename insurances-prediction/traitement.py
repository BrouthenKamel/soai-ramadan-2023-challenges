def treat(data_train, categorical_cols, numerical_cols):

    numerical_cols = numerical_cols.remove("Claim")

    data_train["Building_Painted"].replace({"N":1, "V":0}, inplace=True)
    data_train["Building_Fenced"].replace({"N":1, "V":0}, inplace=True)
    data_train["Garden"].replace({"V":1, "O":0}, inplace=True)
    data_train["Settlement"].replace({"R":1, "U":0}, inplace=True)

    data_train["NumberOfWindows"].replace({
    ".":0,
    "1":1,
    "2":2,
    "2.0":2
    "3":3,
    "4":4,
    "5":5,
    "6":6,
    "7":7,
    "8":8,
    "9":9,
    ">=10":10}, inplace=True)

    data_train.loc[data_train["NumberOfWindows"]==0, "NumberOfWindows"] = 4.33

    data_train["Geo_Code"].value_counts().to_dict()

    for key, value in data_train["Geo_Code"].value_counts().to_dict().items():
        if value < 30:
            data_train.loc[data_train["Geo_Code"] == key, "Geo_Code"] = "rare"
        elif value > 30 and value < 100:
            data_train.loc[data_train["Geo_Code"] == key, "Geo_Code"] = "common"
        else:
            data_train.loc[data_train["Geo_Code"] == key, "Geo_Code"] = "frequent"

    data_train['Insured_Period'] = data_train['Insured_Period'].map(lambda x: '1_year' if x == 1 else 'less_than_year')
    data_train['Insured_Period'] = data_train['Insured_Period'].astype('object')

    data_train["Building Dimension"] = data_train["Building Dimension"].map(
    lambda x: 'small' if x < 1500 else 'medium' if x > 4000 else 'large' )

    data_train['Date_of_Occupancy'] = data_train['Date_of_Occupancy'].fillna(1960)

    data_train['Date_of_Occupancy'] = data_train['Date_of_Occupancy'].map(
        lambda x: 'before_1900' if x < 1900 else '1900-1950' if x < 1950 else '1950-1980' if x < 1980 else '1980-2000' if x < 2000 else 'after_2000' )
    
    data_train["NumberOfWindows"] = data_train["NumberOfWindows"] / 10
    data_train["YearOfObservation"] = ( data_train["YearOfObservation"] - 1545) / (2016 - 1545)
    
    data_train['Building_Type'] = data_train['Building_Type'].astype(str)

    X_test = pd.concat([data_train["Customer Id"], pd.get_dummies(data_train[categorical_cols]), data_train[numerical_cols]], axis=1)

    return X_test