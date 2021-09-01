def model_as_dict(model):
    dct = model.__dict__
    columns = {f.attname for f in model._meta.fields}
    return {column: dct[column] for column in columns if column in dct}
