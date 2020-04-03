# nig-uge

Snakemake cookiecutter profile for running jobs on the NIG Supercomputer
Derived from  
[jaicher/snakemake-qsub][qsub]  
 and  
[broadinstitute/snakemake-broad-uger][broad].

Deploy using [cookiecutter][cookiecutter-repo] (easily installed using conda or
pip) by running:

   [qsub]: https://github.com/jaicher/snakemake-sync-bq-sub
   [broad]: https://github.com/broadinstitute/snakemake-broad-uger
   [cookiecutter-repo]: https://github.com/audreyr/cookiecutter

```
# make sure configuration directory snakemake looks for profiles in exists
mkdir -p ~/.config/snakemake
# use cookiecutter to create a profile in the config directory
cookiecutter --output-dir ~/.config/snakemake gh:shjenkins94/nig-uge
```

This command will prompt for parameters to set.  It will ask to change default
snakemake parameters, log directories. It will ask for a default queue for job
submissions (if left empty, by default it will not add a flag for the queue).
It will finally ask what the desired profile name is.

Once complete, this will allow you to run Snakemake with the cluster
configuration using the `--profile` flag. For example, if the profile name
was `cluster-qsub`, then you can run:

```
snakemake --profile cluster-qsub {...}
```

## Specification of resources/cluster settings

Individual snakemake rules can have the following parameters specified in the
Snakemake file:
+ `threads`: the number of threads needed for the job. If not specified,
  assumed to be 1.
+ `resources`
    - `mem_gb`: the memory required for the rule in gigabytes, which will be
      requested if present

