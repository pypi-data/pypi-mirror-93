from automl_tools.functions.optimization_binary import best_search_tuning as best_search_binary_tuning
from automl_tools.functions.optimization_multi_class import best_search_tuning as best_search_multi_tuning
from automl_tools.functions.optimization_regression import best_search_tuning as best_search_regression_tuning
from automl_tools.functions.utils import target_count_class


def get_dataset_parameter(train, target, feature_name, model_name):
    global best_parameter_tuning

    model_type, _, _ = target_count_class(target)
    X = train[feature_name]
    y = target

    if model_type == "binary":
        print("binary", model_name)
        best_parameter_tuning = best_search_binary_tuning(model_name, X, y)
    elif model_type == "multi_class":
        print("multi_class", model_name)
        best_parameter_tuning = best_search_multi_tuning(model_name, X, y)
    elif model_type == "regression":
        print("regression", model_name)
        best_parameter_tuning = best_search_regression_tuning(model_name, X, y)

    return best_parameter_tuning
