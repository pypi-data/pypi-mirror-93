# Automl_tools: automl binary classification


[![Github License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Updates](https://pyup.io/repos/github/woctezuma/google-colab-transfer/shield.svg)](pyup)
[![Python 3](https://pyup.io/repos/github/woctezuma/google-colab-transfer/python-3-shield.svg)](pyup)
[![Code coverage](https://codecov.io/gh/woctezuma/google-colab-transfer/branch/master/graph/badge.svg)](codecov)




Automl_tools is a Python library that implements Gradient Boosting
## Installation

The code is packaged for PyPI, so that the installation consists in running:
```sh
pip install automl-tools
```

## Colab

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/10DFkSmzMO1GqLX-mgBWfDjS9OIVmEy6O?usp=sharing)


## Usage

Probabilistic binary example on the Boston housing dataset:

```python
import pandas as pd
from automl_tools import automl_run

train = pd.read_csv("https://raw.githubusercontent.com/jonaqp/automl_tools/main/automl_tools/examples/train.csv?token=AAN2ZBDWF77QITK4ARSFIFDABUGAU")
test = pd.read_csv("https://raw.githubusercontent.com/jonaqp/automl_tools/main/automl_tools/examples/test.csv?token=AAN2ZBD6TMUC5XSGRTJNVPDABUGCO")

automl_run(train=train,
           test=test,
           id_col=None, 
           target_col="Survived",
           imp_num="knn",
           imp_cat="knn",
           processing="binding",
           mutual_information=False,
           correlation_drop=False,
           model_feature_selection=None,
           model_run="LR",
           augmentation=True,
           Stratified=True,
           cv=5)







```

## Parameter
```sh
imp_num : "gaussian", "arbitrary", "median", "mean", "random", "knn"
imp_cat : "frequent", "constant", "rare", "knn"
processing:  "woe", "binding" 
```

## Support Binary
```sh
model_feature_selection: 
    default: ["LR", "RF", "LGB"]
        LR  : LogisticRegression
        RF  : RandomForestClassifier
        SVM : SVC
        LS  : LASSO
        RD  : RIDGE
        NET : Elasticnet
        DT  : DecisionTreeClassifier
        ET  : ExtraTreesClassifier
        GB  : GradientBoostingClassifier
        AB  : AdaBoostClassifier
        XGB  : XGBClassifier
        LGB  : LGBMClassifier
        CTB  : CatBoostClassifier
        NGB  : NGBClassifier

model_run:
    default: "LR"
        LR  : LogisticRegression
        RF  : RandomForestClassifier
        SVM : SVC
        LS  : LASSO
        RD  : RIDGE
        NET : Elasticnet
        DT  : DecisionTreeClassifier
        ET  : ExtraTreesClassifier
        GB  : GradientBoostingClassifier
        AB  : AdaBoostClassifier
        XGB  : XGBClassifier
        LGB  : LGBMClassifier
        CTB  : CatBoostClassifier
        NGB  : NGBClassifier
```

## License

[Apache License 2.0](https://www.dropbox.com/s/8t6xtgk06o3ij61/LICENSE?dl=0).


## New features v1.0
 * multi_class
 * regression
 * integrations GCP deploy model CI/CD
 * integrations AWS deploy model CI/CD
 
## BugFix
 - 0.1.5
   - fix imputer
   - fix space hyperparameter
   - update catboost test
   
 - 0.1.4
   - add parameter cv
   - add confusion Matrix
   - add comments readme.txt
   
 - 0.1.3
   - add parameter id_col
   - add comments readme.txt



## Reference

 - Jonathan Quiza [github](https://github.com/jonaqp).
 - Jonathan Quiza [RumiMLSpark](http://rumi-ml.herokuapp.com/).
 - Jonathan Quiza [linkedin](https://www.linkedin.com/in/jonaqp/).

