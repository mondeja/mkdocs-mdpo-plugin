import os


def remove_empty_directories_from_dirtree(dirpath):
    """Remove empty directories walking through all nested subdirectories.

    Args:
        dirpath (str): Top directory tree path.
    """
    for root, dirs, files in os.walk(dirpath, topdown=False):
        if not os.listdir(root):
            os.rmdir(root)


def remove_file_and_parent_dir_if_empty(filepath):
    """Remove a file and the directory that contains it if it is empty.

    Args:
        filepath (str): Path of the file to remove.

    Raises:
        FileNotFoundError: the file doesn't exists.
    """
    os.remove(filepath)

    parent_dir = os.path.abspath(os.path.dirname(filepath))
    if not os.listdir(parent_dir):
        os.rmdir(parent_dir)
