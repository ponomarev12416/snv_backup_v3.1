from .models import JobRun, Report


from .backuper import backup as backup


def make_backups(dest, *args):
    for rep in args:
        backup(rep, dest)


def make_report():
    pass