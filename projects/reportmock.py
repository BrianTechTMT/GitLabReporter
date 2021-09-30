import json

from ReportMainModule import GitLabReportMock
from ReportUtilityModule import ReportUtils


def run():
    live_request = GitLabReportMock()
    existing_id = live_request.get_existing_id()
    projects_urls = live_request.get_projects_url_paths()
    json_pipe_ids = live_request.get_server_id(projects_urls)
    compared_ids = live_request.compare_ids(json_pipe_ids, existing_id)
    if len(compared_ids) == 0:
        print("No new update")
    elif compared_ids != existing_id and len(compared_ids) != 0:
        ReportUtils.store_id(live_request.LAST_RUN_FILE, existing_id, compared_ids)
        for url in projects_urls:
            pipes = json.load(live_request.get_pipe_ids(url + "pipelines"))
            # Get Pipe ID paths from get_pipe_ids(), pipe_ids is all the pipeline IDs stats per project
            live_request.get_report(compared_ids,pipes,url)
