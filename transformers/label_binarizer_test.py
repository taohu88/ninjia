import pandas as pd
from sklearn.preprocessing import LabelBinarizer
import pickle


if __name__ == "__main__":
    df = pd.DataFrame([
           ['green', 'Chevrolet', 2017],
           ['blue', 'BMW', 2015],
           ['yellow', 'Lexus', 2018],
    ])
    df.columns = ['color', 'make', 'year']

    color_lb = LabelBinarizer()
    make_lb = LabelBinarizer()
    X = color_lb.fit_transform(df.color.values)
    print(f"X \n {X}")
    Xm = make_lb.fit_transform(df.make.values)

    pickle.dump(color_lb, open("color_lb.pickle", "wb"))
    color_lb2 = pickle.load(open("color_lb.pickle", "rb"))
    inv_X=color_lb2.inverse_transform(X)
    print(f"Inverse back \n {inv_X}")

    dfOneHot = pd.DataFrame(X, columns = ["Color_"+str(int(i)) for i in range(X.shape[1])])
    df = pd.concat([df, dfOneHot], axis=1)
    print(df.head())
