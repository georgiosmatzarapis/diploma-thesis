""" Module which contains helper functions. """
import os


def file_path(folder_name, file_name):
    """ Specify file path. """
    file_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.dirname(file_directory)
    file_path = os.path.join(parent_directory, f'{folder_name}/{file_name}')
    return file_path
