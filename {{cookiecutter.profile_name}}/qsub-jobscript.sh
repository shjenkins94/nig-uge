#!/usr/bin/env bash
# properties = {properties}

# Create directory to hold exit status files
mkdir -p "{{cookiecutter.cluster_dir}}"

# print cluster job id
echo "Running cluster job $JOB_ID"
echo "=============================="

# run the job command
( {exec_job} )
echo $? > {{cookiecutter.cluster_dir}}/$JOB_ID.exit #Store exit status in a file

echo "-----------------------------"
# print resource consumption
qstat -j $JOB_ID | grep '^usage'
# print exit status
echo "-----------------------------"
printf "Exit Status: " | cat - .cluster_status/$JOB_ID.exit
echo "-----------------------------"

# exit with captured exit status
cat .cluster_status/$JOB_ID.exit | exit -
