from flask import Flask
from flask import Response
from flask import request
from flask import send_from_directory
import os
import logging
import colorlog
from colorlog import ColoredFormatter
import time
import requests
import re
import json
from datetime import timedelta
import yaml
import urllib
from packaging.version import Version

import sqlite3
# Sqlite reference
# https://github.com/drewmiranda-gl/gl-lookups/blob/2e1f324e72d62a8dd38c336f269ee2bb99a079da/src/dns_ip_search.py

def parse_env_vars(d_env_var_arg):
    
    """
    regex to convert to envvars
        ^[", ]+([^"]+)": (?:")?([^"]+)?(?:")?$
            $1=$2
    """

    final_opts = {}
    d_allowed_env_var = {
        "LOG_FILE": "web.log"
        , "CONSOLE_LEVEL": "INFO"
        , "LOG_LEVEL": "INFO"
        , "BIND_ADDR": ""
        , "BIND_PORT": ""
        , "CONFIG_FILE": "config.yml"
    }

    # build init values
    for item in d_allowed_env_var:
        final_opts[item] = d_allowed_env_var[item]

    # build overrides
    for item in d_env_var_arg:
        # print(str(item) + ": " + str(d_env_var_arg[item]))
        if item in d_allowed_env_var:
            # print(item + " in d_allowed_env_var")
            final_opts[item] = d_env_var_arg[item]

    return final_opts

d_opts = parse_env_vars(os.environ)

def log_level_from_string(log_level: str):
    if log_level.upper() == "DEBUG":
        return logging.DEBUG
    elif log_level.upper() == "INFO":
        return logging.INFO
    elif log_level.upper() == "WARN":
        return logging.WARN
    elif log_level.upper() == "ERROR":
        return logging.ERROR
    elif log_level.upper() == "CRITICAL":
        return logging.CRITICAL

    return logging.INFO

# Read DICT from yaml file
def yaml_to_dict(file: str):
    if os.path.exists(file):
        with open(file) as f:
            doc = yaml.safe_load(f)
            return doc
    return {}

if 1==1:
    logFile = str(d_opts['LOG_FILE'])

    logger = logging.getLogger('PythonGraylogLogReplay')
    logger.setLevel(logging.DEBUG)
    console_log_level = d_opts['CONSOLE_LEVEL']

    d_config = yaml_to_dict(d_opts['CONFIG_FILE'])

    if len(d_opts['LOG_FILE']) > 0:
        logging_file_handler = logging.FileHandler(logFile)
        logging_file_handler.setLevel(log_level_from_string(str(d_opts['LOG_LEVEL'])))
        formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s', '%Y-%m-%d %H:%M:%S')
        logging_file_handler.setFormatter(formatter)
        logger.addHandler(logging_file_handler)
    
    # Console Logging
    try:
        logging_console_handler = colorlog.StreamHandler()
        formatter = ColoredFormatter(
                '%(asctime)s.%(msecs)03d %(log_color)s%(levelname)-8s%(reset)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                reset=True,
                log_colors={
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "red",
                },
            )
    except:
        logging_console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s', '%Y-%m-%d %H:%M:%S')

    logging_console_handler.setLevel(log_level_from_string(str(console_log_level)))
    logging_console_handler.setFormatter(formatter)
    logger.addHandler(logging_console_handler)

    # if "TMP_CUS_LIST" in d_opts and len(d_opts['TMP_CUS_LIST']) > 0:
    #     logger.debug("TEST 123")
    # logger.debug(d_opts)

app = Flask(__name__)
@app.route("/", methods=['GET'])
@app.route("/search", methods=['GET'])
@app.route("/favicon.ico", methods=['GET'])
@app.route("/api", methods=['GET'])
@app.route("/api/find-pr-in-branch", methods=['GET'])
@app.route("/api/get-branches", methods=['GET'])
def main():
    return do_GET()

@app.route('/files/<path:filename>')
def serve_file(filename):
    return send_from_directory('static', filename)



