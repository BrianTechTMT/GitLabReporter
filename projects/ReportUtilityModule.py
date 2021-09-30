import os


class ReportUtils:

    def print_infulix_protocol(proj_id, proj_name, report_dict):
        opening_line = "gitlab_test_report,project_id={projectID}".format(projectID=proj_id)
        tag_line, field_line = "", ""
        tags = ["project_id", "ref", "sha", "id", "proj_name", "build_ids"]

        for k, v in report_dict.items():

            if k in tags:

                if k == "build_ids":
                    tag_line += ",{key}={value}".format(key=k, value=v[0])

                else:
                    tag_line += ",{key}={value}".format(key=k, value=v)

            elif k == "web_url":
                field_line += "{key}=\"{value}\"".format(key=k, value=v)

            else:
                field_line += ",{key}={value}".format(key=k,
                                                      value="\"{string}\"".format(string=v) if type(v) != int else v)

        print(opening_line + tag_line + ",project_name=" + proj_name + " " + field_line)

    def store_id(store_file_location, file_pipe_ids,compared_ids_list):
            id_file = open(os.path.dirname(__file__) + store_file_location, "w")
            list_to_write_to_file = file_pipe_ids + compared_ids_list
            pipe_id_str = ','.join([str(pipe_id) for pipe_id in list_to_write_to_file])
            id_file.write(pipe_id_str)
            id_file.close()