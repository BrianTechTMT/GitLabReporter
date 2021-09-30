This project is use for collecting report from GITLAB API
To get the report we will be using Python 3 script reportmain.py in folder projects

Requirements:
- Python 3 (3.9 as of the version of this script) installed
- Change the BASE_URL to your pipelines base url in projects/ReportMainModule.py
- If you have a GitLab token authentication header then please add them by editing the etc/default/telegraf

Use command line: 	python3 reportmain.py [-options,--long-options] (Pick below)
					   -h,--help (To get options help on terminal)
					   -m,--mock (To run mock test)
					   -l,--live (To run live test)

This script will give user result report from GITLAB for each new projects from each time there is a new pipeline report from the API
Report includes project ids, project names, report results, test counts, etc.
