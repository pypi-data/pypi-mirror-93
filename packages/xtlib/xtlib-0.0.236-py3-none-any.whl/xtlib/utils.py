#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
 # py: common functions shared among XT modules

from logging import error
import os
import re
import sys
import json
import math
import time
from xtlib import pc_utils
import arrow
import pickle
import logging
import shutil
import datetime
import traceback
import importlib
from threading import Thread, Lock
from multiprocessing import Pool

from xtlib import errors
from xtlib import constants
from xtlib import file_utils
from xtlib import job_helper
from xtlib import run_errors

from xtlib.console import console
from xtlib.helpers.feedbackParts import feedback as fb

class PropertyBag: pass

# utils internal variables
show_stack_trace = True     # until config/flag overrides

def dict_default(dd, key, default_value=None):
    return dd[key] if key in dd else default_value

def dict_to_object(prop_dict):
    class BagObject:
        def __init__(self, **prop_dict):
            self.__dict__.update(prop_dict)

    return BagObject(**prop_dict)

def has_azure_wildcards(name):
    has_wild = "*" in name
    return has_wild

def parse_list_option_value(value):
    if isinstance(value, str):
        if value.startswith("[") and value.endswith("]"):
            # remove optional brackets
            value = value[1:-1].strip()
            
        # convert comma separated values into a list of values
        value = value.split(",")

    return value
    
def is_azure_batch_box(box_name):
    return (box_name and "-batch-" in box_name)

def is_azure_ml_box(box_name):
    return (box_name and "-aml-" in box_name)

def is_philly_box(box_name):
    return (box_name and "-philly-" in box_name)

def is_itp_box(box_name):
    return (box_name and "-itp-" in box_name)

def is_service_box(box_name):
    return box_name and job_helper.is_job_id(box_name) and "-" in box_name

def load_json_records(text):
    # each line is a JSON text record, with a newline at the end
    json_text = "[" + text.replace("\n", ",")[0:-1] + "]"
    records = json.loads(json_text)
    return records

def load_json_file(fn):
    with open(fn, "rt") as infile:
        text = infile.read()
    data = json.loads(text)
    return data

def format_store(store):
    return "{}://".format(store)  

def format_workspace(store, ws_name):
    return "store={}, workspace={}".format(store.upper(), ws_name.upper())

def format_workspace_exper_run(store_type, ws_name, exper_name, run_name):
    return "{}/{}.format(ws_name, run_name)"

def time_diff(time1, time2):
    '''
    Args:
        time1, time2: datetime or arrow objects 
    '''
    atype = arrow.arrow.Arrow
    dttype = datetime.datetime

    # support mixed types
    if type(time1) != type(time2):

        # convert both to datetime without timezone
        if isinstance(time1, atype):
            time1 = time1.datetime.replace(tzinfo=None)

        if isinstance(time2, atype):
            time2 = time2.datetime.replace(tzinfo=None)

    return (time1 - time2).total_seconds()

def elapsed_time(start):
    diff = datetime.datetime.now() - start

    elapsed = str(diff)
    index = elapsed.find(".")
    if index > -1:
        elapsed = elapsed[0:index]

    return elapsed

def str_is_float(value):
    is_float = False
    try:
        fvalue = float(value)
        is_float = True
    except:
        pass
    return is_float

def is_number(text):
    return str_is_float(text)
    
def make_numeric_if_possible(value):
    try:
        value = int(value)
    except:
        try:
            value = float(value)
        except:
            pass

    # also convert boolean values
    if isinstance(value, str):
        lower = value.lower()
        if lower == "true":
            value = True
        elif lower == "false":
            value = False

    return value

def format_elapsed_hms(elapsed, include_fraction=False):
    value = str(datetime.timedelta(seconds=float(elapsed)))
    if not include_fraction:
        index = value.find(".")
        if index > -1:
            value = value[0:index]

    return value

