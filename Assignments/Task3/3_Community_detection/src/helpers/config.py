## function to make the model information readable, model_type to the list of files corresponding models
def paths_dict() -> dict:
    """Returns a dictionary with the models of each type."""
    model_info = {
        "MODEL": "./data/model/",
        "REAL": "./data/real/",
        "TOY": "./data/toy/",
    }
    return model_info
