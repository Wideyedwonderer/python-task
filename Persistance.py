import configparser


def persist_by_id(id, collection_name, dict):
    file = configparser.ConfigParser()
    filename = collection_name + '.ini'

    file.read(filename)
    file[id] = dict

    with open(filename, 'w') as configfile:
        file.write(configfile)


def get_by_id(id, collection_name):
    file = configparser.ConfigParser()
    filename = collection_name + '.ini'

    file.read(filename)

    return dict(file[str(id)].items())


def remove_by_id(id, collection_name):
    file = configparser.ConfigParser()
    filename = collection_name + '.ini'

    file.read(filename)
    file.remove_section(str(id))

    with open(filename, 'w') as configfile:
        file.write(configfile)


def update_field(id, collection_name, field_name, field_value):
    file = configparser.ConfigParser()
    filename = collection_name + '.ini'

    file.read(filename)
    file[id][field_name] = str(field_value)

    with open(filename, 'w') as configfile:
        file.write(configfile)


def get_field(id, collection_name, field_name):
    file = configparser.ConfigParser()
    filename = collection_name + '.ini'

    file.read(filename)
    return file[str(id)][str(field_name)]


def get_all_ids_from_collection(collection_name):
    file = configparser.ConfigParser()
    filename = collection_name + '.ini'
    file.read(filename)
    return file.sections()