def make_retry_func(max_retries=8, reset_func=None):
    #max_retries = 8     # 95 secs total retry time
    #console.print("received max_retries=", max_retries)

    def expo_retry(context):

        if not hasattr(context, "count"):
            context.count = 1
        else:
            context.count += 1
            pass

        status = None
        if context.response and context.response.status:
            status = context.response.status

        ex_type, exception_msg, ex_traceback = sys.exc_info()
        str_exception = str(context.exception).replace('\n', '')

        '''
        do not retry this error; it must be retried at the API level:
            azure error being RETRIED (non-fatal): status=412, retry count=21, backoff=16, max_retries=25, exception=The condition 
            specified using HTTP conditional header(s) is not met. ErrorCode: ConditionNotMet<?xml version="1.0" encoding="utf-8"?>
        '''

        if status == 412 or "specified using HTTP conditional header(s) is not met" in str_exception:
            # do not retry - fail now
            return None

        tb_lines = get_stack_lines()
        run_errors.record_run_error("storage", str_exception, None, tb_lines)

        with open(constants.AZURE_ERRORS_FN, "a") as errfile:
            error_time = time.time()

            console.print("Azure Exception in XTLIB (see {} at time={} for more details): {}".\
                format(constants.AZURE_ERRORS_FN, error_time, exception_msg))

            # console.print exception and stack trace in errfile
            errfile.write("Azure Exception in XTLIB at time={}: {}\n".format(error_time, exception_msg))
            errfile.write('-'*60 + "\n")
            traceback.print_exc(file=errfile)
            errfile.write('-'*60 + "\n")

        if context.count > max_retries:
            backoff_time = None
            if max_retries:
                console.print("*** auzre error retry FAILED (FATAL): max_retries={} exceeded ***".format(max_retries))
        else:
            backoff_time = min(16, 2**context.count)

            if max_retries:
                console.print("\nazure error being RETRIED (non-fatal): status={}, retry count={}, backoff={}, max_retries={}, exception={}" \
                    .format(status, context.count, backoff_time, max_retries, str_exception))

        return backoff_time
    
    return expo_retry

def print_elapsed(start, operation):
    elapsed = time.time() - start
    console.print("{} took: {:.2f} secs".format(operation, elapsed))

def records_in_sync(records, records2, TIME_COL):
    in_sync = True

    for r1, r2 in zip(records, records2):
        t1 = arrow.get(r1[TIME_COL])
        t2 = arrow.get(r2[TIME_COL])
        delta = min((t1-t2).seconds, (t2-t1).seconds)
        #console.print("delta=", delta)

        if delta > .5:
            in_sync = False
            break

    #console.print("returning in_sync: ", in_sync)
    return in_sync

def merge_records(records, records2, TIME_COL):   
    for r, r2 in zip(records, records2):
        #console.print("r2=", r2)    
        for key,value in r2.items():    
            if key != TIME_COL:
                r[key] = value

def strip_leading_dashes(value):
    while value.startswith("-"):
        value = value[1:]
    return value

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)

    HOW IT WORKS: the re.split code below elegantly splits "text" into a list
    of text and int values.  these are returned to sort, which uses them to 
    sort the list.
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def get_number_or_string_list_from_text(text):
    parts = text.split(",")
    
    count = len(parts)
    float_count = sum(str_is_float(part) for part in parts)
    int_count = sum(part.isdigit() for part in parts)

    if float_count == count:
        # all numbers
        if int_count == float_count:
            # all int
            parts = [int(part) for part in parts]
        else:
            # mixture of ints/floats
            parts = [float(part) for part in parts]

    return parts

def get_python_value_from_text(part):
    '''
    args: 
        part - string containing a python simple value (int, float, string, bool)

    processing:
        convert text to its native python type value

    return:
        native python value
    '''
    part = part.strip()
    if part.isdigit():
        value = int(part)
    elif str_is_float(part):
        value = float(part)
    elif str in ["false", "False"]:
        value = False
    elif str in ["true", "True"]:
        value = True
    else:
        # value must be a string
        value = part

    return value        

def get_arrow_time_str():
    ''' 
    returns NOW as an arrow time string
    '''
    #return time.time()
    return str(arrow.now()) 

def get_time_from_arrow_str(arrow_str):
    '''
    converts an arrow time string to seconds (float)
    '''
    arrow_time = arrow.get(arrow_str)
    return arrow_time.datetime.timestamp()

def parse_time(arrow_time_str):
    '''
    parse an datetime string produced by arrow module
    and return value in form of datetime object. 
    '''
    atime = arrow.get(arrow_time_str)
    dt = atime.datetime
    return dt

def is_philly_job(job_info):
    is_philly = False
    
    if "pool_info" in job_info:
        pool_info = job_info["pool_info"]
        if "service" in pool_info:
            service = pool_info["service"]
            is_philly = (service == "philly")  

    return is_philly

def safe_value(dd, key, default=None):
    return dd[key] if dd and key in dd else default

def safe_delete(dd, key, default=None):
    value = default
    if dd and key in dd:
        value = dd.pop(key)

    return value

def safe_move(newdd, dd, key, default=None, flatten=False):
    value = default
    if key in dd:
        value = dd[key]
        del dd[key]

        if flatten:
            if value:
                newdd.update(value)
        else:
            newdd[key] = value

    return value

def safe_nested_value(dd, key, default=None):
    parts = key.split(".")
    value = dd

    for part in parts:
        value = safe_value(value, part)

    return value    

def print_dict_lines(dd, indent="", max_len=150):
    fmt = "{}{}: {:." + str(max_len) + "s}"
    for key, value in dd.items():
        console.print(fmt.format(indent, key, str(value)))


def make_box_name(job_id, service_name, node_index):
    box_name = "{}-{}-{}".format(job_id, service_name, node_index)
    return box_name

