rmdir /Q /S output
rmdir /Q /S model
rmdir /Q /S log_plain_nn

cntk configFile=plain_embedding.cntk dataDir=XXXX EMBEDDING_DIM=24 NUM_HIDDEN_NODES=9 MAX_EPOCHES=5  tensorBoardLogDir=log_plain_nn
REM tensorboard --logdir=log_plain_nn


python concate_file_vertically.py d:\XXXX\3cols_origin.tsv .\output\prediction.score .\output\final.tsv

python draw_precision_recall_and_auc_curve.py .\output\final.tsv .\output\pr.pdf .\output\auc.pdf 2 3 3 