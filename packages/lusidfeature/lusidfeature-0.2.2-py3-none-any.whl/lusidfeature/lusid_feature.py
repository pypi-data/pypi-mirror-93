from functools import wraps


def lusid_feature(*feature_codes):
    if len(feature_codes) < 1:
        raise ValueError("lusid_feature error: Decorator requires at least some input.")

    for feature_code in feature_codes:
        if type(feature_code) != str:
            raise ValueError("lusid_feature error: Decorator requires a string input parameter.")

        if feature_code == "":
            raise ValueError("lusid_feature error: Some decorated methods have no value passed. "
                             "Please make sure each lusid_feature decorator has a value code passed.")

    def decorator(decorated_method):
        if decorated_method is None:
            return

        @wraps(decorated_method)
        def wrapper(*method_args, **kwargs):
            return decorated_method(*method_args, **kwargs)

        wrapper.decorator_value = list(feature_codes)  # <-- store the feature
        return wrapper

    return decorator
