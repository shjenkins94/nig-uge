#!/usr/bin/env bash
# properties = {properties}

# make file for cluster_dir
mkdir -p "{{cookiecutter.cluster_dir}}"
# print cluster job id
echo "Running cluster job $JOB_ID"
echo "-----------------------------"

# run the job command
{exec_job}
echo $? > "{{cookiecutter.cluster_dir}}/${JOB_ID}.exit"

# print resource consumption
echo "-----------------------------"
qstat -j $JOB_ID | grep '^usage'

# print exit status
echo "-----------------------------"
echo "EXIT_STATUS: $(cat {{cookiecutter.cluster_dir}}/${JOB_ID}.exit)"

# exit with captured exit status
exit $(cat {{cookiecutter.cluster_dir}}/${JOB_ID}.exit)