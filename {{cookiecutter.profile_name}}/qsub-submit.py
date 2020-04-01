#!/usr/bin/env python
"""
qsub-submit.py

Script to wrap qsub command (no sync) for Snakemake. Uses the following job or
cluster parameters:

+ `threads`
+ `resources`
    - `mem_mb`: Expected memory requirements in megabytes. Overrides
      cluster.mem_mb
"""

import os
import re
import sys  # for command-line arguments (get jobscript)
import subprocess
from pathlib import Path  # for path manipulation
from snakemake.utils import read_job_properties  # get info from jobscript


# Create a job name. Defaults to group name, then rule plus wildcards
def get_job_name(job: dict) -> str:
    if job.get("type", "") == "group":
        groupid = job.get("groupid", "group")
        jobid = job.get("jobid", "").split("-")[0]
        jobname = "{groupid}_{jobid}".format(groupid=groupid, jobid=jobid)
    else:
        wildcards = job.get("wildcards", {})
        wildcards_str = ("_".join(wildcards.values()) or "unique")
        name = job.get("rule", "") or "rule"
        jobname = "smk.{0}.{1}".format(name, wildcards_str)
    return jobname


# get the resources part of the command
def generate_resources_command(job: dict) -> str:
    # get values
    threads = job.get("threads", 1)
    resources = job.get("resources", {})
    # start by requesting threads in smp if threads > 1
    if threads > 1:
        thread_cmd = "-pe smp {threads}"
    else:
        thread_cmd = ""
    mem_mb = resources.get("mem_mb", int({{cookiecutter.default_mem_mb}}))
    mem_cmd = "-l s_vmem={mem_mb}M -l mem_req={mem_mb}M".format(mem_mb=mem_mb)
    if (threads >= int({{cookiecutter.reserve_min_threads}}) or
            mem_mb >= int({{cookiecutter.reserve_min_mem_mb}})):
        reserve_cmd = "-R yes"
    else:
        reserve_cmd = ""
    res_cmd = "{thread_cmd} {mem_cmd} {reserve_cmd}".format(
        thread_cmd=thread_cmd,
        mem_cmd=mem_cmd,
        reserve_cmd=reserve_cmd)
    return (res_cmd)


def get_log_files(jobname: str) -> str:
    # get the name of the job
    jobname = get_job_name(job)
    # determine names to pass through for job name, logfiles
    log_dir = "{{cookiecutter.default_cluster_logdir}}"
    # get the output file name
    out_log = "{}.out".format(jobname)
    err_log = "{}.err".format(jobname)
    # get logfile paths
    out_log_path = str(Path(log_dir).joinpath(out_log))
    err_log_path = str(Path(log_dir).joinpath(err_log))
    log_cmd = "-o {out} -e {err} -N {name}".format(
        out=out_log_path,
        err=err_log_path,
        name=jobname
    )
    return(log_cmd)


# get the jobscript (last argument)
jobscript = sys.argv[-1]

# read the jobscript and get job properties
job = read_job_properties(jobscript)

# get command to do cluster command (no sync)
submit_cmd = "qsub -terse -cwd"

# get queue part of command (if empty, don't put in anything)
queue_cmd = "-q {queue}" if "{{cookiecutter.default_queue}}" else ""

# get resources
res_cmd = generate_resources_command(job)

# get logs
log_cmd = get_log_files(job)

# get cluster commands to pass through, if any
cluster_cmd = " ".join(sys.argv[1:-1])

# format command
cmd = "{submit} {queue} {res} {log} {cluster} {jobscript}".format(
    submit=submit_cmd,
    queue=queue_cmd,
    res=res_cmd,
    log=log_cmd,
    cluster=cluster_cmd,
    jobscript=jobscript
)

try:
    res = subprocess.run(cmd, check=True, shell=True, stdout=subprocess.PIPE)
except subprocess.CalledProcessError as e:
    raise e

res = res.stdout.decode()
print(res.strip())
