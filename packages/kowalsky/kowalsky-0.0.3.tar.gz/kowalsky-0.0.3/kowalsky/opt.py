import optuna
import pandas as pd
from optuna.samplers import TPESampler
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from .metrics import rmsle, rmse


def create_rf_model(trial):
    return RandomForestRegressor(
        min_samples_leaf=trial.suggest_int("min_samples_leaf", 1, 15),
        min_samples_split=trial.suggest_uniform("min_samples_split", 0.05, 1.0),
        n_estimators=trial.suggest_int("n_estimators", 2, 300),
        max_depth=trial.suggest_int("max_depth", 2, 15),
        random_state=666
    )


def create_xgboost_model(trial):
    return XGBRegressor(
        learning_rate=trial.suggest_uniform("learning_rate", 0.0000001, 2),
        n_estimators=trial.suggest_int("n_estimators", 2, 800),
        max_depth=trial.suggest_int("max_depth", 2, 20),
        gamma=trial.suggest_uniform('gamma', 0.0000001, 1),
        random_state=666
    )


def create_lgb_model(trial):
    return LGBMRegressor(
        learning_rate=trial.suggest_uniform('learning_rate', 0.0000001, 1),
        n_estimators=trial.suggest_int("n_estimators", 1, 800),
        max_depth=trial.suggest_int("max_depth", 2, 25),
        num_leaves=trial.suggest_int("num_leaves", 2, 3000),
        min_child_samples=trial.suggest_int('min_child_samples', 3, 200),
        random_state=666
    )


models = {
    'RFR': create_rf_model,
    'XGBR': create_xgboost_model,
    'LGB': create_lgb_model
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
