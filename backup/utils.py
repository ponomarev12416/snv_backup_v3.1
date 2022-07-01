from .models import Job, Report, Track


from .backuper import backup as backup


def make_backups(*args):
    print(args)
    job: Job = Job.objects.get(pk=args[0])
    print(job)
    print(type(job))

    repo_pathes = [rep.path for rep in job.repositories.all()]
    report = init_report(job)
    for repo_path in repo_pathes:
        track: Track = Track.objects.get(report=report.id, repsository_path=repo_path)
        track.status = Track.RUNING
        track.save()
        backup(repo_path, job.destination)
        track.status = Track.COMPLETE
        track.save()


def init_report(job: Job):
    # Create initial report for current job
    print(job)
    print(type(job))
    print(job.id)
    report = Report.objects.create(job=job)
    for repo in job.repositories.all():
        Track.objects.create(
            report=report,
            destination_path=job.destination,
            repsository_path=repo)
    return report
    