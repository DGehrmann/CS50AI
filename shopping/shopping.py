import csv
import sys

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
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    with open(filename) as file:
        # table = csv.DictReader(file)
        
        table = csv.reader(file)
        headers = next(table)
        evidence = [row[:17] for row in table]
        
    
    with open(filename) as file:
        table = csv.reader(file)
        headers = next(table)
        labels = [row[17] for row in table]
        

    dict_headers_column_no = {}
    for column_no, header in enumerate(headers):
        dict_headers_column_no[header] = column_no

    int_columns = [
        "Administrative", "Informational", "ProductRelated",
        "Month", "OperatingSystems", "Browser", "Region", 
        "TrafficType", "VisitorType", "Weekend"
        ]
    
    dict_months = {
        "Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, 
        "June":6, "Jul":7, "Aug":8, "Sep":9, "Oct":10, 
        "Nov":11, "Dec":12
        }
    
    for col in headers[:17]:
        j = dict_headers_column_no[col]
        for i in range(len(evidence)):
            entry = evidence[i][j]
            if col in int_columns:  
                try: 
                    entry = int(entry)
                except ValueError:
                    if col == "Month":
                        entry = int(dict_months[entry] - 1)
                    elif col == "VisitorType":
                        if entry == "Returning_Visitor":
                            entry = int(1)
                        else:
                            entry = 0
                    else: # key == "Weekend"
                        if entry == "TRUE":
                            entry = int(1)
                        else: 
                            entry = 0
            else:
                entry = float(entry)
            evidence[i][j] = entry
    
    for i, entry in enumerate(labels):
        if entry == "TRUE":
            entry = int(1)
        else:
            entry = 0
        labels[i] = entry

    # print(evidence[0])
    # print(labels[0])
    
    return (evidence, labels)

    # raise NotImplementedError


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """

    model = KNeighborsClassifier(n_neighbors=1)
    return model.fit(evidence, labels)

    # raise NotImplementedError


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
    # print(labels)
    # print(predictions[0])
    count_identified_sensitivity = 0
    count_positive_labels = 0
    count_identified_specificity = 0
    count_negative_labels = 0
    for i in range(len(labels)):
        if labels[i] == 1:
            if predictions[i] == 1:
                count_identified_sensitivity += 1
                count_positive_labels += 1
            else:
                count_positive_labels += 1
        else:
            if predictions[i] == 0:
                count_identified_specificity += 1
                count_negative_labels += 1
            else:
                count_negative_labels += 1
    
    sensitivity = float(count_identified_sensitivity / count_positive_labels)
    specitivity = float(count_identified_specificity / count_negative_labels)

    return (sensitivity, specitivity)

    # raise NotImplementedError


if __name__ == "__main__":
    main()