class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def convert_ImmutableMultiDict_to_dict(arg_in):
    # logger.info(arg_in)
    rs = {
        
    }
    for item in arg_in:
        # logger.info("".join([ item, ": ", arg_in[item] ]))
        rs[item] = arg_in[item]
    return rs

def decodeurl(url: str):
    from urllib.parse import unquote
    return unquote(url)

def get_scrape(url: str):
    r = requests.get(url)
    if r.status_code == 200:
        return r.text
    else:
        return str("".join([ "Unexpected return code: ", str(r.status_code) ]))
    return False

def get_end_time_ms(start_time):
    end_time = time.monotonic()
    diff = timedelta(seconds=end_time - start_time)
    diff = diff.total_seconds()*1000
    return diff

def get_customer_list():
    return yaml_to_dict(d_opts['TMP_CUS_LIST'])

def serve_html_for_includes_js_css():
    return "".join([
        "<head>"
        , '<link rel="stylesheet" href="/files/css.css">'
        , '<script type="text/javascript" src="/files/app.js"></script>'
        , '<script type="text/javascript" src="/files/jquery-3.7.1.min.js"></script>'
        "</head>"
    ])

def format_customer_list(input: dict):
    customer_rows = ""
    for customer in input:
        if len(customer) and not str(customer) == " ":
            cluster_ids = ""
            if "cluster-ids" in input[customer]:
                if isinstance(input[customer]["cluster-ids"], list):
                    # logger.debug("input[customer][cluster-ids]")
                    # logger.debug(input[customer]["cluster-ids"])
                    i = 0
                    for s_cluster_id in input[customer]["cluster-ids"]:
                        # logger.debug(s_cluster_id)
                        s_note_html = ""
                        if len(s_cluster_id) and not str(s_cluster_id) == " " and "id" in s_cluster_id:
                            if i > 0:
                                cluster_ids = "".join([
                                    cluster_ids
                                    , "<br>"
                                ])
                            
                            if "note" in s_cluster_id:
                                s_note_html = "".join([
                                    " ("
                                    , s_cluster_id["note"]
                                    , ")"
                                ])

                            cluster_ids = "".join([
                                cluster_ids
                                , '<a href="/cluster/?'
                                    , urllib.parse.urlencode({"cluster_id": str(s_cluster_id["id"])})
                                    , '">'
                                    , str(s_cluster_id["id"])
                                , "</a>"
                                , s_note_html
                            ])
                            i += 1

            customer_rows = "".join([
                customer_rows
                , "<tr>"
                    , "<td>"
                        , str(customer)
                    , "</td>"
                    , "<td>"
                        , str(cluster_ids)
                    , "</td>"
                , "</tr>"
            ])

    final_output = "".join([
        "<style>"
        , "table.customer-table tr td {padding: 4px;}"
        , "</style>"
        ,"<table border=\"1\" class=\"customer-table\">"
            , "<thead>"
            , "<tr>"
                , "<th>"
                    , "customer name"
                ,"</th>"
                , "<th>"
                    , "cluster id(s)"
                ,"</th>"
            , "</tr>"
            , "</thead>"
            , "<tbody>"
                , customer_rows
            , "</tbody>"
        , "</table>"
    ])
    return final_output

def html_search_form():
    s_html = "".join([
        ""
        , "<form action=\"/search\">"
        , "Issue or PR: "
        , "<input type=\"text\" name=\"pr\">"
        , " "
        , "<input type=\"submit\" value=\"search\">"
        , "</form>"
    ])
    return s_html

def get_http_root():
    # customers = get_customer_list()
    # customers_formatted = format_customer_list(customers)
    s_html = html_search_form()

    output_final = ""
    output_final = "".join([
        "<html>"
        , serve_html_for_includes_js_css()
        , "<body>"
        , s_html
        , "</body>"
        , "</html>"
    ])
    return output_final

