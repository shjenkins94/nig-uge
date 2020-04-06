#!/usr/bin/env bash
# properties = {properties}

# print cluster job id
echo "Running cluster job $JOB_ID"
echo "=============================="

# run the job command
{exec_job}

# print resource consumption
qstat -j $JOB_ID | grep '^usage'
echo "-----------------------------"
