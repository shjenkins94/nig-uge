# nig-uge
[![Snakemake](https://img.shields.io/badge/snakemake-≥5.17-brightgreen.svg)](https://snakemake.bitbucket.io)

Snakemake profile for running jobs on the NIG Supercomputer.  
Derived from  
[jaicher/snakemake-qsub][qsub]  
 and  
[broadinstitute/snakemake-broad-uger][broad].

Requires [Cookiecutter][cookiecutter-repo] to use.  

## Installation/Setup
To create a new profile, first make sure that the configuration directory that Snakemake searches for profiles exists by running:
```
mkdir -p ~/.config/snakemake
```
then create the profile using Cookiecutter:

```
cookiecutter --output-dir ~/.config/snakemake gh:shjenkins94/nig-uge
```

After giving the profile a name, the following Snakemake parameters can be set:

 - directory
 - conda-prefix
 - restart-times
 - use-conda
 - use-singularity
 - keep-going
 - printshellcmds
 - jobs
 - latency-wait

Along with parameters for cluster execution:

 - default_mem_gb: default amount of memory reserved by each job.
 - default_queue: which queue to use if no resources are specified.
 - cpu_hung_min_time: minimum amount of time before a job can be checked for hanging.
 - cpu_hung_max_ratio: the maximum ratio between cpu time and wallclock time for a job to be considered hanging.
 - missing_job_wait: the amount of time the cluster should wait before checking on a missing job.
 - default_cluster_logdir: directory to store stdout and stderr output from cluster.
 - cluster_dir: directory that stores files tracking job statuses during cluster jobs.

## Usage
After creating a profile, you can run workflows with the parameters you specified using Snakemake's profile flag like so:

```
snakemake --profile PROFILE-NAME {...}
```

## Rule Settings

Individual Snakemake rules can have the following parameters specified in the
Snakemake file:
+ `threads`: the number of threads needed for the job. If not specified,
  assumed to be 1.
+ `resources`
    - `mem_gb`: the memory required for the rule in gigabytes, which will be
      requested if present
    - `use_java`: set to True for rules that use java. Prevents java from using too much memory.
    
[qsub]: https://github.com/jaicher/snakemake-sync-bq-sub
[broad]: https://github.com/broadinstitute/snakemake-broad-uger
[cookiecutter-repo]: https://github.com/audreyr/cookiecutter

