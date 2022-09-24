import csv


def save_to_csv(jobs):
    file = open('listJobs.csv', mode='w')
    writer = csv.writer(file)
    writer.writerow(['title', 'company', 'location', 'link'])
    for job in jobs:
        writer.writerow(list(job.values()))




    return
