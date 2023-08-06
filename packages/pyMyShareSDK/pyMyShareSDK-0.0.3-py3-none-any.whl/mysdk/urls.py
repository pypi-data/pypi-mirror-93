
class URLs():
    def __init__(self):
        self.base = "https://api.myshare.today/"

        # get inforamtion
        self.get_jobs = "getJobs"

        # add information
        self.create_job = "createJob"

        # edit information
        self.update_job = "updateJob"

        # delete information
        self.delete_job = "deleteJob"

    def get_jobs_url(self):
        return self.base + self.get_jobs

    def create_job_url(self):
        return self.base + self.create_job

    def update_job_url(self):
        return self.base + self.update_job

    def delete_job_url(self):
        return self.base + self.delete_job