def get_provider_code_path_from_context(context, provider_type, name):
    '''
    return the class constructor method for the specified provider.
    '''
    providers = context.providers[provider_type]

    if not name in providers:
        errors.config_error("{} provider='{}' not registered in XT config file".format(provider_type, name))

    code_path = providers[name]
    return code_path
    
def get_provider_class_ctr_from_context(context, provider_type, name):
    '''
    return the class constructor method for the specified provider.
    '''
    code_path = get_provider_code_path_from_context(context, provider_type, name)
    return get_class_ctr(code_path)

def get_class_ctr(code_path):
    package, class_name = code_path.rsplit(".", 1)
    module = importlib.import_module(package)
    class_ctr = getattr(module, class_name)
    return class_ctr

import inspect

def obj_to_dict(obj):
    obj_dict = {}
    
    for name in dir(obj):
        value = getattr(obj, name)
        if not callable(value) and not name.startswith('__'):
            obj_dict[name] = value

    return obj_dict

def text_to_base64(text):
    value = ""
    if text:
        import base64
        #print("text=", text)
        bytes_value = base64.b64encode(bytes(text, 'utf-8'))
        value = bytes_value.decode()
    return value

def base64_to_text(b64_text):
    value = ""
    if b64_text:
        import base64
        bytes_value = base64.b64decode(b64_text)
        value = bytes_value.decode()
    return value

def debug_break():
    import ptvsd

    # 5678 is the default attach port in the VS Code debug configurations
    console.print("Waiting for debugger attach")
    ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
    ptvsd.wait_for_attach()
    breakpoint()

def copy_data_to_submit_logs(args, data, fn):
    submit_logs = args["submit_logs"]
    if submit_logs:
        text = json.dumps(data)
        # copy text to submit logs
        fn_dest = os.path.join(submit_logs, os.path.basename(fn))
        with open(fn_dest, "w") as outfile:
            outfile.write(text)
        console.diag("copied {} to: {}".format(fn, fn_dest))

def copy_to_submit_logs(args, fn, fnx=None):
    submit_logs = args["submit_logs"]
    if submit_logs:
        # copy file to submit logs
        if not fnx:
            fnx = fn
        fn_dest = os.path.join(submit_logs, os.path.basename(fn))
        shutil.copyfile(fn, fn_dest)
        console.diag("copied {} to: {}".format(fn, fn_dest))

def get_controller_cwd(is_windows, is_local=False):
    if is_windows:
        # we only support windows as a local machine
        #cwd = os.path.expanduser("~/.xt/cwd")

        # docker has problems mapping paths to user home directories (~/)
        # controller app has problems copying/deleting files in 'programdata' folder
        # so, for windows, we use this:
        home_drive = os.getenv("HOMEDRIVE")
        cwd = home_drive + "\\.xt\\cwd"
    else:   
        cwd = "~/.xt/cwd"

        # only safe to expand if local
        if is_local:
            cwd = os.path.expanduser(cwd)

    return cwd

def init_logging(fn, logger, title):
    fn_xt_info = os.path.expanduser(fn)
    file_utils.ensure_dir_exists(file=fn_xt_info)

    logging.basicConfig(format='%(asctime)s.%(msecs)03d, %(levelname)s, %(name)s: %(message)s', 
        datefmt='%Y-%m-%d, %H:%M:%S', level=logging.INFO, filename=fn_xt_info)
  
    logger.info("---------------------------")
    logger.info("new {} started".format(title))

def cmd_split(cmd):
    # split on spaces, unless protected by quotes or []
    parts = []

    part = ""
    protector = None

    for ch in cmd:
        if protector:
            # spaces are protected
            part += ch
            if ch == protector:
                protector = None
        else:
            # spaces are separators
            if ch == " ":
                parts.append(part)
                part = ""
            else:
                part += ch
                if ch in ["'", '"']:
                    protector = ch
                elif ch == "[":
                    protector = "]"

    # add last part, if any
    if part:
        parts.append(part)

    # cleanup parts
    cmd_parts = []

    for i, part in enumerate(parts):
        part = part.strip()
        if part:
            if part.startswith("'") and part.endswith("'"):
                part = part[1:-1]
            elif part.startswith('"') and part.endswith('"'):
                part = part[1:-1]

            cmd_parts.append(part)

    return cmd_parts

def wildcard_to_regex(text):
    text2 = text.replace(".", "\\.")
    text3 = text2.replace("*", ".*")
    text4 = text3.replace("?", ".")

    return text4
    
def node_id(node_index):
    return "node" + str(node_index)

def node_index(node_id):
    return int(node_id[4:])

def remove_surrounding_quotes(text):
    text = text.strip()
    if text.startswith("'") and text.endswith("'"):
        text = text[1:-1].strip()
    elif text.startswith('"') and text.endswith('"'):
        text = text[1:-1].strip()

    return text

