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