def get_customer_by_cluster_id(cluster_id: str):
    d_customer = get_customer_list()
    for customer in d_customer:
        if "cluster-ids" in d_customer[customer]:
            if isinstance(d_customer[customer]["cluster-ids"], list):
                for s_cluster_id in d_customer[customer]["cluster-ids"]:
                    if len(s_cluster_id) and not str(s_cluster_id) == " " and "id" in s_cluster_id:
                        if "id" in s_cluster_id:
                            if str(s_cluster_id["id"]) == str(cluster_id):
                                o_dict = {
                                    "name": customer,
                                    "dict": d_customer[customer]
                                }
                                if "note" in s_cluster_id:
                                    o_dict["note"] = s_cluster_id["note"]
                                return o_dict
    return {
        "name": "",
        "note": "",
        "dict": {}
    }

def search_page(search_q: str):
    output_final = ""

    output_final = "".join([
        "<html>"
        , serve_html_for_includes_js_css()
        , "<script>"
            , 'find_pr("',search_q,'");'
        , "</script>"
        , "<body>"
            , html_search_form()
            , "<h1>"
                , "Issue or PR: "
            , "</h1>"
            , "<div>"
                , str(search_q)
            , "</div>"
            , "<div id=\"xhr-pr-rs-open\" class=\"pr-rs\"></div>"
            , "<div id=\"xhr-pr-rs-enterprise\" class=\"pr-rs\"></div>"
        , "</body>"
        , "</html>"
    ])

    return output_final

def get_cluster_info(cluster_id: str):
    output_final = ""

    d_customer = get_customer_by_cluster_id(cluster_id)
    # logger.debug(d_customer)
    s_html_note = ""
    if "note" in d_customer:
        s_html_note = "".join([
            "<br>"
            , "Cluster Note: "
            , str(d_customer["note"])
            , ""
        ])

    output_final = "".join([
        "<html>"
        , serve_html_for_includes_js_css()
        , "<script>"
            , "load_ph_req("
                , "\""
                    , str(cluster_id)
                , "\""
            ,");"
        , "</script>"
        , "<body>"
            , '<a href="/">'
                , "Home"
            , "</a>"
            , "<h1>"
                , "Cluster ID: "
                , str(cluster_id)
            , "</h1>"
            , "Customer: "
            , str(d_customer["name"])
            , s_html_note
        , "</body>"
        , "</html>"
    ])

    return output_final

def query_gh_api(repo_arg: str, query_type: str, query_opt: dict):
    if "github" in d_config:
        if "api-token" in d_config["github"]:
            GITHUB_TOKEN = d_config["github"]["api-token"]
        else:
            raise Exception("Please configure github.api-token in config file.")
        
        if "owner" in d_config["github"]:
            OWNER = d_config["github"]["owner"]
        else:
            raise Exception("Please configure github.owner in config file")

        logger.debug(repo_arg)
        if "repos" in d_config["github"]:
            logger.debug('if "repos" in')
            if str(repo_arg).lower() == "open":
                if "open" in d_config["github"]["repos"]:
                    REPO = d_config["github"]["repos"]["open"]
            elif str(repo_arg).lower() == "enterprise":
                if "enterprise" in d_config["github"]["repos"]:
                    REPO = d_config["github"]["repos"]["enterprise"]

    url = ""
    if str(query_type).lower() == "branches":
        url = f'https://api.github.com/repos/{OWNER}/{REPO}/branches'
    elif str(query_type).lower() == "find-pr-in-branch":
        if "branch" in query_opt:
            BRANCH_SHA = query_opt["branch"]
            url = f'https://api.github.com/repos/Graylog2/{REPO}/git/trees/{BRANCH_SHA}?recursive=1'
    
    logger.debug("".join([
        "len(url): ", str(len(url))
    ]))

    if not len(url):
        logger.error("NO URL built. Invalid query type.")
        return ""
    else:
        logger.debug("".join([
            "GH URL: ", str(url)
        ]))

    # === Headers with Authentication ===
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        final_rs = response.json()
        if str(query_type).lower() == "find-pr-in-branch":
            final_rs["repo"] = REPO
        return final_rs 
        # branches = response.json()
        # branch_names = [branch['name'] for branch in branches]
        # logger.debug("Branches in the repository:")
        # for name in branch_names:
        #     logger.debug("".join([
        #         "- "
        #         , str(name)
        #     ]))

    return ""

