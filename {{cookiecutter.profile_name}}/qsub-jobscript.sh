#!/usr/bin/env bash
# properties = {properties}

# print cluster job id
echo "Running cluster job $JOB_ID"
echo "=============================="

# run the job command
{exec_job}
EXIT_STATUS=$?

# print resource consumption
echo "-----------------------------"
qstat -j $JOB_ID | grep '^usage'

# # print exit status
# echo "-----------------------------"
# echo "EXIT_STATUS: $(cat {{cookiecutter.cluster_dir}}/${JOB_ID}.exit)"
# 
# # exit with captured exit status
# exit $(cat "{{cookiecutter.cluster_dir}}/$JOB_ID.exit")