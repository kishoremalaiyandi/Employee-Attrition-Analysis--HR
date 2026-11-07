import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             classification_report, confusion_matrix)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

def train_model(df, random_state=42):
    X, y = df.drop(columns=["Attrition"]), df["Attrition"].astype(int)
    numeric = X.select_dtypes(include=["number"]).columns.tolist()
    categorical = X.select_dtypes(exclude=["number"]).columns.tolist()
    numeric_pipe = Pipeline([("imputer", SimpleImputer(strategy="median"))])
    categorical_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))])
    prep = ColumnTransformer([
        ("num", numeric_pipe, numeric), ("cat", categorical_pipe, categorical)])
    model = Pipeline([
        ("prep", prep),
        ("rf", RandomForestClassifier(n_estimators=300, class_weight="balanced",
                                      min_samples_leaf=2, random_state=random_state,
                                      n_jobs=-1))])
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_state, stratify=y)
    model.fit(X_train, y_train)
    return model, X_test, y_test

def evaluate_model(model, X_test, y_test):
    pred = model.predict(X_test)
    metrics = {"accuracy": accuracy_score(y_test, pred),
               "precision": precision_score(y_test, pred, zero_division=0),
               "recall": recall_score(y_test, pred, zero_division=0)}
    return metrics, classification_report(y_test, pred, zero_division=0), confusion_matrix(y_test, pred, labels=[0,1])
