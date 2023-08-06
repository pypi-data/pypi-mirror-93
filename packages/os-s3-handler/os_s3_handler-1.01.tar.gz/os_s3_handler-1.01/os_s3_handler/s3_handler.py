import os
from os_s3_handler.bp import _res
from os_tools import tools


########################################################################
# this module meant to provide general handling functions for AWS's S3 #
########################################################################

def download_all_by_extension(bucket_name, rel_path_to_dir, extension, dst_path, recursive):
    """
    Will download all of the files with to the same extension from an S3 path.

    :param bucket_name the name of the S3 bucket
    :param rel_path_to_dir the local path of the files in the bucket (/remotes/Samsung)
    :param dst_path the path to which the files will be downloaded
    :param extension the extension you wish to look for
    :param recursive set to true if you want to download from sub dirs as well
    NOTICE: IT'S IMPERATIVE TO SET THIS ARG AS THE SHITTY S3 CLI DOESN'T INFORM WHEN IT IS DONE DOWNLOADING FILES.
    """
    rel_path_to_dir = _build_s3_path(bucket_name, rel_path_to_dir)
    include_cmd = f'{_res.CMD_INCLUDE_PREFIX} "*{extension}"'
    exclude_cmd = f'{_res.CMD_EXCLUDE_PREFIX} "*"'
    conditions_full_cmd = f'{exclude_cmd} {include_cmd}'
    if not recursive:
        exclude_cmd = f'{_res.CMD_EXCLUDE_PREFIX} "*/*"'
        conditions_full_cmd = f'{include_cmd} {exclude_cmd}'
    copy_command = f'{_res.CMD_PREFIX} {_res.CMD_COPY} "{_res.CMD_PATH_PREFIX}{rel_path_to_dir}" "{dst_path}"'
    params_command = f'--recursive {conditions_full_cmd}'
    full_command = f'{copy_command} {params_command}'

    tools.run_command(full_command)


def download_file(bucket_name, rel_path_to_search, file_name, dst_dir_path):
    """
    Will download a file from an S3 path.

    :param bucket_name the name of the S3 bucket
    :param rel_path_to_search -> the local path to look for the file in
    :param file_name -> the file name incl the extension you wish to look for
    :param dst_dir_path -> the path to which the files will be downloaded
    """
    search_path = _build_s3_path(bucket_name, rel_path_to_search)

    include_cmd = f'{_res.CMD_INCLUDE_PREFIX} "{file_name}"'
    exclude_cmd = f'{_res.CMD_EXCLUDE_PREFIX} "*"'
    conditions_full_cmd = f'{exclude_cmd} {include_cmd}'
    copy_command = f'{_res.CMD_PREFIX} {_res.CMD_COPY} "{_res.CMD_PATH_PREFIX}{search_path}"  "{dst_dir_path}"'
    params_command = f'--recursive {conditions_full_cmd}'
    full_command = f'{copy_command} {params_command}'
    tools.run_command(full_command)


def _build_s3_path(bucket_name, rel_path):
    if rel_path.startswith('/'):
        rel_path = rel_path[1:]
    rel_path = f'{bucket_name}/{rel_path}'
    if rel_path.endswith('/'):
        rel_path = rel_path[:len(rel_path) - 2]
    return rel_path
