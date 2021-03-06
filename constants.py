from os.path import dirname, expanduser, realpath

HOST = "https://oj.ebg.tw/"
#HOST = "http://localhost/"
CONTEST_NAME = "1092CP2"
#CONTEST_NAME = "1092CP2_Midterm"
#CONTEST_NAME = "1092CPPY"

API_HOST = HOST + "api"
CONTENT_TYPE_OPTION = " -H 'Content-Type: application/json' "
home = expanduser("~")
COOKIES_DIR = home + "/.cookies/"
COOKIES_NAME = "oj_cookies"
COOKIES_PATH = COOKIES_DIR + COOKIES_NAME

ASSIGNMENT_MAPPING_PATH = home + "/oj_statement/assign_mapping.json"
MY_STATUS_PATH = home + "/oj_statement/status_log.json"
PROBLEM_MAPPING_PATH = home + "/oj_statement/problem_mapping.json"
STATEMENT_PATH = home + "/oj_statement/"


TEMPLATE_FILENAME = {
    "C": "main.c",
    "C++": "main.cpp",
    "Java": "main.java",
    "Python2": "mainpy2.py",
    "Python3": "mainpy3.py",
    "Golang": "main.go",
}
