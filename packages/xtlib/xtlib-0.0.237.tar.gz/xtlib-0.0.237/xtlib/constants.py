#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# constants.py: constant strings and values share among multiple modules
'''
NOTE: some of these constant strings are by necessity hard-coded into 
the standalone file psm/psm.py.  If you change the value of a string
here, check to see if you need to also change it in psm.py.
'''

#Sync the BUILD string changes with: setup.py, CHANGELOG.md
BUILD = "version: 0.0.237, build: Jan-29-2021"
    
INFO_CONTAINER_V1 = "xt-store-info"
INFO_CONTAINER_V2 = "00-store-info"
STORAGE_FORMAT_V2 = "2"
STORAGE_FORMAT_V1 = "1"

INFO_DIR = "__info__"
STORAGE_INFO_FILE = INFO_DIR + "/storage_info.json"
NODE_PREFIX = "_"

TRACEBACK = "Traceback (most recent call last)"

# XT inserted metrics
INDEX = "__index__"
STEP_NAME = "__step_name__"
TIME = "__time__"

CONFIG_FN = "xt_config.yaml"
AZURE_ERRORS_FN = "azure_errors.txt"

AFTER = "__after__"
WINDOWS_SERVICE_LOGS = "__after__\\service_logs"
WINDOWS_XT_LOGS = "__after__\\xt_logs"
LINUX_XT_LOGS = "__after__/xt_logs"

# workspace directory and files
WORKSPACE_DIR = "__ws__"
RUNS_DIR = "runs"
EXPERIMENTS_DIR = "experiments"
HOLDER_FILE = "__make_dir__"
WORKSPACE_LOG = "workspace.log"
WORKSPACE_LAST_JOB = "last_job_created.txt"
SHARED_FILES = "shared_files"
EMPTY_TAG_CHAR = "+"

# FN_RUNNER_SH = "_xt_runner_{}.sh"
# FN_RUNNER_BAT = "_xt_runner_{}.bat"

# mongo_run_index STATUS values
UNSTARTED = "unstarted"
WAITING = "waiting_for_restart"
STARTED = "started"
COMPLETED = "completed"

# run LOG files
ALL_RUNS_CACHE_FN = "allruns/$aggregator/all_runs.json"   
RUN_LOG = "run.log"                 # single run (stored in run dir)
ALL_RUNS_FN = "all_runs.jsonl"      # job/experiment set of runs

# event logs
XT_HOME = "~/.xt"
FN_XT_EVENTS = "~/.xt/xt_events.log"     # normal and error events for XT client
FN_CONTROLLER_EVENTS = "~/.xt/controller_events.log"     # normal and error events for XT controller
FN_QUICK_TEST_EVENTS = "~/.xt/quick_test_events.log"

# run SUMMARY files
RUN_SUMMARY_CACHE_FN = "summaries/$ws/summary.json"
RUN_SUMMARY_LOG = "run_summary.log"      # single run (stored in run dir)
WORKSPACE_SUMMARY = "run_summary.log"    # all runs (stored in workspace)

# run names by JOB/EXPERIMENT
AGGREGATED_RUN_NAMES_FN = "aggregated_run_names.txt"     # runs that have ENDED

JOBS_NEXT = "next_job_number.control"
JOBS_DIR = "jobs"
JOB_INFO_FN = "job_info.json"
JOB_LOG = "job.log"               # info about a job

# run names
RUN_STDOUT = "console.txt"
RUN_STDERR = "console.txt"

# context file (in run dir of each run)
FN_RUN_CONTEXT = "__xt_run_context__.json"

# hyperparameter config file
OLD_HP_CONFIG_DIR = "hp-confg-dir"
HP_CONFIG_DIR = "hp-config-dir"
HP_CONFIG_FN = "hp_config.txt" 
HP_SWEEP_LIST_FN = "sweeps-list.json"

BOX_WD = "~/xt_run"
CONTROLLER_PORT = 18861
TENSORBOARD_PORT = 6006
AZURE_BATCH_BASE_CONTROLLER_PORT = 7500  

CONTROLLER_SCRIPTS_DIR = "~/.xt/controller"
CWD_DIR = "~/.xt/cwd"
CODE_ZIP_FN = "xt_code.zip"
BOOTSTRAP_ZIP_FN = "xt_bootstrap.zip"

# files that capture controller output
CONTROLLER_SCRIPT_LOG = "./__after__/controller_script.log"           # output of batch/script file that launches controller
CONTROLLER_RUN_LOG = "./__after__/controller_run.log"                 # output of cmd that runs controller
CONTROLLER_INNER_LOG = "./__after__/controller_inner.log"   # stdout capture from within controller code

# script/batch files used to launch the controller
CONTROLLER_SHELL = "~/.xt/cwd/run_controller.sh"
CONTROLLER_BATCH = "~/.xt/cwd/run_controller.bat"
        
APP_EXIT_MSG = "@__app_exit__"
TEMP_SCRIPT = "$TEMP/xt_script"

LOCAL_KEYPAIR_PRIVATE = "~/.ssh/xt_id_rsa"
LOCAL_KEYPAIR_PUBLIC = "~/.ssh/xt_id_rsa.pub"

# files needed to run controller on Azure Batch/Azure ML
SH_NAME ="__run_controller__.sh"
PY_RUN_CONTROLLER ="__run_controller__.py"
FN_MULTI_RUN_CONTEXT = "__multi_run_context__.json"

# the full cert (including private key)
FN_SERVER_CERT = "~/.xt/cwd/__xt_server_cert__.pem"

# the public half of the full cert
FN_SERVER_CERT_PUBLIC = "~/.xt/cwd/__xt_server_cert_public__.pem"

# primary setup cmd file
FN_WRAPPED_SH = "__wrapped__.sh"
FN_WRAPPED_BAT = "__wrapped__.bat"
FN_EV = "__dockev__.txt"
FN_AML_SHIM = "__aml_shim__.py"
FN_BATCH_HELPER = "__batch_helper__.sh"

# if using docker, most cmds are stored in the secondary inner file
FN_INNER_SH = "__inner__.sh"
FN_INNER_BAT = "__inner__.bat"

LOGS_DIR = "__logs__"
FN_IMAGE_NAME =  "__docker_image_name.txt"

distribution_types = [
    "choice", "randint", 
    "uniform", "normal", "loguniform", "lognormal", 
    "quniform", "qnormal", "qloguniform", "qlognormal", 
    ]

ESCAPE = '\x1b'
CONTROL_C = '\x03'

# psm modules (keep manually in-sync with standalone psm.py)
PSM_QUEUE = "~/.xt/psm_queue"
CWD = "~/.xt/cwd"
PSM = "psm.py"
PSMLOG = "psm.log"
PSM_LOGDIR = "~/.xt/psm_logs"
CURRENT_RUNNING_ENTRY = "__current_running_entry__.txt"

# hyperparameter YAML property names
HPARAM_DIST = "hyperparameter-distributions"
HPARAM_RUNSET = "hyperparameter-runset"
HPARAM_RUNSETS = "hyperparameter-runsets"
HPARAM_COMMAND = "command"

# used to communicate user requests from XT controller to running scripts
FN_USER_REQUEST = "~/.xt/cwd/__user_request__.txt"