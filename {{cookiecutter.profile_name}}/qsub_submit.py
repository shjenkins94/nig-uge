#!/usr/bin/env python
"""
Qsub submission script.

Script to wrap qsub command (no sync) for Snakemake. Uses the following job
parameters:

+ `threads`
+ `resources`
    - `mem_gb`: Expected memory requirements in gigabytes
    - `mpi`: Number of mpi processes to use
    - `use_java`: Sets MALLOC_ARENA_MAX to 2 if true to avoid memory problems.
"""

import sys  # for command-line arguments (get jobscript)
from pathlib import Path  # for path manipulation
from snakemake.utils import read_job_properties  # get info from jobscript
from snakemake.shell import shell  # to run shell command nicely


def get_job_name(job: dict) -> str:
    """Create a job name. Defaults to group name, then rule plus wildcards."""
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


def generate_resources_command(job: dict) -> str:
    """Get the resources part of the command."""
    # Get resource values from rule
    threads = job.get("threads", False)
    resources = job.get("resources", {})
    mem_gb = resources.get("mem_gb", int({{cookiecutter.default_mem_gb}}))
    mpi_np = resources.get("mpi", False)
    use_java = resources.get("use_java", False)

    # Specify number of cpus if threads was specified
    thread_cmd = "-l cpu={}".format(threads) if threads else ""
    # Specify the amount of memory the job requires.
    mem_cmd = "-l s_vmem={0}G -l mem_req={0}G".format(mem_gb)
    # Specify number of mpi processes if mpi was specified
    mpi_cmd = "-pe mpi-fillup {}".format(mpi_np) if mpi_np else ""
    # If use_java is true, set MALLOC_ARENA_MAX to 2
    # (this stops rules that use Java failing silently)
    java_cmd = "-v MALLOC_ARENA_MAX=2" if use_java else ""
    # Set reserve to yes if using mpi or more than the minimum reserve memory
    if mpi_np or mem_gb >= int({{cookiecutter.reserve_min_gb}}):
        reserve_cmd = "-R y"
    else:
        reserve_cmd = ""
    # Make list of resource commands, remove empty string, and join with spaces
    res_cmds = [thread_cmd, java_cmd, mem_cmd, mpi_cmd, reserve_cmd]
    res_cmds = list(filter(None, res_cmds))
    resource_cmd = " ".join(res_cmds)
    return resource_cmd


def get_log_files(job: dict) -> str:
    """Generate the log file part of the command."""
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
    log_file_cmd = "-o {out} -e {err} -N {name}".format(
        out=out_log_path,
        err=err_log_path,
        name=jobname
    )
    return log_file_cmd


# get the jobscript (last argument)
jobscript = sys.argv[-1]

# read the jobscript and get job properties
job_props = read_job_properties(jobscript)

# First part of qsub command
SUBMIT_CMD = "qsub -terse -cwd -V"

# get queue part of command (if empty, don't put in anything)
queue_cmd = "-l {{cookiecutter.default_queue}}" if "{{cookiecutter.default_queue}}" else ""

# get resources
res_cmd = generate_resources_command(job_props)

# get logs
log_cmd = get_log_files(job_props)

# get cluster commands to pass through, if any
cluster_cmd = " ".join(sys.argv[1:-1])

cmds = [SUBMIT_CMD, queue_cmd, res_cmd, log_cmd, cluster_cmd, jobscript]

cmds = list(filter(None, cmds))
# format command
cmd = " ".join(cmds)

# run commands
# get byte string from stdout
shell_stdout = shell(cmd, read=True)

# obtain job id from this, and print
try:
    print(shell_stdout.decode().strip())
except AttributeError:
    print(shell_stdout.strip())
