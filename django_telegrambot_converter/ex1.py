
def restrictions(limitter):
    def _restrictions(func):
        def wraps(a, b):
            success = limitter(a, b)
            if success:
                return func(a, b)
            return None
        return wraps
    return _restrictions


@restrictions(lambda x, y: x % 2 == 0 and y % 2 == 0)
def some_count(a, b):
    return a + b


