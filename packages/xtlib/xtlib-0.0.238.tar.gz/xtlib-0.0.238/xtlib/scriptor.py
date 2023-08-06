#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# scriptor.py: creates scripts for running XT controller and user Runs
import os
import json

from xtlib import utils
from xtlib import pc_utils
from xtlib import file_utils
from xtlib import run_helper
from xtlib import process_utils
from xtlib import constants
from .console import console
from xtlib import errors

def fixup_script(lines, for_windows, is_local, run_cmd=None, run_info=None, concurrent=None, 
        hold=False):
    #console.print("before FIXUP: lines=", lines)

    newlines = []

    for line in lines:
        if run_cmd and (("%*" in line) or ("$*" in line)):
            # substitute updated run_cmd 
            console.print("fixup_script: substituting new run_cmd=", run_cmd)
            line = run_cmd

        line = fixup_user_cmd(line, for_windows, is_local, run_info, concurrent, hold)
        newlines.append(line)

    #console.print("after FIXUP: newlines=", newlines)
    return newlines

def fixup_user_cmd(flat_cmd, for_windows, is_local, run_info, concurrent, hold):
    '''
    Macros supported:
        $HOME       - same as "~/"
        $IP_ADDR    - ip address of target box
        $REGISTRY   - the name of the user's docker registry (from config file)
        $MR_INDEX   - the child run index modulo the max-runs for the box
        $HOLD       - the True/False value of --hold option
        $CURRENT_CONDA_ENV  - the name of the currenly active conda virtual environment

    Other updates:
        - translate between "$(pwd)" and "%cd", as appropriate for "for_windows"
    '''
    mr_index = None

    if run_info:
        run_name = run_info.run_name
       
        if "." in run_name:
            # compute mr_index (the child run index, modulo the max-runs value)
            # variations: run23, run23.2,  exper.run123, exper.run123.3
            right_part = run_name.split(".")[-1]
            if not run_helper.is_run_name(right_part):
                run_index = int(right_part)
                mr_index = str((run_index-1) % concurrent)
                console.print("run_index=", run_index, ", mr_index=", mr_index)
        
    home_dir = os.path.expanduser("~/")
    ip_addr = pc_utils.get_ip_address() if is_local else ""
    conda = pc_utils.get_conda_env()
    if not conda:
        conda = "py36"      # reasonable default

    # unconditional: we always have this info
    flat_cmd = flat_cmd.replace("$CURRENT_CONDA_ENV", conda)
    flat_cmd = flat_cmd.replace("$HOLD", str(hold))

    if "$MR_INDEX" in flat_cmd:
        flat_cmd = flat_cmd.replace("$MR_INDEX", mr_index)

    if "$HOME" in flat_cmd:
        if not is_local:
            errors.internal_error("cannot expand $HOME for remote box")
        flat_cmd = flat_cmd.replace("$HOME", home_dir)

    if "$IP_ADDR" in flat_cmd:
        # if not is_local:
        #     errors.internal_error("cannot expand $IP_ADDR for remote box")
        ip_addr = "'" + ip_addr + "'"    # surround it with single quotes
        flat_cmd = flat_cmd.replace("$IP_ADDR", ip_addr)

    if for_windows:
        flat_cmd = flat_cmd.replace("$(pwd)", "%cd%")
    else:
        flat_cmd = flat_cmd.replace("%cd%", "$(pwd)")

    # add "-u" unbuffered flag to python, if this marked as the RUN CMD
    if "%*" in flat_cmd or "$*" in flat_cmd:
        if not "-u" in flat_cmd:
            if flat_cmd.startswith("python "):
                flat_cmd = "python -u " + flat_cmd[7:]
            elif flat_cmd.startswith("python3 "):
                flat_cmd = "python3 -u " + flat_cmd[8:]
        
    return flat_cmd

def write_controller_script_file(script_lines, is_windows):
    fn = constants.CONTROLLER_BATCH if is_windows else constants.CONTROLLER_SHELL
    fn = write_script_file(script_lines, fn, is_windows)
    return fn

