
import io, yaml



def dict_fetchone(cursor):

    '''Returns all rows from a cursor as a dict'''
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def is_number(string):
    is_string_number = True
    try:
        if str.lower(string) in ['nan', 'inf']:
            is_string_number = False
        else:
            num = float(string)
    except ValueError:
        is_string_number = False
    return is_string_number


def testcase_to_yml(path, yaml_dict):
    with io.open(path, 'a', encoding='utf-8') as stream:
        yaml.dump(yaml_dict, stream, encoding='utf-8')


def isset_var(var):
    try:
        var
    except NameError:
        var_exists = False
    else:
        var_exists = True
    return var_exists


