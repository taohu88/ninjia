import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import sys


def plotStreamDistributionsSingle(SavePath, Path):
    data    = pd.read_csv(Path, sep="\t", low_memory = False, names = ["Score", "Frequency"]).sort_values('Score').set_index('Score')
    NormalizedData= data / data.cumsum().max()
    Histogram = NormalizedData.cumsum()
    dataplot = data.plot(title = "Raw Distribution plot")
    histplot = Histogram.plot(title = "Cumulative Histogram plot")
    
    pp = PdfPages(SavePath)
    pp.savefig(dataplot.get_figure())
    pp.savefig(histplot.get_figure())
    pp.close()

def plotStreamDistributionsMultiple(SavePath, FirstPath, SecondPath, FirstLabel, SecondLabel):
    First    = pd.read_csv(FirstPath, sep="\t", low_memory = False, names = ["Score", "Frequency"]).sort_values('Score').set_index('Score')
    Second   = pd.read_csv(SecondPath, sep="\t", low_memory = False, names = ["Score", "Frequency"]).sort_values('Score').set_index('Score')
    data = pd.DataFrame.merge(First, Second, left_index=True, right_index=True, suffixes=[FirstLabel, SecondLabel])
    NormalizedData= data / data.cumsum().max()
    Histogram = NormalizedData.cumsum()
    diff = First - Second
    dataplot = data.plot(title = "Raw Distribution plot")
    histplot = Histogram.plot(title = "Cumulative Histogram plot")
    diffplot = diff.plot(title = "Raw Distribution Difference plot")
    
    pp = PdfPages(SavePath)
    pp.savefig(dataplot.get_figure())
    pp.savefig(histplot.get_figure())
    pp.savefig(diffplot.get_figure())
    pp.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit('Not enough arguments')
    if len(sys.argv) == 3:
        plotStreamDistributionsSingle(sys.argv[1], sys.argv[2])
    if len(sys.argv) == 6:
        SaveIn = sys.argv[1]
        FirstP = sys.argv[2]
        SecondP = sys.argv[3]
        FirstL = sys.argv[4]
        SecondL = sys.argv[5]
        plotStreamDistributionsMultiple(SaveIn, FirstP, SecondP, FirstL, SecondL)
    if len(sys.argv) > 6:
        sys.exit('Too many arguments')
