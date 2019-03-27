from collections import defaultdict
from sklearn.base import BaseEstimator, TransformerMixin


class CategoryGrouper(BaseEstimator, TransformerMixin):
    """A tranformer for combining low count observations for categorical features.

    This transformer will preserve category values that are above a certain
    threshold, while bucketing together all the other values. This will fix issues
    where new data may have an unobserved category value that the training data
    did not have.
    """

    def __init__(self, threshold=0.05):
        """Initialize method.

        Args:
            threshold (float): The threshold to apply the bucketing when
                categorical values drop below that threshold.
        """
        self.d = defaultdict(list)
        self.threshold = threshold

    def transform(self, X, **transform_params):
        """Transforms X with new buckets.

        Args:
            X (obj): The dataset to pass to the transformer.

        Returns:
            The transformed X with grouped buckets.
        """
        X_copy = X.copy()
        for col in X_copy.columns:
            X_copy[col] = X_copy[col].apply(lambda x: x if x in self.d[col] else 'CategoryGrouperOther')
        return X_copy

    def fit(self, X, y=None, **fit_params):
        """Fits transformer over X.

        Builds a dictionary of lists where the lists are category values of the
        column key for preserving, since they meet the threshold.
        """
        df_rows = len(X.index)
        for col in X.columns:
            calc_col = X.groupby(col)[col].agg(lambda x: (len(x) * 1.0) / df_rows)
            self.d[col] = calc_col[calc_col >= self.threshold].index.tolist()
        return self


if __name__ == "__main__":
    import pandas as pd

    cgr = CategoryGrouper(threshold=0.1)
    colors = 3*['red'] + 11 * ['green'] + 5 *['blue'] + ['yellow']
    print(f"Colors = {colors}")
    df = pd.DataFrame.from_dict({'color': colors})
    print(df.head())

    X = cgr.fit_transform(df)
    print(X)