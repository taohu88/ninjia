import sys
import pandas as pd
import numpy as np
import math
from sklearn.metrics import precision_recall_curve


if __name__ == "__main__":
    #arg 1
    in_file = sys.argv[1]
    columns = sys.argv[2]
    true_col = sys.argv[3]
    score_col = sys.argv[4]
    out_file = sys.argv[5]
    num_of_scales = int(sys.argv[6])
    print('Num of scale is %d' % num_of_scales)
    factor = math.pow(10, num_of_scales)

    columns = ''.join(columns.split())
    columns = columns.split(',')
    print('Columns are %s' % columns)
    df = pd.read_csv(in_file, sep='\t', names=columns, encoding='utf-8')

    y_true = df[true_col]
    #this will dramatically reduce number of threholds
    y_score = (df[score_col] * factor).astype(np.int64)

    precision, recall, thresholds = precision_recall_curve(
        y_true, y_score)
    print('Number of thresholds is %d' % len(thresholds))

    data = {
        'precision': precision[:-1],
        'recall': recall[:-1],
        'thresholds': thresholds / factor
    }

    out_df = pd.DataFrame(data=data)
    out_df.to_csv(out_file, sep='\t', index=False)
