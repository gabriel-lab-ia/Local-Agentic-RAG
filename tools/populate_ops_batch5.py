from pathlib import Path
from textwrap import dedent


DOCUMENTS = {
    "data/raw/mlops/mlflow/tracking.md": dedent(
        """
        ---
        source_id: mlops_mlflow_tracking
        title: "Experiment Tracking with MLflow"
        domain: mlops
        topic: experiment_tracking
        url: "https://mlflow.org/docs/latest/ml/tracking/"
        license: Apache-2.0
        language: en
        source_type: official_documentation_summary
        ---

        # Experiment tracking

        Experiment tracking records the evidence required to understand,
        reproduce, compare, and audit model-development runs.

        A run should connect:

        - source code revision;
        - dataset version;
        - model configuration;
        - hyperparameters;
        - metrics;
        - artifacts;
        - environment;
        - execution status.

        ## Experiments and runs

        An experiment groups related runs. A run represents one execution of a
        training, evaluation, tuning, or validation workflow.

        ```python
        import mlflow

        mlflow.set_experiment("fraud-classification")

        with mlflow.start_run():
            mlflow.log_param("max_depth", 8)
            mlflow.log_param("class_weight", "balanced")

            mlflow.log_metric("validation_roc_auc", 0.91)
            mlflow.log_metric("validation_recall", 0.87)

            mlflow.log_artifact("reports/confusion_matrix.png")
        ```

        ## Parameters, metrics, tags, and artifacts

        Parameters describe run configuration and are generally stable during a
        run.

        Metrics represent numerical observations and may vary over steps or time.

        Tags hold searchable metadata such as:

        - Git commit;
        - dataset identifier;
        - model family;
        - owner;
        - environment;
        - evaluation policy.

        Artifacts include:

        - serialized models;
        - plots;
        - reports;
        - schemas;
        - feature definitions;
        - evaluation results;
        - configuration files.

        ## Reproducibility

        Tracking alone does not guarantee reproducibility.

        A reproducible run also requires:

        - immutable or versioned data;
        - dependency lock state;
        - deterministic configuration where practical;
        - source revision;
        - hardware and runtime metadata;
        - saved preprocessing state.

        ## Nested runs

        Nested runs can represent hyperparameter trials under a parent experiment.

        ```python
        with mlflow.start_run(run_name="search"):
            for learning_rate in learning_rates:
                with mlflow.start_run(nested=True):
                    mlflow.log_param(
                        "learning_rate",
                        learning_rate,
                    )
        ```

        ## Production guidance

        Use stable metric names.
        Log units explicitly.
        Avoid logging secrets or raw private data.
        Record failed and cancelled runs.
        Keep large artifacts in appropriate object storage.
        Make run identifiers visible in deployment metadata.
        """
    ).strip()
    + "\n",
    "data/raw/mlops/mlflow/model_registry.md": dedent(
        """
        ---
        source_id: mlops_mlflow_model_registry
        title: "Model Registry and Lifecycle Governance"
        domain: mlops
        topic: model_registry
        url: "https://mlflow.org/docs/latest/ml/model-registry/"
        license: Apache-2.0
        language: en
        source_type: official_documentation_summary
        ---

        # Model registry

        A model registry manages model versions and the metadata required to move
        models through validation, deployment, rollback, and retirement.

        ## Registered models and versions

        A registered model represents a logical model product.

        Each new artifact can create a model version with metadata linking it to:

        - experiment run;
        - source code;
        - dataset;
        - evaluation;
        - model signature;
        - owner;
        - deployment history.

        ## Aliases

        Aliases provide stable names for selected versions.

        Examples:

        ```text
        champion
        challenger
        candidate
        production
        shadow
        ```

        Deployment systems can resolve an alias rather than embedding a numeric
        model version into application code.

        ## Promotion policy

        Registration must not imply production approval.

        Promotion should require evidence such as:

        - minimum predictive metrics;
        - subgroup evaluation;
        - schema compatibility;
        - latency and memory limits;
        - security validation;
        - reproducibility;
        - human approval where required.

        ## Model signatures

        A model signature describes expected inputs and outputs.

        Signatures help detect:

        - missing fields;
        - incorrect types;
        - shape mismatch;
        - incompatible serving payloads;
        - train-serving skew.

        ## Lineage

        A production model version should be traceable to:

        ```text
        deployment
        → registry version
        → experiment run
        → code revision
        → dataset version
        → configuration
        → evaluation report
        ```

        ## Rollback and retirement

        A registry should support rollback to a previously validated version.

        Retired versions should remain auditable even when they are no longer
        eligible for deployment.

        ## Governance guidance

        Use immutable model versions.
        Use aliases for deployment intent.
        Require explicit promotion gates.
        Record approval decisions.
        Preserve lineage.
        Never overwrite historical model evidence.
        """
    ).strip()
    + "\n",
    "data/raw/mlops/mlflow/model_serving.md": dedent(
        """
        ---
        source_id: mlops_model_serving
        title: "Reliable Model Serving Architecture"
        domain: mlops
        topic: model_serving
        url: "https://mlflow.org/docs/latest/ml/deployment/"
        license: Apache-2.0
        language: en
        source_type: engineering_synthesis
        ---

        # Model serving

        Model serving exposes trained models through a controlled inference
        interface.

        A serving system must preserve correctness, latency, availability,
        observability, and model lineage.

        ## Request lifecycle

        A typical inference request passes through:

        ```text
        authentication
        → authorization
        → schema validation
        → preprocessing
        → model inference
        → post-processing
        → response
        → telemetry
        ```

        Every stage can fail and requires bounded behavior.

        ## Initialization

        Models should generally load during application startup rather than once
        per request.

        Startup should validate:

        - model artifact;
        - model signature;
        - dependency compatibility;
        - device availability;
        - memory capacity;
        - required configuration.

        ## Health endpoints

        Liveness indicates whether the process is running.

        Readiness indicates whether the service can safely accept inference
        requests.

        A process may be alive but not ready while a model is loading.

        ## Batching

        Batching can improve accelerator utilization but adds queue delay.

        A batching policy should define:

        - maximum batch size;
        - maximum waiting time;
        - memory limits;
        - fairness;
        - timeout behavior.

        ## Deployment strategies

        Common strategies include:

        - rolling deployment;
        - blue-green deployment;
        - canary deployment;
        - shadow deployment;
        - champion-challenger evaluation.

        ## Monitoring

        Track:

        - request rate;
        - latency percentiles;
        - error rate;
        - timeout rate;
        - queue depth;
        - batch size;
        - resource use;
        - model version;
        - input drift;
        - prediction distribution;
        - outcome metrics when labels arrive.

        ## Safety

        Validate inputs before expensive inference.
        Bound payload and sequence size.
        Avoid executing model-generated code.
        Isolate untrusted artifacts.
        Protect endpoints with authorization and rate limits.

        ## Engineering guidance

        Separate serving APIs from training code.
        Load immutable model versions.
        expose model version in telemetry.
        support graceful shutdown.
        define rollback before deployment.
        test cold start and degraded dependencies.
        """
    ).strip()
    + "\n",
    "data/raw/llmops/rag/evaluation.md": dedent(
        """
        ---
        source_id: llmops_rag_evaluation
        title: "Evaluation of Retrieval-Augmented Generation Systems"
        domain: llmops
        topic: rag_evaluation
        url: "https://www.deepset.ai/blog/rag-evaluation"
        license: engineering_synthesis
        language: en
        source_type: engineering_synthesis
        ---

        # RAG evaluation

        Retrieval-augmented generation must be evaluated as multiple connected
        components rather than as one opaque text-generation system.

        ## Evaluation layers

        Evaluate separately:

        1. corpus quality;
        2. chunking and metadata;
        3. retrieval;
        4. context construction;
        5. answer generation;
        6. citation correctness;
        7. end-to-end task success.

        ## Retrieval metrics

        Given a labeled evaluation set, retrieval can be measured with:

        - recall at k;
        - precision at k;
        - mean reciprocal rank;
        - normalized discounted cumulative gain;
        - hit rate;
        - source coverage.

        Retrieval evaluation requires relevance judgments or trusted expected
        sources.

        ## Generation metrics

        Evaluate whether the answer is:

        - correct;
        - grounded in retrieved evidence;
        - relevant;
        - complete;
        - concise;
        - citation-aligned;
        - safe.

        Fluency alone is not evidence of correctness.

        ## Faithfulness

        A faithful answer should not make factual claims unsupported by the supplied
        context.

        Each claim can be classified as:

        - supported;
        - contradicted;
        - not present in context;
        - not requiring retrieval evidence.

        ## Evaluation dataset

        A useful test set contains:

        - answerable questions;
        - unanswerable questions;
        - ambiguous questions;
        - multi-document questions;
        - adversarial wording;
        - outdated-information traps;
        - metadata-filtering cases;
        - near-duplicate sources.

        ## Component diagnosis

        A wrong answer may result from:

        ```text
        correct source not retrieved
        retrieved source ranked too low
        chunk missing required context
        prompt discarded evidence
        model ignored evidence
        citation mapped incorrectly
        ```

        Evaluation should identify the failing layer.

        ## Regression testing

        Store evaluation cases in version control.

        Run them after changes to:

        - embedding model;
        - chunk size;
        - overlap;
        - retrieval algorithm;
        - reranker;
        - prompt;
        - generator model;
        - corpus.

        ## Engineering guidance

        Maintain a human-reviewed benchmark.
        Record retrieval and generation results separately.
        Include no-answer behavior.
        Compare changes against a baseline.
        inspect failures manually.
        prevent evaluation data from contaminating the corpus.
        """
    ).strip()
    + "\n",
    "data/raw/llmops/observability/tracing.md": dedent(
        """
        ---
        source_id: llmops_tracing
        title: "Tracing and Observability for LLM Applications"
        domain: llmops
        topic: tracing
        url: "https://opentelemetry.io/docs/concepts/signals/traces/"
        license: Apache-2.0
        language: en
        source_type: engineering_synthesis
        ---

        # LLM tracing and observability

        LLM applications contain several probabilistic and external components.
        Tracing connects the complete request path into one diagnosable execution.

        ## Trace structure

        A trace may contain spans for:

        ```text
        HTTP request
        ├── input validation
        ├── query embedding
        ├── vector search
        ├── reranking
        ├── prompt construction
        ├── model generation
        ├── tool execution
        └── response formatting
        ```

        ## Span attributes

        Useful attributes include:

        - trace and request identifiers;
        - component name;
        - model and version;
        - embedding model;
        - retrieval limit;
        - result count;
        - token counts;
        - latency;
        - retry count;
        - status;
        - cache outcome;
        - tool name;
        - corpus or index version.

        Avoid high-cardinality attributes that cannot be queried efficiently.

        ## Prompt and response privacy

        Full prompts, retrieved documents, tool arguments, and generated responses
        may contain private or regulated data.

        Apply:

        - redaction;
        - sampling;
        - truncation;
        - access control;
        - encryption;
        - retention policy;
        - explicit consent and classification.

        ## Metrics

        Important metrics include:

        - end-to-end latency;
        - time to first token;
        - generation duration;
        - input and output token count;
        - retrieval latency;
        - tool latency;
        - failure rate;
        - timeout rate;
        - citation rate;
        - cache hit rate;
        - cost or compute estimate.

        ## Quality telemetry

        Operational telemetry can include:

        - user feedback;
        - retrieval confidence;
        - grounding checks;
        - citation validity;
        - refusal rate;
        - fallback rate;
        - no-answer rate.

        Quality indicators should not be confused with verified truth.

        ## Correlation

        Deployment version, prompt version, model version, corpus version, and
        evaluation version must be correlated with every production trace.

        ## Engineering guidance

        Instrument component boundaries.
        Propagate trace context across workers and tools.
        Never log secrets.
        Sample intentionally.
        bound trace payload size.
        connect traces to offline evaluation.
        use telemetry to diagnose, not merely collect.
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
