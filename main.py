from headhunter import extract_max_page, extract_block_vacancy

hh_max_page = extract_max_page()
hh_jobs = extract_block_vacancy(hh_max_page)# результат присвоили в переменную чтобы вывести его

print(hh_jobs)