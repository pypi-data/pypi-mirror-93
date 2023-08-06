import optuna
import pandas as pd
from lightgbm import LGBMRegressor
from lightgbm import LGBMClassifier
from xgboost import XGBRegressor
from xgboost import XGBClassifier
from optuna.samplers import TPESampler
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import ExtraTreeRegressor
from sklearn.tree import ExtraTreeClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import BaggingRegressor
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import AdaBoostRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import KNeighborsRegressor

from .metrics import rmsle, rmse


def rf_params(trial):
    return {
        'min_samples_leaf': trial.suggest_int("min_samples_leaf", 1, 15),
        'min_samples_split': trial.suggest_uniform("min_samples_split", 0.05, 1.0),
        'n_estimators': trial.suggest_int("n_estimators", 2, 300),
        'max_depth': trial.suggest_int("max_depth", 2, 15),
        'random_state': 666
    }


def xgboost_params(trial):
    return {
        'learning_rate': trial.suggest_uniform("learning_rate", 0.0000001, 2),
        'n_estimators': trial.suggest_int("n_estimators", 2, 800),
        'max_depth': trial.suggest_int("max_depth", 2, 20),
        'gamma': trial.suggest_uniform('gamma', 0.0000001, 1),
        'random_state': 666
    }


def lgb_params(trial):
    return {
        'learning_rate': trial.suggest_uniform('learning_rate', 0.0000001, 1),
        'n_estimators': trial.suggest_int("n_estimators", 1, 800),
        'max_depth': trial.suggest_int("max_depth", 2, 25),
        'num_leaves': trial.suggest_int("num_leaves", 2, 3000),
        'min_child_samples': trial.suggest_int('min_child_samples', 3, 200),
        'random_state': 666
    }


def dt_params(trial):
    return {
        'max_depth': trial.suggest_int("max_depth", 2, 15),
        'min_samples_split': trial.suggest_int('min_samples_split', 2, 20),
        'min_weight_fraction_leaf': trial.suggest_uniform('min_weight_fraction_leaf', 0.0, 0.5),
        'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 15),
        'random_state': 666
    }


def et_params(trial):
    return {
        'min_samples_leaf': trial.suggest_int("min_samples_leaf", 1, 15),
        'min_samples_split': trial.suggest_uniform("min_samples_split", 0.05, 1.0),
        'max_depth': trial.suggest_int("max_depth", 2, 25),
        'random_state': 666
    }


def bagg_params(trial):
    return {
        'n_estimators': trial.suggest_int('n_estimators', 2, 300),
        'max_samples': trial.suggest_int('max_samples', 1, 200),
        'random_state': 666
    }


def kn_params(trial):
    return {
        'n_neighbors': trial.suggest_int("n_neighbors", 2, 100)
    }


def ada_params(trial):
    return {
        'n_estimators': trial.suggest_int("n_estimators", 2, 800),
        'learning_rate': trial.suggest_uniform('learning_rate', 0.0001, 1.0)
    }


models = {

    # Gradient Boosts
    'XGBR': lambda trial: XGBRegressor(**xgboost_params(trial)),
    'XGBC': lambda trial: XGBClassifier(**xgboost_params(trial)),
    'LGBR': lambda trial: LGBMRegressor(**lgb_params(trial)),
    'LGBC': lambda trial: LGBMClassifier(**lgb_params(trial)),

    # Trees
    'RFR': lambda trial: RandomForestRegressor(**rf_params(trial)),
    'RFC': lambda trial: RandomForestClassifier(**rf_params(trial)),
    'DTR': lambda trial: DecisionTreeRegressor(**dt_params(trial)),
    'DTC': lambda trial: DecisionTreeClassifier(**dt_params(trial)),
    'ETR': lambda trial: ExtraTreeRegressor(**et_params(trial)),
    'ETC': lambda trial: ExtraTreeClassifier(**et_params(trial)),

    # Ensemble
    'BC': lambda trial: BaggingClassifier(**bagg_params(trial)),
    'BR': lambda trial: BaggingRegressor(**bagg_params(trial)),
    'ADAR': lambda trial: AdaBoostRegressor(**ada_params(trial)),
    'ADAC': lambda trial: AdaBoostClassifier(**ada_params(trial)),

    # KNeighbors
    'KNC': lambda trial: KNeighborsClassifier(**kn_params(trial)),
    'KNR': lambda trial: KNeighborsRegressor(**kn_params(trial))
}

scorers = {
    'acc': accuracy_score,
    'f1': f1_score,
    'rmse': rmse,
    'rmsle': rmsle
}


def optimize(model_name, path, scorer, y_label, trials=30, sampler=TPESampler(seed=666), direction='maximize'):
    ds = pd.read_csv(path)
    X_ds, y_ds = ds.drop(y_label, axis=1), ds[y_label]
    X_train, X_val, y_train, y_val = train_test_split(X_ds, y_ds)

    def objective(trial):
        model = models[model_name](trial)
        model.fit(X_train, y_train)
        preds = model.predict(X_val)
        return scorers[scorer](y_val, preds)

    study = optuna.create_study(direction=direction, sampler=sampler)
    study.optimize(objective, n_trials=trials)
    return study.best_params
