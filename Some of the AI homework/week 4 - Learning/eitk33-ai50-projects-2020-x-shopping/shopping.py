import csv
import sys
import calendar

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - 0 Administrative, an integer
        - 1 Administrative_Duration, a floating point number
        - 2 Informational, an integer
        - 3 Informational_Duration, a floating point number
        - 4 ProductRelated, an integer
        - 5 ProductRelated_Duration, a floating point number
        - 6 BounceRates, a floating point number
        - 7 ExitRates, a floating point number
        - 8 PageValues, a floating point number
        - 9 SpecialDay, a floating point number
        - 10 Month, an index from 0 (January) to 11 (December)
        - 11 OperatingSystems, an integer
        - 12 Browser, an integer
        - 13 Region, an integer
        - 14 TrafficType, an integer
        - 15 VisitorType, an integer 0 (not returning) or 1 (returning)
        - 16 Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidance = []
    labels = []
    with open (filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            row[0] = int(row[0])
            row[1] = float(row[1])
            row[2] = int(row[2])
            row[3] = float(row[3])
            row[4] = int(row[4])
            row[5] = float(row[5])
            row[6] = float(row[6])
            row[7] = float(row[7])
            row[8] = float(row[8])
            row[9] = float(row[9])
            abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}
            abbr_to_num['June'] = 6

            row[10] = int(abbr_to_num[row[10]]) - 1
            row[11] = int(row[11])
            row[12] = int(row[12])
            row[13] = int(row[13])
            row[14] = int(row[14])
            if row[15] == 'Returning_Visitor':
                row[15] = 1
            else:
                row[15] = 0

            if row[16] == 'TRUE':
                row[16] = 1
            else:
                row[16] = 0


            if row[17] == 'FALSE':
                row[17] = 0
            else:
                row[17] = 1
            evidance.append(row[:17])
            labels.append(row[17])
    a = (evidance, labels)
    return a


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    knn = KNeighborsClassifier()
    knn.fit(evidence, labels)
    return knn

    raise NotImplementedError


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    correct = 0
    incorrect = 0
    total_pos = 0
    total_neg = 0
    for actual, predicted in zip(labels, predictions):
        if actual == 1:
            total_pos += 1
            if predicted == actual:
                correct += 1
        elif actual == 0:
            total_neg += 1
            if predicted == actual:
                incorrect += 1
    sensitivity = float(correct/total_pos)
    specificity = float(incorrect/total_neg)
    a = (sensitivity, specificity)
    return a

if __name__ == "__main__":
    main()
