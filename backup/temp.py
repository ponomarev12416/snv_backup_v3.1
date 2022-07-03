import sys
import os
import getopt
import stat
import re
import time
import shutil
import subprocess
from functools import cmp_to_key


# Path to svnlook utility
svnlook = r"svnlook"  # r"@SVN_BINDIR@/svnlook"

# Path to svnadmin utility
svnadmin = r"svnadmin"  # r"@SVN_BINDIR@/svnadmin"

def get_date_modified(repo_dir):
    """Examine the repository REPO_DIR using the svnlook binary
    specified by SVNLOOK, and return the date modified."""

    p = subprocess.Popen([svnlook, 'date', repo_dir],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         shell=True)
    infile, outfile, errfile = p.stdin, p.stdout, p.stderr

    stdout_lines = outfile.readlines()
    stderr_lines = errfile.readlines()
    outfile.close()
    infile.close()
    errfile.close()

    if stderr_lines:
        raise Exception("Unable to find the youngest revision for repository '%s'"
                        ": %s" % (repo_dir, stderr_lines[0].rstrip()))

    str_date = stdout_lines[0].decode('cp1251').strip().split(' ')
    str_date = ' '.join(str_date[0:2])
    return datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S')


if __name__ == "__main__":
    from datetime import datetime
    from dateutil import parser
    import time
    res = get_date_modified(r'D:\\Repositories\\trash\\repos')
    print(res)


def backup(*args, **kw):
    import time
    time.sleep(30)