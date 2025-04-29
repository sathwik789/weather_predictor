from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)
#HI this is my DOCKER PROJECT
# Load and preprocess data
df = pd.read_csv("weatherHistory.csv")
df = df[["Precip Type", "Temperature (C)", "Humidity", "Wind Speed (km/h)"]]
df["Precip Type"] = df["Precip Type"].fillna("Sunny")
df.drop_duplicates(inplace=True)
df.dropna(inplace=True)

features = ["Temperature (C)", "Humidity", "Wind Speed (km/h)"]
scaler = StandardScaler()
df[features] = scaler.fit_transform(df[features])
df["Precip Type"] = df["Precip Type"].astype("category")

X = df[features]
y = df["Precip Type"]
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=123)
labels = y.cat.categories

@app.route("/", methods=["GET", "POST"])
def index():
    knn_accuracy = nb_accuracy = 0
    if request.method == "POST":
        k = int(request.form["k_value"])

        # KNN
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(X_train, y_train)
        knn_pred = knn.predict(X_test)
        knn_accuracy = accuracy_score(y_test, knn_pred)
        knn_cm = confusion_matrix(y_test, knn_pred, labels=labels)

        # Naive Bayes
        nb = GaussianNB()
        nb.fit(X_train, y_train)
        nb_pred = nb.predict(X_test)
        nb_accuracy = accuracy_score(y_test, nb_pred)
        nb_cm = confusion_matrix(y_test, nb_pred, labels=labels)

        # Plot accuracy bar chart
        acc_df = pd.DataFrame({"Model": ["KNN", "Naive Bayes"],
                               "Accuracy": [knn_accuracy * 100, nb_accuracy * 100]})
        sns.set(style="whitegrid")
        plt.figure(figsize=(6, 4))
        sns.barplot(x="Model", y="Accuracy", data=acc_df, palette=["lightblue", "orange"])
        plt.ylim(0, 100)
        plt.title("Model Accuracy Comparison")
        plt.savefig("static/accuracy.png")
        plt.close()

        # Confusion matrix - KNN
        plt.figure(figsize=(5, 4))
        sns.heatmap(knn_cm, annot=True, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels)
        plt.title("KNN Confusion Matrix")
        plt.xlabel("Predicted")
        plt.ylabel("Actual")
        plt.savefig("static/knn_cm.png")
        plt.close()

        # Confusion matrix - Naive Bayes
        plt.figure(figsize=(5, 4))
        sns.heatmap(nb_cm, annot=True, fmt="d", cmap="Oranges", xticklabels=labels, yticklabels=labels)
        plt.title("Naive Bayes Confusion Matrix")
        plt.xlabel("Predicted")
        plt.ylabel("Actual")
        plt.savefig("static/nb_cm.png")
        plt.close()

    return render_template("index.html", knn_acc=knn_accuracy, nb_acc=nb_accuracy)

if __name__ == "__main__":
    if not os.path.exists("static"):
        os.makedirs("static")
    app.run(debug=True, host='0.0.0.0')
