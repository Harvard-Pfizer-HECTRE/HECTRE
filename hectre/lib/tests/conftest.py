

def pytest_collection_modifyitems(items):
    """
    Modifies tests in this directory to make them run in a given order,
    ex: I want test_hectre_init to run first, for obvious reason.
    """
    # Move up test_hectre_init first, since I want to run it second
    for i, item in enumerate(items):
        if item.module.__name__ == "tests.test_hectre_init":
            items.insert(0, items.pop(i))
            break

    # Now move up test_config_setup, since I want to run it first
    for i, item in enumerate(items):
        if item.module.__name__ == "tests.test_config_setup":
            items.insert(0, items.pop(i))
            break