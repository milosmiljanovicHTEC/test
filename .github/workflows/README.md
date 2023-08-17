# Workflows

## `benchmarks.yml`

<p>
This is a GitHub Actions workflow that benchmarks the performance of MiGraphX, a machine learning framework, using the Open Neural Network Exchange Runtime (ONNX Runtime) framework.
</p>

- ## Trigger
> The workflow will be triggered on workflow dispatch event from caller workflow 
[benchmark.yaml](https://github.com/migraphx-benchmark/AMDMIGraphX/blob/develop/.github/workflows/benchmark.yaml) 

- ## Input Parameters

> - `rocm_version`: 111

> - `script_repo`: 113213213

> - `result_path`: R213

- ## Environment Variables

>- `SCRIPT_PATH`: 111111

- ## Jobs
The following jobs are executed in the workflow:
> - `check_image_version`: This job checks if a new Docker image needs to be built. It runs on a self-hosted machine and sets the output parameter `image` to `true` if a new image needs to be built. This output is used by the next job, `build_image`.

> - `build_image`: This job builds a new Docker image if the `check_image_version` job indicated that one is needed. It runs on a self-hosted machine and depends on the `check_image_version` job. If a new image needs to be built, it checks out the code, checks out the benchmark utilities, and then builds the Docker image. The image is tagged with the current date, and the job sets no outputs.

> - `run_benchmark`: This job runs the benchmark. It runs on a self-hosted machine and depends on the `build_image` job. It exports the start time of the benchmark as an output parameter, `result_time_start`. It then executes the benchmark script in the Docker container and deletes old images and containers. The script takes several arguments, including the result path, which is an input parameter. The job sets no other outputs.

> - `git_push_result`: This job pushes the benchmark results to a GitHub repository. It runs on a self-hosted machine and depends on the `run_benchmark` job. It checks out the results repository, executes two Python scripts to generate a report, and pushes the report to the results repository. The job sets no outputs.

For more details, please refer to the [benchmarks.yml](https://github.com/migraphx-benchmark/actions/blob/main/.github/workflows/benchmarks.yml) file in the repository.

---
## `history.yml`

<p>
This workflow analyzes the historical performance of the MIGraphX project by running a Python script that produces a report between two given dates. The results are uploaded to a Github repository and a link to the report is provided. The workflow requires several input parameters and access to Github credentials as secrets.
</p>

- ## Trigger
> The workflow will be triggered on workflow dispatch event from caller workflow 
[history_HTEC.yaml](https://github.com/migraphx-benchmark/AMDMIGraphX/blob/develop/.github/workflows/history_HTEC.yaml) 

- ## Input Parameters

> - `start_date`: Test25

> - `end_date`: End date for results analysis#111111

> - `benchmark_utils_repo`: Repository where benchmark utils are stored

> - `organization`: Organization based on which location of files will be different

> - `benchmark_utils11_repo`: Repository where benchmark utils are stored

> - `TEST`: TEST

- ## Environment Variables

>- `TEST_RESULTS_PATH`: 111111test

>- `UTILS_DIR`: 324tTEST24 

>- `BLA`: blaaaaa111111111

>- `REPORTS_PATH`: 321321321

>- `REPORTS2424_PATH`: 321321321TEST

- ## Jobs
The workflow has a single job named `performance_test`. The following steps are executed in this job:
> - `Checkout code`: This step checks out the code for the MIGraphX project.

> - `Checkout utils`: This step checks out the benchmark utilities repository specified by the user in the inputs. The repository is checked out to the `UTILS_DIR` directory using the `path` parameter.

> - `Checkout report's repo`: This step checks out the repository where the historical analysis report will be stored. The repository is checked out to the `REPORTS_DIR` directory using the `path` parameter.

> - `Run history script`: This step runs a Python script named `history.py` located in the `UTILS_DIR/scripts/` directory. The script takes the start and end dates specified by the user in the inputs, and the paths to the test results and reports directories specified in the environment variables, as command line arguments. The script generates a historical analysis report for the specified time period.

> - `Upload history results`: This step copies the generated historical analysis report to the `REPORTS_DIR` directory and adds it to the Git repository. It then commits the changes with a message specifying the time period of the report and pushes the changes to the remote repository.

> - `Get link to results repository`: This step prints a link to the historical analysis report repository specified in the inputs, which can be used to access the report.

For more details, please refer to the [history.yml](https://github.com/migraphx-benchmark/actions/blob/main/.github/workflows/history.yml) file in the repository.

---

## `perf-test.yml`

<p>
Overall, this workflow is designed for running performance tests on the MIGraphX library and saving the results to a specified repository.
</p>

- ## Trigger
> The workflow will be triggered on workflow dispatch event from caller workflow 
[performance_HTEC.yaml](https://github.com/migraphx-benchmark/AMDMIGraphX/blob/develop/.github/workflows/performance_HTEC.yaml) 

- ## Input Parameters

> - `rocm_release`: ROCm release versionpesto sesto

> - `performance_reports_repo`: Result repository

> - `benchmark_utils_repo`: Repository where benchmark utils are stored312313123213

> - `organization`: Organization based on which location of files will be different 312312312312313

> - `result_number`: Number of last results

> - `model_timeout`: If model in performance test script passes this threshold, it will be skipped32132131

> - `flags`: -m for Max value; -s for Std dev; -r 'path' for Threshold file

> - `performance_backup_repo`: Repository for backup

- ## Environment Variables

>- `MAIL_TO`: 123

>- `MAIL_FROM`: 5235235325235

>- `MAIL_SUBJECT`: 123

>- `MAIL_BODY`: 123

- ## Jobs
The workflow has a single job named `performance_test`. The following steps are executed in this job:
> - `Update Mailing list based on organization`: If the organization is HTEC, update the mailing list.

> - `Update PR env`: If the event name is `pull_request` update the environment variables related to the pull request.

> - `Checkout code`: Check out the code of the repository.

> - `Checkout utils`: Check out the benchmark utilities repository and place it in the UTILS_DIR environment variable.

> - `Get git SHA`: Get the git SHA for the current commit and store it in the git_sha output variable.

> - `Docker build`: Build a Docker container based on the Daily.Dockerfile in the benchmark utilities repository.

> - `Run performance tests`: Run the performance tests inside the Docker container.
### Comment out step for now:
```
 - Delete old images/containers: This step deletes old Docker images and containers based on a reference and prunes unused images.
```
> - `Checkout report's repo`: This step checks out a Git repository for performance reports using the `actions/checkout` action and sets the path for the repository.

> - `Execute report script`: This step executes a Python script for generating performance reports using the `run` command. The script generates a report, copies the results to a directory, commits the changes, and pushes them to the Git repository checked out in the previous step.

> - `Execute comment script`: This step executes a Python script for creating a comment on a pull request using the `run` command. The script takes parameters such as test results path, result number, and flags.

> - `Create a comment on PR`: This step creates a sticky comment on a pull request using the `marocchino/sticky-pull-request-comment` action. The comment includes a header and the path for the comment script.

> - `Get latest accuracy results`: This step gets the latest accuracy results by changing the working directory and using a command to list the accuracy results and select the latest one.

> - `Create accuracy comment on PR`: This step creates a sticky comment on a pull request for accuracy results using the `marocchino/sticky-pull-request-comment` action. The comment includes a header and the path for the accuracy results.

> - `Get latest report`: This step gets the latest performance report by changing the working directory, listing the reports, and selecting the latest one.

> - `Send mail`: This step sends an email using the `dawidd6/action-send-mail` action. The email includes the subject, recipient, sender, body, and attachment of the latest performance report.

> - `Checkout for backup`: This step checks out a Git repository for performance backup using the `actions/checkout` action and sets the path for the repository.

> - `Backup`: This step creates a backup of performance results if a pull request is closed and merged, or if a scheduled event occurs. It copies the performance results to a directory based on the organization name, adds the changes to Git, and pushes the commit.

> - `Clean merged PR data`: This step runs a script in a Docker container to clean up data after a pull request is merged. It mounts directories and sets a working directory before executing the script.

> - `Clean closed PR data`: This step is similar to the previous step, but it runs a script to clean up data after a pull request is closed without being merged.

For more details, please refer to the [perf-test.yml](https://github.com/migraphx-benchmark/actions/blob/main/.github/workflows/perf-test.yml) file in the repository.

---

## `rocm-release.yml`

<p>
This workflow automates the process of building a Docker image for the ROCm (Radeon Open Compute) software stack developed and maintained by Advanced Micro Devices (AMD) Corporation. ROCm is an AMD software stack designed for high-performance computing (HPC) and machine learning (ML) workloads, with a focus on providing support for AMD hardware, including GPUs and CPUs.
</p>

- ## Trigger
> The workflow will be triggered on workflow dispatch event from caller workflow 
[rocm-image-release_HTEC.yaml](https://github.com/migraphx-benchmark/AMDMIGraphX/blob/develop/.github/workflows/rocm-image-release_HTEC.yaml) 

- ## Input Parameters

> - `rocm_release`: ROCm release version2626262

> - `utils_repo`: Repository for benchmark utils05050

> - `base_image`: Base image for rocm Docker buildfhfg

> - `docker_image`: Docker image name for rocm Docker buildhfgf

> - `build_navi`: Build navi numberhfgh

- ## Environment Variables

>- `daad`: 4234234

- ## Jobs
The following jobs are executed in the workflow:
> - `check_image_version`: This job checks whether the specified Docker image already exists. If it does, the job checks the `overwrite` flag to determine whether to delete the existing image and create a new one. This job outputs a boolean value indicating whether a new image needs to be built.

> - `build_image`: This job builds the ROCm Docker image if the `check_image_version` job determined that a new image needs to be built. This job checks out the benchmark utilities repository, sets environment variables based on the input parameters, and runs a script to build the Docker image.

For more details, please refer to the [rocm-release.yml](https://github.com/migraphx-benchmark/actions/blob/main/.github/workflows/rocm-release.yml) file in the repository.

---
