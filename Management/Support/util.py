import io
import yaml
import os


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
    yaml_dict = [yaml_dict]
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


def yml_file(contect):
    return '{}.yml'.format(contect)


def join_yaml_file(path, contect):
    return os.path.join(path, yml_file(contect))


def new_a_file(new_file, mode='a'):
    if not os.path.exists(new_file):
        with io.open(new_file, mode) as f:
            pass



