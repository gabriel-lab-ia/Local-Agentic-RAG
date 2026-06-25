from pathlib import Path
from textwrap import dedent


DOCUMENTS = {
    "data/raw/python/observability/structured_logging.md": dedent(
        """
        ---
        source_id: python_structured_logging
        title: "Structured Logging for Production Python Systems"
        domain: python
        topic: observability
        url: "https://docs.python.org/3.11/library/logging.html"
        license: PSF-2.0
        language: en
        source_type: official_documentation_summary
        ---

        # Structured logging

        Logging records discrete events emitted by software. Production logs should
        be machine-readable, correlated across components, bounded in volume, and
        safe for operational use.

        ## Logging architecture

        Python logging separates responsibilities:

        - loggers create records;
        - handlers deliver records;
        - formatters serialize records;
        - filters enrich or reject records.

        Libraries should obtain a module logger and should not configure global
        handlers during import.

        ```python
        import logging

        logger = logging.getLogger(__name__)

        def load_model(model_name: str) -> None:
            logger.info(
                "model_load_started",
                extra={"model_name": model_name},
            )
        ```

        ## Structured event fields

        Useful fields include:

        - event name;
        - timestamp;
        - severity;
        - service and component;
        - environment;
        - request, trace, and span identifiers;
        - model and model version;
        - latency and status;
        - bounded error classification.

        The message should identify the event. Dynamic values should be separate
        fields rather than embedded into prose.

        ## Correlation

        A request identifier or trace identifier should cross API, worker, database,
        retrieval, model, and tool boundaries.

        `contextvars` can carry request-scoped values in async applications without
        relying on unsafe process-wide mutable state.

        ## Severity

        DEBUG is diagnostic detail.
        INFO is normal lifecycle and business events.
        WARNING is degraded or unexpected but recoverable behavior.
        ERROR is a failed operation requiring attention.
        CRITICAL is a severe service-level failure.

        Severity is not a substitute for metrics or alert policy.

        ## Sensitive data

        Never log passwords, tokens, cookies, private keys, raw authorization
        headers, complete prompts containing private data, or unrestricted model
        outputs.

        Use allowlists, redaction, hashing, truncation, and explicit data
        classification.

        ## Operational guidance

        Avoid duplicate handlers.
        Avoid logging the same exception at every layer.
        Use lazy formatting for expensive values.
        Bound payload size and cardinality.
        Configure output at the application composition root.
        Prefer stable event names for queries and dashboards.
        """
    ).strip()
    + "\n",

    "data/raw/python/observability/error_handling.md": dedent(
        """
        ---
        source_id: python_operational_error_handling
        title: "Operational Error Handling in Python Services"
        domain: python
        topic: reliability
        url: "https://docs.python.org/3.11/tutorial/errors.html"
        license: PSF-2.0
        language: en
        source_type: official_documentation_summary
        ---

        # Operational error handling

        Reliable systems classify failures, preserve causal information, expose
        stable public errors, and define recovery behavior.

        ## Failure classes

        Common categories include:

        - invalid input;
        - expected domain rejection;
        - dependency timeout;
        - dependency unavailable;
        - rate limiting;
        - transient conflict;
        - corrupted or incompatible data;
        - invariant violation;
        - operator or configuration error.

        Retry policy, status code, alerting, and user communication depend on the
        category.

        ## Translate at boundaries

        ```python
        class EmbeddingUnavailable(RuntimeError):
            pass

        def embed(texts: list[str]) -> list[list[float]]:
            try:
                return client.embed(texts)
            except TimeoutError as exc:
                raise EmbeddingUnavailable(
                    "embedding service timed out"
                ) from exc
        ```

        Application code should not depend on every exception class emitted by a
        concrete HTTP or database library.

        ## Retry safety

        Retry only when the operation is transient and safe to repeat.

        Consider:

        - idempotency;
        - deadline budget;
        - exponential backoff;
        - jitter;
        - maximum attempts;
        - overload amplification;
        - partial side effects.

        A retry loop without a total deadline can extend an outage.

        ## Public error responses

        External responses should be stable and should not expose stack traces,
        internal paths, credentials, SQL, or dependency details.

        Internal telemetry should retain exception type, cause, stack trace,
        operation, request identifier, and bounded context.

        ## Fail fast versus degrade

        Fail startup for invalid mandatory configuration, incompatible schemas, or
        missing critical credentials.

        Degrade when an optional capability is unavailable and the fallback remains
        correct and visible.

        Never silently degrade model quality without telemetry and an explicit
        product decision.

        ## Engineering guidance

        Preserve causes with exception chaining.
        Define recovery at the correct boundary.
        Do not catch exceptions that cannot be handled.
        Keep user-facing errors stable.
        Separate retryable and permanent failures.
        Test timeout, cancellation, partial failure, and cleanup behavior.
        """
    ).strip()
    + "\n",

    "data/raw/python/performance/profiling.md": dedent(
        """
        ---
        source_id: python_profiling
        title: "Profiling and Performance Engineering in Python"
        domain: python
        topic: performance
        url: "https://docs.python.org/3.11/library/profile.html"
        license: PSF-2.0
        language: en
        source_type: official_documentation_summary
        ---

        # Profiling and performance engineering

        Performance work starts with a measurable objective and representative
        workloads. Optimize observed bottlenecks, not intuition.

        ## Define the objective

        Measure the relevant service-level property:

        - latency percentiles;
        - throughput;
        - startup time;
        - memory peak;
        - GPU utilization;
        - cost per request;
        - queue wait time;
        - batch efficiency.

        Average latency alone can hide tail failures.

        ## Deterministic profiling

        `cProfile` records call counts and time spent in functions.

        ```bash
        python -m cProfile -o profile.out application.py
        ```

        Analyze cumulative time when a function delegates expensive work and
        internal time when the function itself is expensive.

        ## Microbenchmarks

        Use `timeit` for small isolated operations, not for proving end-to-end
        service performance.

        Warm caches, compilation, network variance, thread scheduling, and dataset
        shape can invalidate naive comparisons.

        ## Numerical workloads

        Prefer vectorized NumPy or PyTorch operations over Python loops when the
        operation maps naturally to array computation.

        Reduce:

        - unnecessary device transfers;
        - repeated serialization;
        - tiny kernel launches;
        - unbounded batching;
        - duplicate tokenization or embedding;
        - redundant copies.

        ## Production profiling

        A production-safe profiler should have bounded overhead and controlled
        access. Correlate profiles with request type, model version, payload size,
        hardware, and deployment revision.

        ## Optimization order

        Improve algorithmic complexity first.
        Remove unnecessary work.
        Batch compatible work.
        Cache only stable and reusable results.
        Move proven hotspots to vectorized or native execution.
        Scale resources after software inefficiencies are understood.

        ## Engineering guidance

        Keep a reproducible benchmark.
        Report variance, hardware, versions, and configuration.
        Compare correctness before comparing speed.
        Reject optimizations that destroy maintainability for negligible gain.
        Re-profile after every meaningful change.
        """
    ).strip()
    + "\n",

    "data/raw/python/performance/memory_management.md": dedent(
        """
        ---
        source_id: python_memory_management
        title: "Memory Management for Python and AI Workloads"
        domain: python
        topic: memory
        url: "https://docs.python.org/3.11/library/tracemalloc.html"
        license: PSF-2.0
        language: en
        source_type: official_documentation_summary
        ---

        # Memory management

        Memory behavior depends on object lifetime, ownership, references, native
        libraries, process architecture, and accelerator allocation.

        ## Object lifetime

        CPython primarily uses reference counting and also detects reference cycles.
        A lingering reference keeps an object alive even when application logic no
        longer needs it.

        Common causes include:

        - unbounded caches;
        - global registries;
        - queues without limits;
        - retained closures;
        - exception tracebacks;
        - task collections;
        - large tensors referenced by metrics or callbacks.

        ## tracemalloc

        `tracemalloc` traces Python memory allocations and can compare snapshots.

        ```python
        import tracemalloc

        tracemalloc.start()
        before = tracemalloc.take_snapshot()

        run_pipeline()

        after = tracemalloc.take_snapshot()
        for statistic in after.compare_to(before, "lineno")[:10]:
            print(statistic)
        ```

        It does not account for every allocation made by native libraries or GPU
        runtimes.

        ## Streaming and bounded data structures

        Avoid materializing entire datasets when iteration or pagination is
        sufficient.

        Bound queues, caches, request bodies, result sets, log fields, and batch
        sizes.

        ## Copies and views

        Slicing and conversion semantics differ across lists, NumPy arrays, and
        tensors. Understand whether an operation creates a copy, a view, or a
        shared storage reference.

        Accidental copies increase latency and memory. Unsafe shared views create
        mutation bugs.

        ## Processes and models

        Worker count multiplies memory when each process loads a model, tokenizer,
        index, or cache. Copy-on-write savings can disappear after mutation.

        Accelerator memory must be measured separately from Python heap memory.

        ## Engineering guidance

        Establish memory budgets.
        Measure peak and steady-state usage.
        Test repeated workloads for growth.
        Bound all producer-consumer buffers.
        Release references after large temporary computations.
        Avoid manual garbage collection as a substitute for fixing ownership.
        """
    ).strip()
    + "\n",

    "data/raw/python/packaging/pyproject.md": dedent(
        """
        ---
        source_id: python_pyproject
        title: "Modern pyproject.toml Design"
        domain: python
        topic: packaging
        url: "https://packaging.python.org/en/latest/guides/writing-pyproject-toml/"
        license: MIT
        language: en
        source_type: official_documentation_summary
        ---

        # Modern pyproject.toml design

        `pyproject.toml` centralizes project metadata, build configuration, and tool
        configuration.

        ## Main tables

        `[build-system]` declares the build backend and build requirements.

        `[project]` contains standardized project metadata such as name, version,
        Python requirement, dependencies, entry points, and classifiers.

        `[tool.*]` contains tool-specific configuration.

        ```toml
        [project]
        name = "private-qwen-training"
        version = "0.1.0"
        requires-python = ">=3.11,<3.12"
        dependencies = [
          "chromadb",
          "requests",
        ]

        [dependency-groups]
        dev = [
          "pytest",
          "ruff",
        ]

        [tool.pytest.ini_options]
        testpaths = ["tests"]
        ```

        ## Source layout

        A `src/` layout reduces accidental imports from the repository root and
        better resembles an installed package.

        ## Entry points

        Command-line entry points provide stable executable interfaces instead of
        requiring users to know module paths.

        ## Tool configuration

        Keep configuration near the project when the tool supports it. Avoid
        contradictory settings spread across multiple files.

        ## Version policy

        Declare supported Python versions explicitly. Test them in CI. Do not claim
        support that is not exercised.

        ## Engineering guidance

        Keep runtime and development dependencies distinct.
        Avoid unnecessary upper bounds without evidence.
        Pin applications through a lockfile, not by overconstraining library
        metadata.
        Keep metadata reproducible and reviewable.
        Validate builds in CI.
        """
    ).strip()
    + "\n",

    "data/raw/python/packaging/dependency_management.md": dedent(
        """
        ---
        source_id: python_dependency_management_uv
        title: "Reproducible Dependency Management with uv"
        domain: python
        topic: dependency_management
        url: "https://docs.astral.sh/uv/concepts/projects/dependencies/"
        license: Apache-2.0-MIT
        language: en
        source_type: official_documentation_summary
        ---

        # Reproducible dependency management with uv

        Dependency management converts declared requirements into a resolved,
        reproducible environment.

        ## Declaration and lock state

        Direct requirements belong in `pyproject.toml`.
        The lockfile records the complete resolved graph for repeatable sync.

        ```bash
        uv add fastapi
        uv add --dev pytest ruff
        uv remove fastapi
        uv sync
        uv run pytest
        ```

        Use `uv run` to execute commands in the project environment without relying
        on whichever virtual environment happens to be active in the shell.

        ## Dependency groups

        Development-only tools such as test runners, linters, and type checkers
        belong in dependency groups rather than runtime package metadata.

        ## Version constraints

        Constraints express compatibility policy.

        Too broad can admit incompatible releases.
        Too narrow can block security and compatibility upgrades.
        Exact pins belong primarily in application lock state.

        ## Reproducibility

        CI and deployment should use the committed lockfile.
        Changes to declared dependencies and lock state should be reviewed together.

        ## Private indexes and credentials

        Do not commit index credentials.
        Restrict trusted indexes.
        Understand dependency-confusion risk.
        Prefer explicit source configuration and least-privilege tokens.

        ## Upgrade policy

        Upgrade on a regular cadence.
        Review changelogs for critical dependencies.
        Run tests, static checks, and representative inference or training checks.
        Monitor security advisories and transitive changes.

        ## Engineering guidance

        Use one project environment per repository.
        Avoid activating a virtual environment from another project.
        Commit `pyproject.toml` and `uv.lock`.
        Keep caches and virtual environments out of Git.
        Make dependency updates small and observable.
        """
    ).strip()
    + "\n",

    "data/raw/python/security/secure_python_services.md": dedent(
        """
        ---
        source_id: python_secure_services
        title: "Secure Engineering for Python AI Services"
        domain: python
        topic: security
        url: "https://docs.python.org/3.11/library/security_warnings.html"
        license: PSF-2.0
        language: en
        source_type: security_engineering_synthesis
        ---

        # Secure Python services

        Security must be enforced at trust boundaries, dependency boundaries,
        deployment boundaries, and model-tool boundaries.

        ## Input validation

        Validate type, size, encoding, shape, range, and allowed values before
        expensive processing.

        Set limits for:

        - request bodies;
        - uploaded files;
        - batch size;
        - sequence length;
        - archive expansion;
        - recursion and nesting;
        - execution duration;
        - generated output.

        ## Secrets

        Load secrets from an approved secret-management mechanism.
        Never commit secrets or print them in logs.
        Rotate credentials and apply least privilege.

        ## Dangerous features

        Do not use `eval` or `exec` on untrusted input.
        Do not unpickle untrusted data.
        Treat YAML loaders, template engines, subprocesses, and dynamic imports as
        security boundaries.

        ## Subprocess execution

        Prefer argument lists over shell strings.

        ```python
        import subprocess

        subprocess.run(
            ["python", "-m", "module_name"],
            check=True,
            timeout=30,
        )
        ```

        Avoid `shell=True` with untrusted data.

        ## File safety

        Normalize and constrain paths.
        Prevent path traversal.
        Store uploads outside executable source directories.
        Use generated file names and explicit allowlists.

        ## AI-specific boundaries

        Retrieved text and model output are untrusted data.
        Tool calls require schemas, authorization, allowlists, budgets, and audit
        events.
        Prompt instructions must not override system authorization.
        Generated code must not execute automatically in a privileged environment.

        ## Supply chain

        Lock dependencies.
        Review updates.
        Use trusted indexes.
        Scan dependencies and containers.
        Minimize runtime images and permissions.

        ## Engineering guidance

        Apply defense in depth.
        Fail closed for authorization.
        Separate authentication from authorization.
        Protect logs and traces as sensitive operational data.
        Test abuse cases, not only expected flows.
        """
    ).strip()
    + "\n",
}


def main() -> None:
    for raw_path, content in DOCUMENTS.items():
        path = Path(raw_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"Preenchido: {path}")

    print(f"\nDocumentos preenchidos: {len(DOCUMENTS)}")


if __name__ == "__main__":
    main()