def write_script_file(script_lines, fn, for_windows):
    '''
    args:
        - script_lines: a list of strings (NOT newline terminated)
        - fn: path of file to create
        - for_windows: if True, lines will be written to end with CR + NEWLINE

    return: 
        - the update filename (with "~" expanded)
    '''
    fn = os.path.expanduser(fn)
    file_utils.ensure_dir_exists(file=fn)

    # set the newline joiner according to the target OS
    newline = "\r\n" if for_windows else "\n"
    text = newline.join(script_lines)

    # specify newline="" here to prevent open() from messing with our newlines
    with open(fn, "wt", newline="") as outfile:
        if not for_windows:
            # remove any rouge CR characters
            text = text.replace("\r", "")
        outfile.write(text)

    if not for_windows:
        # ensure no CR characters are found
        with open(fn, "rb") as infile:
            byte_buff = infile.read()
            if 13 in byte_buff:
                console.print("WARNING: write_script_file failed to remove all CR chars")

    #console.print("for_windows=", for_windows, "newline=", newline, ", script_lines=", script_lines) 
    # test_text = file_utils.read_text_file(fn)
    # console.print("test_text=", test_text)
    
    return fn   

def get_run_cmd_from_script(script):
    run_cmd = None

    for line in script:
        if ("%*" in line) or ("$*" in line):
            run_cmd = line
            break

    return run_cmd

def send_script_to_remote_box(caller, box_addr, fn_source, fn_dest, linux_box=True):
    # copy script to box
    console.diag("  copying file to box: " + fn_dest)
    process_utils.scp_copy_file_to_box(caller, box_addr, fn_source, fn_dest, report_error=True)
    console.diag("  <copy completed OK>")

    if linux_box:
        # mark it as executable
        box_cmd = "chmod +x {}".format(fn_dest)
        process_utils.sync_run_ssh(caller, box_addr, box_cmd)
        
def add_controller_env_vars(env_vars, config, box_secret, node_id):
    '''
    adds the following env var's needed by the XT controller:
        - XT_SERVER_CERT            (controller only, for rpyc socket)
        - XT_USER_PRINCIPLE_NAME    (controller only, for request validation)
        - XT_STORE_CREDS            (controller (store access for remote xt) + ML app)
        - XT_DB_CREDS               (controller (store access for remote xt) + ML app)
        - XT_STORE_CODE_PATH        (controller (store access for remote xt) + ML app)
        - XT_NODE_ID                (controller (index into multirun file) + ML app)
    '''
    # convert keys to base64 to workaround issues with AML and env var values with spaces
    # as a minor positive side effect, we don't directly show key values as clear text

    env_vars["XT_BOX_SECRET"] = box_secret

    # BASE64 strings
    cert_text = config.get_vault_key("xt_server_cert")
    env_vars["XT_SERVER_CERT"] = utils.text_to_base64(cert_text)

    storage_creds = config.get_storage_creds()
    sc = json.dumps(storage_creds)
    env_vars["XT_STORE_CREDS"] = utils.text_to_base64(sc)

    mongo_creds = config.get_database_creds()

    ss_info = config.get_store_info()
    storage_tracking = utils.safe_value(ss_info, "track-storage")

    if storage_tracking:
        # no mongo is available for run to use (everything is logged to storage)
        env_vars["XT_DB_CREDS"] = ""
    else:
        db_creds = config.get_database_creds()
        db_creds_json = json.dumps(db_creds)
        env_vars["XT_DB_CREDS"] = utils.text_to_base64(db_creds_json)

    # NORMAL strings
    #env_vars["XT_USER_PRINCIPLE_NAME"] = config.get_vault_key("user_principle_name")
    env_vars["XT_STORE_CODE_PATH"] =  config.get_storage_provider_code_path(storage_creds)

    # gets updated later by backend impl
    if node_id is not None:
        env_vars["XT_NODE_ID"] = node_id