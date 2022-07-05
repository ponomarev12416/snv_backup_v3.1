import os
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


def scan_for_repos(path):
    from .models import Repository
    for obj in os.listdir(path):
        full_path = os.path.join(path, obj)
        if (os.path.islink(full_path) 
            and not Repository.objects.filter(path=full_path)):
            Repository.objects.create(name=obj, path=full_path)

def time_converter(total_seconds):
    total_seconds = int(total_seconds)
    minutes_per_hour = 60
    hours = total_seconds // minutes_per_hour
    seconds_per_minute = 60
    minutes = (total_seconds - (hours * minutes_per_hour)) // seconds_per_minute
    return f'{hours}:{minutes:02d}'



def backup(*args, **kw):
    import time
    time.sleep(30)