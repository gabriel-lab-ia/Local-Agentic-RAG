from pathlib import Path
from textwrap import dedent


DOCUMENTS = {
    "data/raw/python/language/exceptions_context_managers.md": dedent(
        """
        ---
        source_id: python_exceptions_context_managers
        title: "Exceptions and Context Managers in Production Python"
        domain: python
        topic: error_handling_and_resources
        url: "https://docs.python.org/3.11/reference/compound_stmts.html"
        license: PSF-2.0
        language: en
        source_type: official_documentation_summary
        ---

        # Exceptions and context managers

        Exceptions communicate that an operation could not satisfy its contract.
        Context managers define deterministic setup and cleanup around a block.

        ## Exception boundaries

        Catch exceptions where the program can recover, translate the error,
        add useful context, or guarantee cleanup.

        Avoid broad handlers that silently discard failures:

        ```python
        try:
            result = execute_training()
        except Exception:
            pass
        ```

        Prefer precise handling:

        ```python
        class ModelLoadError(RuntimeError):
            pass


        def load_model(path: str) -> bytes:
            try:
                with open(path, "rb") as stream:
                    return stream.read()
            except FileNotFoundError as exc:
                raise ModelLoadError(f"model not found: {path}") from exc
        ```

        The `raise ... from exc` syntax preserves causal information.

        ## Exception hierarchy

        Application exceptions should describe domain or operational meaning.

        ```python
        class ApplicationError(Exception):
            pass


        class InvalidPredictionInput(ApplicationError):
            pass


        class EmbeddingServiceUnavailable(ApplicationError):
            pass
        ```

        Do not create a unique exception for every line of code. Create exceptions
        when callers need distinct recovery, reporting, or translation behavior.

        ## Else and finally

        The `else` block runs only when no exception is raised in `try`.
        The `finally` block runs whether the operation succeeds or fails.

        ```python
        try:
            connection.begin()
            persist_metrics(connection)
        except DatabaseError:
            connection.rollback()
            raise
        else:
            connection.commit()
        finally:
            connection.close()
        ```

        ## Context manager protocol

        A synchronous context manager implements `__enter__` and `__exit__`.

        ```python
        class ModelSession:
            def __enter__(self) -> "ModelSession":
                self.open()
                return self

            def __exit__(
                self,
                exc_type,
                exc_value,
                traceback,
            ) -> bool:
                self.close()
                return False
        ```

        Returning `False` allows an active exception to propagate.

        ## contextlib

        Generator-based context managers can be created with `contextlib`.

        ```python
        from collections.abc import Iterator
        from contextlib import contextmanager

        @contextmanager
        def experiment_run(name: str) -> Iterator[dict[str, str]]:
            run = {"name": name, "status": "running"}

            try:
                yield run
            except Exception:
                run["status"] = "failed"
                raise
            else:
                run["status"] = "completed"
        ```

        Exactly one `yield` separates setup from teardown.

        ## Async context managers

        Resources used by asynchronous services may implement
        `__aenter__` and `__aexit__`.

        ```python
        async with client.session() as session:
            response = await session.fetch()
        ```

        ## Production guidance

        Never suppress unexpected exceptions without telemetry.
        Translate low-level errors at architectural boundaries.
        Preserve exception causes.
        Do not use exceptions for ordinary expected branching.
        Use context managers for files, locks, sessions, transactions,
        temporary directories, spans, and managed model resources.
        """
    ).strip()
    + "\n",

    "data/raw/python/language/iterators_generators.md": dedent(
        """
        ---
        source_id: python_iterators_generators
        title: "Iterators, Generators, and Streaming Python"
        domain: python
        topic: iteration_and_streaming
        url: "https://docs.python.org/3.11/reference/expressions.html"
        license: PSF-2.0
        language: en
        source_type: official_documentation_summary
        ---

        # Iterators and generators

        Iteration separates producing values from consuming them. This permits
        lazy computation, streaming pipelines, bounded memory use, and composition.

        ## Iterable and iterator

        An iterable can produce an iterator. An iterator returns one item at a time
        through `__next__` and raises `StopIteration` when exhausted.

        ```python
        numbers = [1, 2, 3]
        iterator = iter(numbers)

        assert next(iterator) == 1
        assert next(iterator) == 2
        ```

        Iterators are stateful and normally single-use.

        ## Generator functions

        A function containing `yield` creates a generator iterator.

        ```python
        from collections.abc import Iterator

        def batches(
            values: list[str],
            size: int,
        ) -> Iterator[list[str]]:
            if size < 1:
                raise ValueError("size must be positive")

            for start in range(0, len(values), size):
                yield values[start : start + size]
        ```

        This pattern is useful for embedding batches, database pagination,
        model inference batches, and file processing.

        ## Streaming files

        ```python
        from collections.abc import Iterator
        from pathlib import Path

        def nonempty_lines(path: Path) -> Iterator[str]:
            with path.open(encoding="utf-8") as stream:
                for line in stream:
                    value = line.strip()

                    if value:
                        yield value
        ```

        The file remains open while iteration is active. Consumers should not
        retain a partially consumed generator indefinitely.

        ## Generator expressions

        ```python
        squared = (value * value for value in range(1_000_000))
        ```

        Generator expressions avoid materializing the entire result, but they do
        not make an expensive algorithm intrinsically faster.

        ## yield from

        `yield from` delegates iteration to another iterable.

        ```python
        def all_chunks(documents: list[list[str]]):
            for document_chunks in documents:
                yield from document_chunks
        ```

        ## send, throw, and close

        Generator objects also support advanced control methods. These features
        enable coroutine-like behavior but can produce difficult control flow.
        Prefer ordinary iteration, async generators, queues, or explicit state
        machines unless bidirectional generator communication is clearly justified.

        ## Async generators

        An asynchronous generator uses `async def` with `yield`.

        ```python
        from collections.abc import AsyncIterator

        async def stream_events() -> AsyncIterator[dict[str, str]]:
            while event := await receive_event():
                yield event
        ```

        Async generators are useful when each item requires asynchronous I/O.

        ## Failure and cleanup

        Exceptions raised by the producer propagate to the consumer.
        Cleanup should be protected with `try/finally` or context managers.

        ## Engineering guidance

        Use iterators for single-pass streams.
        Use sequences when repeated access and indexing are required.
        Avoid converting large streams to lists without a memory budget.
        Make ownership and resource lifetime explicit.
        Document whether an iterable can be consumed more than once.
        """
    ).strip()
    + "\n",

    "data/raw/python/concurrency/asyncio.md": dedent(
        """
        ---
        source_id: python_asyncio_production
        title: "Asyncio for Production Services"
        domain: python
        topic: asynchronous_concurrency
        url: "https://docs.python.org/3.11/library/asyncio.html"
        license: PSF-2.0
        language: en
        source_type: official_documentation_summary
        ---

        # Asyncio for production services

        `asyncio` provides cooperative concurrency using an event loop,
        coroutines, tasks, futures, queues, synchronization primitives, and
        asynchronous network APIs.

        It is primarily useful when many operations spend time waiting for I/O.

        ## Coroutines and tasks

        Calling an async function creates a coroutine object. It does not execute
        the body immediately.

        ```python
        import asyncio

        async def fetch_document(document_id: str) -> str:
            await asyncio.sleep(0.01)
            return document_id

        async def main() -> None:
            task = asyncio.create_task(fetch_document("doc-1"))
            document = await task
            print(document)

        asyncio.run(main())
        ```

        Tasks schedule coroutines for event-loop execution.

        ## Structured concurrency

        Python 3.11 provides `TaskGroup`.

        ```python
        import asyncio

        async def collect_all(ids: list[str]) -> list[str]:
            tasks: list[asyncio.Task[str]] = []

            async with asyncio.TaskGroup() as group:
                for document_id in ids:
                    tasks.append(
                        group.create_task(fetch_document(document_id))
                    )

            return [task.result() for task in tasks]
        ```

        The task group waits for its tasks and coordinates failure propagation.

        ## Timeouts

        External operations need bounded duration.

        ```python
        import asyncio

        async def bounded_fetch() -> str:
            async with asyncio.timeout(5):
                return await fetch_document("doc-1")
        ```

        A timeout policy should reflect upstream budgets and retry strategy.

        ## Cancellation

        Cancellation is part of the contract of async code.

        ```python
        async def worker() -> None:
            try:
                await consume_queue()
            except asyncio.CancelledError:
                await flush_pending_metrics()
                raise
        ```

        Cleanup may be performed, but cancellation should normally be propagated.

        ## Blocking the event loop

        CPU-heavy work and synchronous blocking I/O prevent other tasks from
        progressing.

        ```python
        result = await asyncio.to_thread(blocking_function, argument)
        ```

        Moving work to a thread prevents event-loop blocking, but does not make
        CPU-bound Python execution inherently parallel.

        ## Backpressure

        Unlimited concurrency can overload databases, embedding services,
        model servers, and memory.

        ```python
        semaphore = asyncio.Semaphore(8)

        async def limited_fetch(document_id: str) -> str:
            async with semaphore:
                return await fetch_document(document_id)
        ```

        Bounded queues and semaphores are common backpressure mechanisms.

        ## Common failure modes

        Creating a coroutine without awaiting it.
        Calling blocking libraries in async routes.
        Launching unlimited tasks.
        Swallowing cancellation.
        Sharing clients across incompatible event loops.
        Creating event loops inside library functions.
        Forgetting graceful shutdown.

        ## Decision guidance

        Use asyncio for high-concurrency I/O-bound services.
        Use synchronous code when concurrency adds no operational value.
        Use processes, native code, CUDA, or vectorized libraries for CPU-heavy work.
        Measure throughput, latency, queue depth, timeout rate, and cancellation.
        """
    ).strip()
    + "\n",

    "data/raw/python/concurrency/threads_processes.md": dedent(
        """
        ---
        source_id: python_threads_processes
        title: "Threads and Processes in Python Systems"
        domain: python
        topic: parallelism
        url: "https://docs.python.org/3.11/library/concurrency.html"
        license: PSF-2.0
        language: en
        source_type: official_documentation_summary
        ---

        # Threads and processes

        Threads share process memory. Processes have separate memory spaces.
        The correct choice depends on workload, communication cost, isolation,
        runtime behavior, and deployment constraints.

        ## Threads

        Threads are useful for overlapping blocking I/O and integrating libraries
        that are not asynchronous.

        Shared memory makes communication convenient but introduces synchronization
        requirements.

        ```python
        from threading import Lock

        class Counter:
            def __init__(self) -> None:
                self._value = 0
                self._lock = Lock()

            def increment(self) -> None:
                with self._lock:
                    self._value += 1
        ```

        Correctness must not depend on operations appearing atomic in one CPython
        implementation.

        ## Global interpreter lock

        In standard CPython 3.11, the GIL generally prevents multiple threads from
        executing Python bytecode simultaneously in one process.

        Threads can still improve I/O-bound throughput. Native libraries may release
        the GIL during expensive operations.

        ## Processes

        Multiple processes can execute independently and provide stronger failure
        isolation and CPU parallelism.

        Costs include:

        - process startup;
        - serialization;
        - inter-process communication;
        - duplicated memory;
        - model and accelerator initialization;
        - more complex shutdown.

        ## AI workload considerations

        Loading a large model separately in every process can exceed RAM or VRAM.
        Forking after initializing CUDA or threaded native runtimes can be unsafe.
        Process start methods and library documentation must be considered.

        ## Queues and messages

        Prefer message passing over widespread shared mutable state.

        A message should have a clear schema, bounded size, identifier,
        retry policy, and idempotency behavior.

        ## Worker shutdown

        Production workers need:

        - stop signals;
        - rejection of new work;
        - completion or cancellation of active work;
        - resource cleanup;
        - bounded shutdown time;
        - telemetry for abandoned work.

        ## Selection rule

        Use threads for blocking I/O and compatible native operations.
        Use processes for isolated CPU-bound Python tasks.
        Use asyncio for cooperative high-concurrency I/O.
        Use vectorization, native extensions, PyTorch, or CUDA for numerical work.
        Benchmark with representative payloads before deciding.
        """
    ).strip()
    + "\n",

    "data/raw/python/concurrency/concurrent_futures.md": dedent(
        """
        ---
        source_id: python_concurrent_futures
        title: "Concurrent Futures for Managed Task Execution"
        domain: python
        topic: executor_concurrency
        url: "https://docs.python.org/3.11/library/concurrent.futures.html"
        license: PSF-2.0
        language: en
        source_type: official_documentation_summary
        ---

        # concurrent.futures

        `concurrent.futures` provides a high-level interface for submitting
        callables to thread or process executors.

        ## Thread pool

        ```python
        from concurrent.futures import ThreadPoolExecutor

        def read_document(path: str) -> str:
            with open(path, encoding="utf-8") as stream:
                return stream.read()

        paths = ["a.md", "b.md", "c.md"]

        with ThreadPoolExecutor(max_workers=4) as executor:
            documents = list(executor.map(read_document, paths))
        ```

        Thread pools are commonly suitable for blocking I/O.

        ## Process pool

        ```python
        from concurrent.futures import ProcessPoolExecutor

        def expensive_score(values: list[float]) -> float:
            return sum(value * value for value in values)

        with ProcessPoolExecutor(max_workers=4) as executor:
            scores = list(executor.map(expensive_score, batches))
        ```

        Submitted functions and arguments must satisfy process serialization and
        importability requirements.

        ## Futures

        `submit` returns a Future representing eventual completion.

        ```python
        with ThreadPoolExecutor(max_workers=4) as executor:
            future = executor.submit(read_document, "document.md")

            try:
                content = future.result(timeout=10)
            except TimeoutError:
                future.cancel()
                raise
        ```

        Cancellation only succeeds when execution has not already started.

        ## Completion order

        ```python
        from concurrent.futures import as_completed

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(read_document, path)
                for path in paths
            ]

            for future in as_completed(futures):
                process(future.result())
        ```

        ## Deadlocks

        Pool tasks can deadlock when they wait on other tasks submitted to the same
        exhausted pool. Avoid nested blocking dependencies inside workers.

        ## Capacity

        More workers do not guarantee more throughput. Excessive workers can cause
        context switching, upstream overload, memory pressure, rate-limit failures,
        and database connection exhaustion.

        ## Error handling

        Exceptions raised by tasks are surfaced when retrieving the future result.
        Capture per-task failures when partial success is acceptable.

        ## Engineering guidance

        Bound the worker count.
        Define task timeouts.
        Avoid hidden global mutable state.
        Do not submit unbounded work.
        Preserve input identifiers for tracing.
        Use process pools cautiously with large models and GPU runtimes.
        """
    ).strip()
    + "\n",

    "data/raw/python/testing/pytest_fixtures.md": dedent(
        """
        ---
        source_id: pytest_fixtures_engineering
        title: "Pytest Fixtures for Reliable Python Systems"
        domain: python
        topic: testing
        url: "https://docs.pytest.org/en/stable/explanation/fixtures.html"
        license: MIT
        language: en
        source_type: official_documentation_summary
        ---

        # Pytest fixtures

        Fixtures provide explicit setup, dependencies, reusable test data,
        resources, and teardown.

        ## Basic fixture

        ```python
        import pytest

        @pytest.fixture
        def sample_documents() -> list[str]:
            return [
                "PyTorch autograd computes gradients.",
                "MLflow tracks experiments.",
            ]

        def test_documents_are_not_empty(
            sample_documents: list[str],
        ) -> None:
            assert all(sample_documents)
        ```

        Test functions request fixtures by parameter name.

        ## Yield fixtures

        Code after `yield` performs teardown.

        ```python
        from collections.abc import Iterator
        from pathlib import Path
        import pytest

        @pytest.fixture
        def temporary_corpus(
            tmp_path: Path,
        ) -> Iterator[Path]:
            corpus = tmp_path / "corpus"
            corpus.mkdir()
            yield corpus
        ```

        Prefer built-in temporary-path fixtures over manually managing global
        test directories.

        ## Fixture scopes

        Common scopes include function, class, module, package, and session.

        Wider scopes reduce repeated setup but increase shared-state risk.

        Use the narrowest scope that meets performance requirements.

        ## Fixture dependencies

        ```python
        @pytest.fixture
        def fake_embedder():
            return FakeEmbedder()

        @pytest.fixture
        def retriever(fake_embedder):
            return Retriever(embedder=fake_embedder)
        ```

        A fixture graph should remain understandable. Deep fixture chains can hide
        important test setup.

        ## Factories

        A fixture can return a factory when tests need multiple customized objects.

        ```python
        @pytest.fixture
        def make_chunk():
            def factory(text: str, domain: str = "python"):
                return {"text": text, "domain": domain}

            return factory
        ```

        ## Autouse fixtures

        Autouse fixtures run without explicit test parameters. They are useful for
        universal isolation, but can conceal behavior. Use them sparingly.

        ## Testing external systems

        Unit tests should use small fakes at explicit interfaces.
        Integration tests may start real databases or services.
        Mark slow and environment-dependent tests clearly.

        ## Engineering guidance

        Keep fixtures deterministic.
        Avoid network access in unit tests.
        Prevent session fixtures from leaking mutable state.
        Make teardown resilient.
        Prefer meaningful test data over oversized production copies.
        Test behavior through public interfaces.
        """
    ).strip()
    + "\n",

    "data/raw/python/testing/parametrization_contracts.md": dedent(
        """
        ---
        source_id: pytest_parametrization_contracts
        title: "Parametrized and Contract Testing with Pytest"
        domain: python
        topic: testing_contracts
        url: "https://docs.pytest.org/en/stable/how-to/parametrize.html"
        license: MIT
        language: en
        source_type: official_documentation_summary
        ---

        # Parametrization and contract testing

        Parametrization executes the same test logic with multiple inputs,
        expected outputs, configurations, or implementations.

        ## Table-driven tests

        ```python
        import pytest

        @pytest.mark.parametrize(
            ("value", "expected"),
            [
                ("python", "PYTHON"),
                ("mlops", "MLOPS"),
                ("llmops", "LLMOPS"),
            ],
        )
        def test_normalization(
            value: str,
            expected: str,
        ) -> None:
            assert value.upper() == expected
        ```

        ## Case identifiers

        ```python
        @pytest.mark.parametrize(
            "batch_size",
            [
                pytest.param(1, id="minimum"),
                pytest.param(16, id="default"),
                pytest.param(128, id="large"),
            ],
        )
        def test_valid_batch_sizes(batch_size: int) -> None:
            assert batch_size > 0
        ```

        Descriptive IDs improve failure reports.

        ## Exception contracts

        ```python
        @pytest.mark.parametrize("invalid_size", [0, -1, -32])
        def test_rejects_invalid_batch_size(
            invalid_size: int,
        ) -> None:
            with pytest.raises(
                ValueError,
                match="positive",
            ):
                validate_batch_size(invalid_size)
        ```

        ## Testing multiple implementations

        A protocol can have a reusable contract test.

        ```python
        @pytest.mark.parametrize(
            "embedder_factory",
            [FakeEmbedder, DeterministicEmbedder],
        )
        def test_embedder_contract(embedder_factory) -> None:
            embedder = embedder_factory()
            vectors = embedder.embed(["a", "b"])

            assert len(vectors) == 2
            assert all(vector for vector in vectors)
        ```

        Contract tests verify common behavior without asserting implementation
        details.

        ## Boundary cases

        Include:

        - empty values;
        - minimum and maximum allowed values;
        - malformed data;
        - duplicate identifiers;
        - Unicode;
        - cancellation and timeout;
        - partial upstream failure;
        - deterministic repeatability.

        ## Avoid combinatorial explosion

        Parametrization should represent meaningful equivalence classes and risks.
        Do not generate enormous Cartesian products without a testing strategy.

        Property-based testing is useful when invariants matter across broad input
        spaces. Example-based tests remain important for known regressions and
        domain scenarios.

        ## Engineering guidance

        Give cases meaningful IDs.
        Separate test data from complex test logic.
        Test stable contracts.
        Avoid asserting private implementation structure.
        Keep failures independently diagnosable.
        Turn every fixed production defect into a regression case.
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
