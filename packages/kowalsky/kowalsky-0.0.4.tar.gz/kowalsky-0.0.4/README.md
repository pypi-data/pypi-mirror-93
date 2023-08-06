# Kowalsky, analysis!

A simple package for handful ML things and more.

What's inside?

1. ```analysis``` - method for evaluation of specified model with
   given dataframe. With ```export_test_set=False``` it exports
   ready for submission predictions.
   
2. df - working with dataframe:
    * ```corr``` - sort all correlated features.
    * ```handle_outliers``` - fill or drop columns with outliers.
    * ```log_transform``` - transform columns with log function.
    * ```group_by_mean``` - make additional columns with aggregated mean
    * ```group_by_max``` - make additional columns with aggregated max
    * ```group_by_min``` - make additional columns with aggregated min
    * ```scale``` - scale columns with Standard of MinMax scalers
    
3. kag:
    * ```submit``` - make submit-file for kaggle based on sample
    
4. metrics:
    *  ```rmse``` - RMSE scorer
    *  ```rmsle``` - RMSLE scorer
    
5. opt - handful methods for working with optuna:
    * ```optimize``` - optimize model with given dataframe
   
## Example:
```
!pip install kowalsky --upgrade
from kowalsky.opt import optimize
optimize('RFR',
         path='../input/project/feed.csv',
         scorer='acc',
         y_label='y_label',
         trials=3000)
```