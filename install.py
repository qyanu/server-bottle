#!/usr/bin/env python3

# stlib
import getpass
import hashlib
import os
import pwd
import stat
# pipped
from logbook import notice


def writable_by_user(dirname, username):
    uid = 0
    try:
        uid = pwd.getpwnam(username).pw_uid
    except KeyError:
        print('[ERROR] User {} does not exist!'.format(username))
        return False

    dir_stat = os.stat(dirname)
    if ((dir_stat[stat.ST_UID] == uid) and
            (dir_stat[stat.ST_MODE] & stat.S_IWUSR)):
        return True

    return False


def writable_by_group(dirname, groupname):
    gid = 0
    try:
        gid = pwd.getpwnam(groupname).pw_gid
    except KeyError:
        print('[ERROR] Group {} does not exist!'.format(groupname))
        return False

    dir_stat = os.stat(dirname)
    if ((dir_stat[stat.ST_GID] == gid) and
            (dir_stat[stat.ST_MODE] & stat.S_IWGRP)):
        return True

    return False


def main():
    # ask for the upload directory (should be writable by the server)
    media_root = input("The directory where to put the pictures" +
                       " (should be writable by the server you use): ")
    if not os.path.isdir(media_root):
        notice("Directory {} does not exist, creating it".format(media_root))
        os.mkdir(media_root)

    # test for user writability of the directory
    server_user = input("Owner of the directory [www-data]: ")
    if not server_user:
        server_user = 'www-data'
    if not writable_by_user(media_root, server_user) and \
            not writable_by_group(media_root, server_user):
        print('[INFO] Directory {} is not writable by {}, check it!'
              .format(media_root, server_user))

    # ask a password for the server
    password = getpass.getpass(prompt='The server password: ')
    passhash = hashlib.sha512(password.encode('utf-8')).hexdigest()

    filename = 'photobackup_settings.py'
    with open(filename, 'w') as settings:
        settings.write("# generated settings for PhotoBackup Bottle server\n")
        settings.write("MEDIA_ROOT = '{}'\n".format(media_root))
        settings.write("PASSWORD = '{}'\n".format(passhash))


if __name__ == '__main__':
    main()