def zap_none(text):
    if text == "none":
        text = None
    return text

def safe_cursor_value(cursor, name):
    value = None
    if cursor:
        records = list(cursor)
        value = safe_value(records[0], name) if records else None
    return value

def find_by_property(elements, prop, target):
    result = next((elem for elem in elements if prop in elem and elem[prop] == target), None) 
    return result

def report_elapsed(start, name):
    elapsed = time.time() - start
    print("{} took: {:.2f} secs".format(name, elapsed))

def run_on_threads(worker_func, workitems, max_workers, args_for_worker):
    # wrapup a subset of run_list on each worker thread
    if not workitems:
        # no work to do
        return

    threads = []
    item_count = len(workitems)

    #for runs in runs_by_box.values():
    num_workers = min(item_count, max_workers)

    # split id_list into num_workers sub-lists
    per_list = math.ceil(item_count/num_workers)
    next_index = 0

    while next_index < item_count:
        # build next sub-list
        items = workitems[next_index:next_index+per_list]
        full_args = [items] + args_for_worker
        next_index += per_list

        thread = Thread(target=worker_func, args=full_args)
        thread.start()
        threads.append(thread)

    # wait for all threads to complete their work
    for thread in threads:
        thread.join()

def run_on_processes(worker_func, workitems, max_workers, args_for_worker):
    # wrapup a subset of run_list on each worker process
    item_count = len(workitems)

    #for runs in runs_by_box.values():
    num_workers = min(item_count, max_workers)

    # split id_list into num_workers sub-lists
    per_list = math.ceil(item_count/num_workers)
    next_index = 0

    pool = Pool(processes=num_workers) 

    res = [pool.apply_async(worker_func, args=(item,)) for item in workitems]

    # wait for all processes to complete
    results = [p.get() for p in res]

def log_title(title, double=False):
    if pc_utils.is_compute_node():
        if double:
            line = "=========================================="
        else:
            line = "------------------------------------------"

        console.print(line)
        console.print(title)
        console.print(line)

add_time_to_log_info = False

def log_info(title, value):
    if pc_utils.is_compute_node():
        title = (title + ":").ljust(25)

        # add time for platforms that don't log time for console output
        if add_time_to_log_info:
            now = datetime.datetime.now()
            now_str = now.strftime("%Y-%m-%d %H:%M:%S")
            title = "@{}: {}".format(now_str, title)

        console.print("{} \t{}".format(title, value))

def log_info_to_text(title, value):
    title = (title + ":").ljust(25)
    text = "{} \t{}".format(title, value)
    return text

def load_context_from_mrc():
    context = None

    fn_context = os.path.abspath(constants.FN_RUN_CONTEXT)
    if os.path.exists(fn_context):
        json_context = file_utils.read_text_file(fn_context)

        context_dict = json.loads(json_context)
        context = dict_to_object(context_dict)

    return context
    
def get_stack_lines():
    ''' 
    Processing:
        - this returns the formatted lines of the CALL STACK, from current frame to beginning of program.
    
    NOTE: this does NOT return TRACEBACK frames, which are the frames between the current stack frame and 
    the frame that threw an exception.
    '''

    RUNPY = "lib\\runpy.py" if os.name == "nt" else "lib/runpy.py"
    frames = traceback.extract_stack()

    index = len(frames)-1
    while index > 0:
        if frames[index].filename.endswith(RUNPY):
            # remove earlier frames
            frames = frames[index:]
            break
        index -= 1

    # remove 2 most recent frames (part of our tooling)
    frames.pop()
    frames.pop()

    lines = []
    for frame in frames:
        line = 'File "{}", line {}, in {}'.format(frame[0], frame[1], frame[2])
        lines.append(line)
        line = '{}'.format(frame[3])
        lines.append(line)
    
    ex_type, ex_value, ex_traceback = sys.exc_info()
    last_line = "{}: {}".format(ex_type, ex_value)
    lines.append(last_line)

    return lines

def rename_dict_key(dd, from_name, to_name):
    if from_name in dd and from_name != to_name:
        dd[to_name] = dd.pop(from_name)

def is_col_name(text):
    # must start with letter, followed by letter/digit/_/-/.
    is_name = False
    if text:
        is_name = re.search("[a-z, A-Z][\\w\\-\\.]*", text)

    return is_name

def print_env_vars():
    keys = list(os.environ.keys())
    keys.sort()
    for key in keys:
        value = os.getenv(key)
        log_info(key, value)
    
def tag_dict_from_list(tag_list):
    td = {}

    if tag_list:
        # convert to dict
        for tag in tag_list:
            if "=" in tag:
                key, value = tag.split("=", 1)
                td[key] = value
            else:
                td[tag] = ""
    return td