def get_gh_branches(repo_arg):

    exp = re.compile(r'^\d+\.\d+$')
    # config_json = json.dumps(d_config, indent=4)
    jsonrs = query_gh_api(repo_arg, "branches", {})

    versions_list = []
    d_tmp = {}

    for item in jsonrs:
        if "name"in item:
            if re.search(exp, str(item["name"])):
                d_tmp[item["name"]] = item
                versions_list.append(item["name"])

    versions_list.sort(key=Version)
    new_versions_list=versions_list[-4:]
    final_list = []
    for version in new_versions_list:
        final_list.append(d_tmp[version])

    return json.dumps(final_list)

def find_pr_in_branch(pr, branch, repo_arg):
    # logger.debug("".join([
    #     "pr: ", str(pr)
    #     , ", "
    #     , "branch: ", str(branch)
    # ]))

    rs = []

    jsonrs = query_gh_api(repo_arg, "find-pr-in-branch", {"branch": branch})
    # logger.debug(jsonrs)
    if "tree" in jsonrs:
        for file in jsonrs["tree"]:
            FILE_PATH = ""
            FILE_PATH = file["path"]
            if str(FILE_PATH).startswith("changelog/"):
                if "," in str(pr):
                    pr_csv = str(pr).split(",")
                else:
                    pr_csv = [pr]
                
                for indv_pr in pr_csv:
                    if str(indv_pr).strip() in str(FILE_PATH):
                        # logger.debug(file)
                        # URL https://github.com/Graylog2/graylog-plugin-enterprise/blob/a007dbdece780b5f1378ce157e32426170d33502/changelog/6.1.0-rc.1/.gitkeep
                        d = {
                            "file": str(FILE_PATH)
                            , "repo": jsonrs["repo"]
                        }
                        rs.append(d)

    return json.dumps(rs)

def do_GET():
    start_time = time.monotonic()

    # logger.debug("".join(["request.path: ", str(request.path)]))

    try:
        d_parsed_args = convert_ImmutableMultiDict_to_dict(request.args)

        # logger.debug(request.query_string.decode())
        logger.info("".join([ 
            "Processing: "
            , str(request.path)
            , " Args: "
            , str(d_parsed_args)
        ]))
        # logger.debug(d_parsed_args)
    except Exception as e:
        return Response(str(e), status=400, mimetype="text/plain")

    if str(request.path) == "/" or str(request.path) == "":
        final_rewritten_page_contents = get_http_root()
        return Response(final_rewritten_page_contents, status=200, mimetype="text/html; version=0.0.4; charset=utf-8")
        
    elif str(request.path) == "/favicon.ico":
        return Response("", status=200, mimetype="text/plain")
    
    elif str(request.path).startswith("/search"):
        final_rewritten_page_contents = ""
        if "pr" in d_parsed_args:
            final_rewritten_page_contents = search_page(d_parsed_args["pr"])
        return Response(final_rewritten_page_contents, status=200, mimetype="text/html")

    elif str(request.path).startswith("/api/get-branches"):
        final_rewritten_page_contents = ""
        if "repo" in d_parsed_args:
            final_rewritten_page_contents = get_gh_branches(d_parsed_args["repo"])
        return Response(final_rewritten_page_contents, status=200, mimetype="application/json")

    elif str(request.path).startswith("/api/find-pr-in-branch"):
        final_rewritten_page_contents = ""
        if "pr" in d_parsed_args and "branch" in d_parsed_args and "repo" in d_parsed_args:
            final_rewritten_page_contents = find_pr_in_branch(d_parsed_args["pr"], d_parsed_args["branch"], d_parsed_args["repo"])
        return Response(final_rewritten_page_contents, status=200, mimetype="application/json")

    return Response("", status=200, mimetype="text/plain")
