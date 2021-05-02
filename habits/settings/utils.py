import os
import subprocess

from django.core.exceptions import ImproperlyConfigured


no_default_provided = dict()


def get_environ_setting(key, default=no_default_provided):
    """ Get the environment variable or raise exception """
    try:
        return os.environ[key]
    except KeyError:
        if default is no_default_provided:
            error_msg = f'Set the {key} environment variable'
            raise ImproperlyConfigured(error_msg)
        else:
            return default


def get_last_git_commit_hash(git_repo_root):
    # The combination of celery, the new relic agent, and calling out to git
    # raises an AttributeError. Since we don't need the git commit hash while
    # we are inside of a Celery process, let's try to get the hash, and
    # move on if we don't.
    # https://github.com/15five/fifteen5/issues/6833
    # todo: remove this method once we are on docker
    try:
        out = subprocess.check_output(
            'git rev-parse HEAD',
            cwd=git_repo_root,
            shell=True,
        )
        out = out.decode().strip()
    except Exception:
        out = 'git-hash-is-not-defined'
    return out

