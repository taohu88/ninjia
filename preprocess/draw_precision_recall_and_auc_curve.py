import sys
import math
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import precision_recall_curve, average_precision_score


def save_auc_figure(fpr, tpr, score, file_name):
    plt.figure()

    lw = 2
    plt.plot(fpr, tpr, color='darkorange',
             lw=lw, label='ROC curve (area = %0.2f)' % score)

    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")

    plt.savefig(file_name, format='pdf')
    plt.close()


def save_pr_curve(precision, recall, avg_precision, file_name):
    f = plt.figure()

    plt.step(recall, precision, color='b', alpha=0.2, where='post')
    plt.fill_between(recall, precision, step='post', alpha=0.2, color='b')

    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])
    plt.title('2-class Precision-Recall curve: AUC={0:0.2f}'.format(
        avg_precision))
    plt.legend(loc="lower right")

    plt.savefig(file_name, format='pdf')
    plt.close()


if __name__ == "__main__":
    #arg 1
    in_file = sys.argv[1]
    precision_recall_file = sys.argv[2]
    auc_file = sys.argv[3]

    true_col = int(sys.argv[4])
    score_col = int(sys.argv[5])

    num_of_scales = 3
    if len(sys.argv) > 6:
        num_of_scales = int(sys.argv[6])
    print('Num of scale is %d' % num_of_scales)
    factor = math.pow(10, num_of_scales)

    df = pd.read_csv(in_file, sep='\t', header=None, quoting=csv.QUOTE_NONE, encoding='utf-8')

    y_true = df.iloc[:, true_col].astype(np.int64)
    #this will dramatically reduce number of threholds
    y_score = (df.iloc[:, score_col] * factor).astype(np.int64)

    #Average PR
    avg_precision = average_precision_score(y_true, y_score)
    print('Average precision is %f' % avg_precision)

    precision, recall, thresholds = precision_recall_curve(
        y_true, y_score)

    print('Number of thresholds is %d' % len(thresholds))
    save_pr_curve(precision, recall, avg_precision, precision_recall_file)

    fpr, tpr, threholds = roc_curve(y_true, y_score)
    auc_score = auc(fpr, tpr)
    print('Auc score is %f' % auc_score)

    save_auc_figure(fpr, tpr, auc_score, auc_file)




