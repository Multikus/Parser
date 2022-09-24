from headhunter import hh_get_jobs
from save import save_to_csv


hh_output_jobs = hh_get_jobs()


# списки можно объеденить для этого
# jobs = hh_output_jobs + so_get_jobs
# #so_get_jobs это такая же функция, как  и  hh_output_jobs

save_to_csv(hh_output_jobs)
