def loadData( filename ):

    import json

    with open(filename) as data_file:
        jsondata = json.load(data_file)

    assert isinstance(jsondata, object)
    return jsondata
