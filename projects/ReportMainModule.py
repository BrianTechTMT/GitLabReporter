import json
import os
import requests
import re

from ReportUtilityModule import ReportUtils


class GitLabReport:
    # Constants
    STATUS_LIST = ["success", "failed", "manual", "skipped", "cancelled"]
    PROJECT_JSON_PATH = "/../config/projects.json"
    BASE_URL = "http://localhost:8000/PycharmProjects/pythonProject5"
    TOKEN_FILE_PATH = "/../etc/default/telegraf"
    LAST_RUN_FILE = "/var/tmp/tmp_pipeline_ids"
    MATCH_STATUS_TAGS = ["ref", "sha", "id", "web_url", "created_at", "source", "name", "build_ids"]
    REPORT_TAGS = ["name", "total_time", "total_count", "success_count", "failed_count", "skipped_count",
                   "error_count", "build_ids", "suite_error"]

    # Support Functions

    def get_projects(self):
        """
        Read projects json
        """
        project_json = open(os.path.dirname(__file__) + self.PROJECT_JSON_PATH)
        project_identity = json.load(project_json)
        return project_identity

    def get_projects_url_paths(self):
        """
        Get paths to project base on the JSON
        """
        projects_infos = GitLabReport.get_projects(self)
        projects_url_paths = []

        for project in projects_infos:
            projects_url_paths.append(self.BASE_URL + "/projects/{id}/".format(id=project[0]))
        return projects_url_paths

    def get_live_token(self):
        """
        Get Live Test Token
        """
        token_file = open(os.path.dirname(__file__) + self.TOKEN_FILE_PATH, "r")
        keyword = "GITLAB_API_SECRET"
        for tokens in token_file:
            token = tokens.split("\n")
            for token_key in token:
                if keyword in token_key:
                    gitlab_token = token_key.split("\"")[1]
        token_file.close()
        return gitlab_token

    def url_request(self, url):
        """
        Use for each time the script ask for json string from server
        """
        live_token = GitLabReport.get_live_token(self)
        try:
            json_response = requests.get(url, headers={"PRIVATE-TOKEN": live_token})
        except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as error:
            raise SystemExit(error)

        return json_response

    def get_pipe_ids(self, url):
        """
        Get All Pipelines IDs
        """
        encoded_pipelines = GitLabReport.url_request(self, url)
        return encoded_pipelines

    def get_result_report(self, project_id, url):
        """
        Get Report for each pipeline
        """
        url = url + "pipeline_id/" + str(project_id) + "/test_report_summary"
        pipe_list = GitLabReport.url_request(self, url).json()
        return GitLabReport.get_tags(self,pipe_list)

    def get_tags(self, pipe_list):
        for k, v in pipe_list.items():

            if type(v) == list:

                for i in v:
                    report_data = {key: i.get(key) for key in self.REPORT_TAGS}

            else:
                continue

        return report_data

    # Main Functions

    def get_existing_id(self):  # Step 1
        ids_list = []
        if not os.path.exists(os.path.dirname(__file__) + self.LAST_RUN_FILE):  # Check if record file exist
            pipe_id_file = open(os.path.dirname(__file__) + self.LAST_RUN_FILE, "a+")  # if not then create
        else:
            pipe_id_file = open(os.path.dirname(__file__) + self.LAST_RUN_FILE, "r+")  # else, start checking the list
            pipelines = []
            for existing_pipeline in pipe_id_file:
                pipelines = existing_pipeline.split(",")

            ids_list = [int(pipeline) for pipeline in pipelines]

        pipe_id_file.close()
        return ids_list

    def get_server_id(self,urls):  # Step 2
        match_pipe_id_list = []
        for url in urls:
            pipelines = GitLabReport.get_pipe_ids(self, url + "pipelines").json()
            for pipeline in pipelines:
                if pipeline['status'] in GitLabReport.STATUS_LIST:
                    match_pipe_id_list.append(pipeline['id'])
        return match_pipe_id_list

    def compare_ids(self, ids_in_json_list, ids_in_file_list):
        """
        Compare the ID list from API and ID previously found and stored on server
        """
        new_pipeline_id = []
        if ids_in_json_list == ids_in_file_list:
            new_pipeline_id = []

        else:
            new_pipeline_id = [pipe_id for pipe_id in ids_in_json_list if pipe_id not in ids_in_file_list]
        return new_pipeline_id

    def get_report(self, compared_ids, pipes, url):

        # Get existing ID
        for pipe in pipes:  # Use each pipe ID to get the report from JSON file
            if pipe['id'] in compared_ids:  # Trace ID
                report_dict = self.get_result_report(pipe['id'], url)
                # Create path to report json then get a dictionary in return
                pipe_tag_dict = {key: pipe.get(key) for key in self.MATCH_STATUS_TAGS}
                # reformat the dictionary
                print_report_dict = {**pipe_tag_dict, **report_dict}
                proj_id_search = int(re.findall("(?<=projects/).*(?=/)", url)[0])
                proj_names = self.get_projects()
                proj_name_search = ""
                for i in range(len(proj_names)):
                    if proj_names[i][0] == proj_id_search:
                        proj_name_search = proj_names[i][1]
                ReportUtils.print_infulix_protocol(proj_id_search, proj_name_search, print_report_dict)


class GitLabReportMock(GitLabReport):
    def get_projects_url_paths(self): # Child
        """
        Get paths to project base on the JSON
        """
        projects_infos = GitLabReport.get_projects(self)
        projects_url_paths = []

        for project in projects_infos:
            projects_url_paths.append(os.getcwd()+"/{id}/".format(id=project[0]))
        return projects_url_paths

    def url_request(self, url):  # Child
        json_response = open(url)
        return json_response

    def get_result_report(self, project_id,url): # Child
        url = url + "pipeline_id/" + str(project_id) + "/test_report_summary"
        pipe_list = json.load(open(url))
        return GitLabReport.get_tags(self, pipe_list)

    def get_pipe_ids(self, url):
        """
        Get All Pipelines IDs
        """
        encoded_pipelines = GitLabReportMock.url_request(self, url)
        return encoded_pipelines

    def get_server_id(self,urls):  # Step 2
        match_pipe_id_list = []
        for url in urls:
            pipelines = json.load(GitLabReportMock.get_pipe_ids(self, url + "pipelines"))
            for pipeline in pipelines:
                if pipeline['status'] in GitLabReport.STATUS_LIST:
                    match_pipe_id_list.append(pipeline['id'])
        return match_pipe_id_list
