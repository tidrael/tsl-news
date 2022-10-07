import csv

label_mapping = {"negative": 0, "neutral": 1, "positive": 2}

with open("train.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        label = label_mapping[row["label"]]
        print(label)
        break