from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


RAW_DATA_DIR = Path("data/raw")


@dataclass(frozen=True)
class DocumentSpec:
    domain: str
    category: str
    source_id: str
    filename: str
    title: str
    topic: str
    url: str
    definition: str
    risks: tuple[str, ...]
    controls: tuple[str, ...]
    verification: tuple[str, ...]


SPECS: tuple[DocumentSpec, ...] = (
    # ------------------------------------------------------------------
    # Cybersecurity
    # ------------------------------------------------------------------
    DocumentSpec(
        "cybersecurity",
        "foundations",
        "cybersecurity_security_engineering",
        "security_engineering.md",
        "Security Engineering Fundamentals",
        "security_engineering",
        "https://www.nist.gov/cyberframework",
        "Security engineering treats confidentiality, integrity, availability, authenticity, accountability, and resilience as system properties that must be designed, implemented, tested, and operated.",
        (
            "Security is added late and becomes a collection of disconnected controls.",
            "Assets, identities, dependencies, and trust assumptions are undocumented.",
            "Compliance evidence is mistaken for proof that the system is secure.",
            "Detection and recovery are ignored in favor of prevention-only designs.",
        ),
        (
            "Define assets, actors, trust boundaries, abuse cases, and unacceptable outcomes.",
            "Apply defense in depth and least privilege at every boundary.",
            "Design prevention, detection, response, recovery, and evidence preservation together.",
            "Turn architectural assumptions into explicit tests and operational telemetry.",
        ),
        (
            "Review data-flow diagrams and trust boundaries.",
            "Validate access-control decisions with negative tests.",
            "Exercise incident and recovery procedures.",
            "Audit whether each control has an owner and measurable outcome.",
        ),
    ),
    DocumentSpec(
        "cybersecurity",
        "governance",
        "cybersecurity_nist_csf",
        "nist_csf.md",
        "Cybersecurity Risk Management with NIST CSF",
        "risk_management",
        "https://www.nist.gov/cyberframework",
        "The NIST Cybersecurity Framework organizes risk-management outcomes around Govern, Identify, Protect, Detect, Respond, and Recover.",
        (
            "Risk decisions have no accountable owner.",
            "Asset and dependency inventories are incomplete.",
            "Residual risk is hidden after controls are implemented.",
            "Architecture changes are deployed without reassessing exposure.",
        ),
        (
            "Assign risk owners and treatment decisions.",
            "Maintain inventories of systems, identities, data, models, dependencies, and suppliers.",
            "Prioritize controls using business impact, exposure, threat likelihood, and control effectiveness.",
            "Reassess risk after changes to architecture, vendors, identity, or public exposure.",
        ),
        (
            "Inspect risk-register freshness and ownership.",
            "Trace critical assets to controls, alerts, response plans, and recovery objectives.",
            "Test whether governance decisions are reflected in engineering backlogs.",
            "Review accepted risk and expiration dates.",
        ),
    ),
    DocumentSpec(
        "cybersecurity",
        "architecture",
        "cybersecurity_threat_modeling",
        "threat_modeling.md",
        "Threat Modeling and Trust Boundaries",
        "threat_modeling",
        "https://www.cisa.gov/securebydesign",
        "Threat modeling identifies assets, attackers, entry points, trust boundaries, attack paths, and security requirements before failures become incidents.",
        (
            "External inputs are treated as trusted because they come from internal networks.",
            "Data stores, queues, model endpoints, and administrative paths are omitted.",
            "Only known vulnerabilities are considered, while design-level abuse cases are ignored.",
            "Threat models become stale after system changes.",
        ),
        (
            "Map data flows, processes, stores, identities, external services, and administrative interfaces.",
            "Mark every point where trust, identity, ownership, or validation changes.",
            "Analyze spoofing, tampering, repudiation, information disclosure, denial of service, and privilege escalation.",
            "Convert threats into requirements, controls, tests, and monitoring signals.",
        ),
        (
            "Review threat models during architecture and release reviews.",
            "Confirm each high-risk threat has a mitigation and test.",
            "Test trust-boundary failures and cross-tenant scenarios.",
            "Update diagrams after material changes.",
        ),
    ),
    DocumentSpec(
        "cybersecurity",
        "identity",
        "cybersecurity_authentication_authorization",
        "authentication_authorization.md",
        "Authentication, Authorization, and Identity Boundaries",
        "identity_access_management",
        "https://pages.nist.gov/800-63-3/",
        "Authentication establishes identity; authorization decides whether that identity may perform an action on a resource under current policy.",
        (
            "Authentication success is treated as authorization for every action.",
            "Shared accounts eliminate accountability.",
            "Long-lived credentials expand the impact of compromise.",
            "Object-level authorization is missing from APIs.",
        ),
        (
            "Separate authentication, session management, and authorization logic.",
            "Authorize every sensitive action and object access.",
            "Use narrow scopes, short-lived credentials, and workload identities.",
            "Log the identity, action, resource, policy result, and outcome without exposing secrets.",
        ),
        (
            "Test horizontal and vertical privilege escalation.",
            "Review dormant identities and excessive permissions.",
            "Verify token audience, issuer, expiration, and scope.",
            "Confirm authorization failures are safe and observable.",
        ),
    ),
    DocumentSpec(
        "cybersecurity",
        "access_control",
        "cybersecurity_least_privilege",
        "least_privilege.md",
        "Least Privilege and Privilege Separation",
        "least_privilege",
        "https://csrc.nist.gov/glossary/term/least_privilege",
        "Least privilege grants only the permissions required for a task, for the minimum duration and smallest practical scope.",
        (
            "Build, deployment, runtime, and administration share the same identity.",
            "Permissions accumulate and are never reviewed.",
            "Broad wildcard policies hide the real access model.",
            "Emergency privileges become permanent.",
        ),
        (
            "Separate human, service, CI, deployment, and break-glass identities.",
            "Use just-in-time elevation and approval for sensitive actions.",
            "Prefer explicit resources and actions over wildcards.",
            "Remove unused permissions and expired access.",
        ),
        (
            "Review effective permissions, not only declared roles.",
            "Test that denied operations remain denied.",
            "Audit use of elevated and emergency access.",
            "Measure privilege reduction over time.",
        ),
    ),
    DocumentSpec(
        "cybersecurity",
        "secure_design",
        "cybersecurity_secure_by_design",
        "secure_by_design.md",
        "Secure by Design and Secure by Default",
        "secure_by_design",
        "https://www.cisa.gov/securebydesign",
        "Secure by design makes security a core product requirement; secure by default enables protective behavior without requiring expert configuration.",
        (
            "Unsafe features are enabled by default.",
            "Customers must discover and configure essential protections themselves.",
            "Repeated vulnerability classes are handled only through patching.",
            "Security ownership is pushed entirely to operators.",
        ),
        (
            "Eliminate unsafe defaults and unnecessary exposure.",
            "Provide strong authentication, logging, update, and recovery capabilities by default.",
            "Treat recurring vulnerability classes as architecture defects.",
            "Measure security outcomes across design, implementation, deployment, and support.",
        ),
        (
            "Install and deploy with default settings in a test environment.",
            "Verify sensitive interfaces are not exposed automatically.",
            "Track recurring defect classes and prevention work.",
            "Review whether protective controls require additional purchase or expert setup.",
        ),
    ),
    DocumentSpec(
        "cybersecurity",
        "secrets",
        "cybersecurity_secrets_management",
        "secrets_management.md",
        "Secrets Management for Production Systems",
        "secrets_management",
        "https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html",
        "Secrets include passwords, API keys, signing keys, tokens, and private certificates that grant access or establish trust.",
        (
            "Secrets are committed to source control or container images.",
            "The same secret is reused across environments.",
            "Secrets appear in logs, traces, prompts, metrics, or crash dumps.",
            "Rotation and revocation procedures are untested.",
        ),
        (
            "Use dedicated secret stores or workload identity.",
            "Inject secrets at runtime with narrow access.",
            "Rotate, revoke, and expire credentials.",
            "Redact secrets from telemetry, errors, prompts, and support artifacts.",
        ),
        (
            "Scan repositories, build outputs, images, and logs for exposed secrets.",
            "Test rotation without service interruption.",
            "Review secret-access audit logs.",
            "Confirm compromised credentials can be revoked quickly.",
        ),
    ),
    DocumentSpec(
        "cybersecurity",
        "vulnerability_management",
        "cybersecurity_vulnerability_management",
        "vulnerability_management.md",
        "Vulnerability Management as an Engineering Loop",
        "vulnerability_management",
        "https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
        "Vulnerability management continuously discovers, validates, prioritizes, remediates, verifies, and prevents security weaknesses.",
        (
            "Severity scores are used without exposure or exploitability context.",
            "Transitive dependencies and embedded components are not inventoried.",
            "Patches are declared complete without deployment verification.",
            "Actively exploited vulnerabilities compete with routine backlog work.",
        ),
        (
            "Maintain software and asset inventories.",
            "Prioritize internet-exposed, privileged, high-impact, and actively exploited weaknesses.",
            "Assign remediation ownership and deadlines.",
            "Verify fixes in source, build artifacts, deployment, and runtime.",
        ),
        (
            "Compare scanner findings with deployed versions.",
            "Test whether mitigations actually block the vulnerable path.",
            "Track mean time to remediate by risk class.",
            "Convert recurring findings into preventive controls.",
        ),
    ),
    DocumentSpec(
        "cybersecurity",
        "supply_chain",
        "cybersecurity_software_supply_chain",
        "software_supply_chain.md",
        "Software Supply-Chain Security",
        "software_supply_chain",
        "https://slsa.dev/spec/v1.0/",
        "Software supply-chain security protects source, dependencies, build systems, package registries, artifacts, and deployment paths from unauthorized modification.",
        (
            "Untrusted dependencies execute during build or installation.",
            "CI identities have excessive repository or deployment privileges.",
            "Artifacts cannot be traced to source and build configuration.",
            "Package names or indexes permit dependency confusion.",
        ),
        (
            "Pin dependencies through reviewed lock state.",
            "Protect branches, build identities, runners, and publishing credentials.",
            "Generate provenance and sign release artifacts.",
            "Restrict trusted package sources and verify artifact integrity.",
        ),
        (
            "Rebuild releases in controlled environments.",
            "Verify signatures and provenance before deployment.",
            "Audit who may publish packages or modify pipelines.",
            "Exercise dependency-compromise response procedures.",
        ),
    ),
    DocumentSpec(
        "cybersecurity",
        "api_security",
        "cybersecurity_api_security",
        "api_security.md",
        "API Security for AI and Data Services",
        "api_security",
        "https://owasp.org/API-Security/",
        "API security protects identities, objects, functions, resources, data exposure, and downstream integrations.",
        (
            "Object identifiers permit cross-tenant access.",
            "Expensive model or retrieval operations lack resource limits.",
            "Server-side integrations accept attacker-controlled destinations.",
            "Errors expose internal implementation or sensitive data.",
        ),
        (
            "Authorize at object and action level.",
            "Validate schemas, content types, lengths, ranges, and state transitions.",
            "Apply rate, concurrency, token, timeout, and cost limits.",
            "Use safe error responses, idempotency, and replay protection where required.",
        ),
        (
            "Test broken object-level and function-level authorization.",
            "Fuzz malformed and oversized requests.",
            "Test resource exhaustion and dependency failures.",
            "Review outbound network and callback controls.",
        ),
    ),
    DocumentSpec(
        "cybersecurity",
        "incident_response",
        "cybersecurity_incident_response",
        "incident_response.md",
        "Security Incident Response",
        "incident_response",
        "https://csrc.nist.gov/pubs/sp/800/61/r2/final",
        "Incident response coordinates preparation, detection, analysis, containment, eradication, recovery, communication, and lessons learned.",
        (
            "Teams cannot identify owners or escalation paths.",
            "Containment destroys evidence required for investigation.",
            "Credentials and secrets remain valid after compromise.",
            "Lessons learned do not change architecture or tests.",
        ),
        (
            "Define severity, ownership, communication, and legal escalation.",
            "Preserve evidence, clocks, logs, images, and chain of custody.",
            "Contain access while maintaining necessary forensic data.",
            "Rotate credentials, validate recovery, and create preventive engineering work.",
        ),
        (
            "Run tabletop and technical exercises.",
            "Measure detection, containment, and recovery times.",
            "Verify evidence sources are complete and synchronized.",
            "Track completion of lessons-learned actions.",
        ),
    ),
    DocumentSpec(
        "cybersecurity",
        "testing",
        "cybersecurity_security_testing",
        "security_testing.md",
        "Security Testing and Abuse-Case Validation",
        "security_testing",
        "https://owasp.org/www-project-web-security-testing-guide/",
        "Security testing evaluates expected functionality and resistance to malicious input, unauthorized sequences, degraded dependencies, and operational abuse.",
        (
            "Only happy paths are tested.",
            "Security defects are fixed without regression tests.",
            "Testing ignores identity, tenancy, rate, concurrency, and failure behavior.",
            "Production controls differ from tested controls.",
        ),
        (
            "Write misuse, abuse, and negative authorization cases.",
            "Test malformed input, timeouts, cancellation, retries, and partial failure.",
            "Verify redaction, auditability, rate limits, and resource budgets.",
            "Keep security tests in CI and representative deployment environments.",
        ),
        (
            "Map tests to threats and requirements.",
            "Reproduce discovered vulnerabilities as regression tests.",
            "Review coverage of critical trust boundaries.",
            "Test production-equivalent configuration and policy.",
        ),
    ),
    # ------------------------------------------------------------------
    # Linux security
    # ------------------------------------------------------------------
    DocumentSpec(
        "linux_security",
        "identity",
        "linux_security_permissions",
        "permissions.md",
        "Linux Users, Groups, Ownership, and Permissions",
        "linux_permissions",
        "https://man7.org/linux/man-pages/man7/credentials.7.html",
        "Linux discretionary access control uses process credentials, file ownership, groups, and mode bits to decide access.",
        (
            "Services run as root without necessity.",
            "World-writable files or directories allow unauthorized modification.",
            "Broad group membership expands access silently.",
            "Setuid and setgid executables create unexpected privilege paths.",
        ),
        (
            "Run each service as a dedicated non-root user.",
            "Keep writable paths explicit and minimal.",
            "Use restrictive ownership and permissions.",
            "Audit privileged executables and sensitive directories.",
        ),
        (
            "Inspect runtime UID, GID, supplementary groups, and umask.",
            "Search for world-writable and setuid files.",
            "Test service operation after removing unnecessary permissions.",
            "Review permissions after package and deployment changes.",
        ),
    ),
    DocumentSpec(
        "linux_security",
        "capabilities",
        "linux_security_capabilities",
        "capabilities.md",
        "Linux Capabilities and Privilege Decomposition",
        "linux_capabilities",
        "https://man7.org/linux/man-pages/man7/capabilities.7.html",
        "Linux capabilities split traditional root privilege into independently assignable units.",
        (
            "A workload receives broad capabilities such as CAP_SYS_ADMIN.",
            "Capabilities persist through container or service configuration changes.",
            "Ambient capabilities grant privilege to child processes.",
            "Root is retained because individual requirements were never analyzed.",
        ),
        (
            "Drop every capability not explicitly required.",
            "Avoid privileged containers and broad capability sets.",
            "Review effective, permitted, inheritable, bounding, and ambient sets.",
            "Combine capability reduction with seccomp, LSM policy, and filesystem controls.",
        ),
        (
            "Inspect process capabilities at runtime.",
            "Test the workload with an empty capability set and add only proven requirements.",
            "Alert on unexpected privileged execution.",
            "Review changes to service and container definitions.",
        ),
    ),
    DocumentSpec(
        "linux_security",
        "process_security",
        "linux_security_no_new_privileges",
        "no_new_privileges.md",
        "The Linux no_new_privs Security Boundary",
        "no_new_privs",
        "https://docs.kernel.org/userspace-api/no_new_privs.html",
        "The no_new_privs flag prevents execve from granting privileges that were not already available to the calling process.",
        (
            "A child process gains privilege through setuid binaries or file capabilities.",
            "Service hardening assumes no privilege transition without enforcing it.",
            "The flag is misunderstood as a complete sandbox.",
            "Runtime configuration differs from the intended service policy.",
        ),
        (
            "Enable no_new_privs for services that do not require privilege transitions.",
            "Use it with unprivileged seccomp filtering.",
            "Combine it with capability, filesystem, namespace, and LSM restrictions.",
            "Document any workload that genuinely requires privilege gain after startup.",
        ),
        (
            "Inspect the process status and service configuration.",
            "Attempt representative privilege-transition paths in tests.",
            "Confirm child processes inherit the restriction.",
            "Review exceptions as security-sensitive changes.",
        ),
    ),
    DocumentSpec(
        "linux_security",
        "sandboxing",
        "linux_security_seccomp",
        "seccomp.md",
        "Seccomp System-Call Filtering",
        "seccomp",
        "https://docs.kernel.org/userspace-api/seccomp_filter.html",
        "Seccomp reduces kernel attack surface by filtering system calls available to a process.",
        (
            "A compromised process can invoke unnecessary kernel interfaces.",
            "A profile blocks startup but misses dangerous steady-state paths.",
            "Architecture-specific syscall behavior is ignored.",
            "Profiles are disabled after operational failures instead of being corrected.",
        ),
        (
            "Derive policies from actual workload requirements.",
            "Prefer narrow allowlists for specialized services.",
            "Account for architecture, libc wrappers, startup, shutdown, and error paths.",
            "Version and test profiles with the application.",
        ),
        (
            "Run tests under the exact deployment profile.",
            "Exercise upgrades, failures, cancellation, and signal handling.",
            "Monitor denied syscalls and investigate before broadening policy.",
            "Compare profile changes during code review.",
        ),
    ),
    DocumentSpec(
        "linux_security",
        "isolation",
        "linux_security_namespaces",
        "namespaces.md",
        "Linux Namespaces and Isolation Boundaries",
        "linux_namespaces",
        "https://man7.org/linux/man-pages/man7/namespaces.7.html",
        "Namespaces isolate selected views of processes, mounts, networks, users, hostnames, cgroups, and IPC resources.",
        (
            "Namespaces are treated as complete isolation by themselves.",
            "Host mounts, sockets, devices, or namespaces are exposed to containers.",
            "User-namespace mappings are misunderstood.",
            "Shared kernel attack surface is ignored.",
        ),
        (
            "Use namespaces with capability reduction, seccomp, LSM policy, and resource controls.",
            "Avoid host PID, network, IPC, and broad mount sharing.",
            "Protect sensitive devices, sockets, and filesystem paths.",
            "Understand UID and GID mappings across user namespaces.",
        ),
        (
            "Inspect namespace membership and mount propagation.",
            "Test access to host resources from isolated workloads.",
            "Review container and systemd namespace settings.",
            "Validate isolation after runtime upgrades.",
        ),
    ),
    DocumentSpec(
        "linux_security",
        "mandatory_access_control",
        "linux_security_lsm",
        "linux_security_modules.md",
        "Linux Security Modules",
        "linux_security_modules",
        "https://docs.kernel.org/security/lsm.html",
        "Linux Security Modules provide kernel hooks for mandatory access control and other security policies.",
        (
            "Mandatory controls are disabled to resolve application friction.",
            "Policy is not versioned with application changes.",
            "Denials are ignored or broadly allowed.",
            "Operators do not know which security module is active.",
        ),
        (
            "Select an enforcement model appropriate to the environment.",
            "Version policy and review changes as code.",
            "Use enforcing mode after validation.",
            "Treat denials as evidence requiring investigation.",
        ),
        (
            "Confirm the active LSM configuration.",
            "Test expected access and denied access.",
            "Review policy exceptions and broad rules.",
            "Monitor denials and policy drift.",
        ),
    ),
    DocumentSpec(
        "linux_security",
        "mandatory_access_control",
        "linux_security_selinux_apparmor",
        "selinux_apparmor.md",
        "SELinux and AppArmor Policy Engineering",
        "selinux_apparmor",
        "https://docs.kernel.org/admin-guide/LSM/index.html",
        "SELinux and AppArmor constrain process access beyond discretionary Unix permissions.",
        (
            "Policies permit entire path trees or broad domains.",
            "Learning-mode output is accepted without review.",
            "Applications write to unexpected locations.",
            "Policy exceptions outlive the incident that created them.",
        ),
        (
            "Model expected files, sockets, capabilities, processes, and transitions.",
            "Keep services in enforcing mode after testing.",
            "Minimize writable and executable paths.",
            "Review every policy exception as a security change.",
        ),
        (
            "Exercise normal and failure behavior under enforcement.",
            "Inspect denial logs and application impact.",
            "Test unauthorized path, socket, and execution access.",
            "Remove stale exceptions.",
        ),
    ),
    DocumentSpec(
        "linux_security",
        "sandboxing",
        "linux_security_landlock",
        "landlock.md",
        "Landlock for Unprivileged Process Sandboxing",
        "landlock",
        "https://docs.kernel.org/userspace-api/landlock.html",
        "Landlock lets a process restrict its own future access to kernel objects, especially filesystem resources, without requiring global administrator policy.",
        (
            "The process retains ambient filesystem access it does not need.",
            "Restrictions are applied after untrusted input is processed.",
            "Unsupported ABI features are assumed to be enforced.",
            "Landlock is treated as a replacement for all other controls.",
        ),
        (
            "Apply restrictions before handling untrusted data.",
            "Grant only required read, write, execute, create, and remove access.",
            "Detect supported ABI and degrade safely.",
            "Combine Landlock with seccomp, no_new_privs, and identity controls.",
        ),
        (
            "Test denied access outside allowed paths.",
            "Verify behavior across supported kernels.",
            "Inspect fallback behavior when features are unavailable.",
            "Review path rules after application changes.",
        ),
    ),
    DocumentSpec(
        "linux_security",
        "service_hardening",
        "linux_security_systemd",
        "systemd_hardening.md",
        "Systemd Service Hardening",
        "systemd_hardening",
        "https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html",
        "Systemd can constrain service privileges, namespaces, filesystems, devices, address families, capabilities, and system calls.",
        (
            "Services inherit broad host access by default.",
            "Writable paths and network families are unrestricted.",
            "Hardening options are copied without workload testing.",
            "Operational fixes disable multiple protections.",
        ),
        (
            "Use NoNewPrivileges, PrivateTmp, ProtectSystem, ProtectHome, and capability bounding.",
            "Restrict writable paths, devices, namespaces, address families, and syscalls.",
            "Keep service credentials and runtime directories scoped.",
            "Apply controls incrementally with representative tests.",
        ),
        (
            "Run systemd-analyze security as a review aid.",
            "Inspect the effective unit configuration.",
            "Exercise startup, reload, shutdown, and failure paths.",
            "Alert on drift from approved unit files.",
        ),
    ),
    DocumentSpec(
        "linux_security",
        "remote_access",
        "linux_security_ssh",
        "ssh_hardening.md",
        "SSH Hardening and Administrative Access",
        "ssh_hardening",
        "https://man.openbsd.org/sshd_config",
        "SSH hardening reduces exposure of remote administration and strengthens authentication, authorization, and auditability.",
        (
            "Password authentication remains exposed to broad networks.",
            "Root login is permitted directly.",
            "Old keys and accounts remain valid.",
            "Administrative activity is not attributable to individuals.",
        ),
        (
            "Prefer strong key-based or federated authentication.",
            "Restrict root login and administrative groups.",
            "Use network controls, bastions, and session accountability.",
            "Rotate keys and remove dormant accounts.",
        ),
        (
            "Review effective sshd configuration.",
            "Test disabled methods and restricted users.",
            "Monitor authentication failures and key changes.",
            "Audit administrative sessions and privilege elevation.",
        ),
    ),
    DocumentSpec(
        "linux_security",
        "detection",
        "linux_security_audit",
        "audit_detection.md",
        "Linux Audit and Detection Engineering",
        "linux_audit",
        "https://man7.org/linux/man-pages/man8/auditd.8.html",
        "Linux audit data supports accountability and investigation for identity, privilege, execution, policy, and sensitive-resource changes.",
        (
            "High-value events are not collected.",
            "Audit rules create excessive noise and hide meaningful activity.",
            "Logs remain only on the compromised host.",
            "Host, container, deployment, and user context cannot be correlated.",
        ),
        (
            "Audit identity, privilege, executable, policy, and sensitive-file changes.",
            "Centralize logs with integrity and access protection.",
            "Attach host, process, user, container, and deployment context.",
            "Tune noise while preserving critical security events.",
        ),
        (
            "Generate representative events and confirm arrival.",
            "Test time synchronization and retention.",
            "Review gaps during high load or storage failure.",
            "Exercise investigation queries.",
        ),
    ),
    DocumentSpec(
        "linux_security",
        "containers",
        "linux_security_container_host",
        "container_host_security.md",
        "Container and Host Security Boundaries",
        "container_security",
        "https://kubernetes.io/docs/concepts/security/",
        "Containers share the host kernel, so security depends on runtime configuration, workload identity, image provenance, kernel controls, and host hardening.",
        (
            "Containers run privileged or as root.",
            "Host devices, sockets, namespaces, or sensitive mounts are exposed.",
            "Images and hosts are patched on different timelines.",
            "Runtime identity has broad cluster or cloud permissions.",
        ),
        (
            "Run as non-root and disallow privilege escalation.",
            "Drop capabilities, use read-only filesystems, and apply seccomp.",
            "Avoid host namespaces, broad mounts, and device access.",
            "Verify image provenance and restrict workload identity.",
        ),
        (
            "Inspect effective runtime security settings.",
            "Attempt access to host resources in tests.",
            "Scan images and hosts for known vulnerabilities.",
            "Review cluster, cloud, and registry permissions together.",
        ),
    ),
    # ------------------------------------------------------------------
    # ML security
    # ------------------------------------------------------------------
    DocumentSpec(
        "ml_security",
        "foundations",
        "ml_security_adversarial_ml",
        "adversarial_ml.md",
        "Adversarial Machine Learning Fundamentals",
        "adversarial_machine_learning",
        "https://csrc.nist.gov/pubs/ai/100/2/e2025/final",
        "Adversarial machine learning studies attacks and mitigations across the ML lifecycle, including training, evaluation, deployment, and interaction.",
        (
            "Attacker goals, knowledge, capabilities, and access are unspecified.",
            "Only prediction accuracy is evaluated.",
            "Training and inference threats are mixed together.",
            "Mitigations are tested only against static attacks.",
        ),
        (
            "Define integrity, availability, privacy, and misuse objectives.",
            "Model attacker knowledge, access, budget, and influence.",
            "Map threats to data collection, training, evaluation, deployment, and feedback stages.",
            "Evaluate controls against adaptive and changing attacks.",
        ),
        (
            "Document the threat model with every evaluation.",
            "Test attacks that match realistic access assumptions.",
            "Measure clean performance and security performance separately.",
            "Reevaluate after model, data, or interface changes.",
        ),
    ),
    DocumentSpec(
        "ml_security",
        "threat_modeling",
        "ml_security_threat_modeling",
        "threat_modeling.md",
        "Threat Modeling for Machine Learning Systems",
        "ml_threat_modeling",
        "https://atlas.mitre.org/",
        "ML threat modeling covers data collection, labeling, feature pipelines, training infrastructure, model artifacts, serving paths, feedback loops, and downstream decisions.",
        (
            "Data writers and labelers are assumed trustworthy.",
            "Pretrained models and datasets are accepted without provenance.",
            "Query access and observable outputs are not considered.",
            "Feedback loops allow attacker influence over future training.",
        ),
        (
            "Identify who can read or modify data, labels, features, models, embeddings, logits, and gradients.",
            "Map suppliers, pretrained artifacts, registries, and evaluation sets.",
            "Define query, rate, output, and feedback access.",
            "Link attack paths to business and safety impact.",
        ),
        (
            "Review permissions across the entire ML pipeline.",
            "Test integrity checks on data and artifacts.",
            "Audit external components and provenance.",
            "Exercise poisoning and extraction response scenarios.",
        ),
    ),
    DocumentSpec(
        "ml_security",
        "inference_attacks",
        "ml_security_evasion",
        "evasion_attacks.md",
        "Evasion Attacks and Adversarial Examples",
        "evasion_attacks",
        "https://csrc.nist.gov/pubs/ai/100/2/e2025/final",
        "Evasion attacks manipulate inference-time inputs to cause incorrect or attacker-preferred model behavior without necessarily changing the model.",
        (
            "Robustness is inferred from normal validation accuracy.",
            "Preprocessing behavior creates exploitable discontinuities.",
            "Detection thresholds are tuned on known attacks only.",
            "Operational constraints differ from laboratory evaluations.",
        ),
        (
            "Define allowable perturbations and realistic attacker control.",
            "Evaluate transformations, preprocessing, and end-to-end pipelines.",
            "Use layered validation, anomaly signals, and safe fallback behavior.",
            "Avoid claiming universal robustness from a single defense.",
        ),
        (
            "Report attack success under explicit threat models.",
            "Test adaptive attacks and pipeline-level effects.",
            "Measure false positives and operational cost.",
            "Monitor distribution shifts and unusual input patterns.",
        ),
    ),
    DocumentSpec(
        "ml_security",
        "training_attacks",
        "ml_security_data_poisoning",
        "data_poisoning.md",
        "Training Data Poisoning",
        "data_poisoning",
        "https://csrc.nist.gov/pubs/ai/100/2/e2025/final",
        "Data poisoning manipulates training data, labels, sampling, or feedback to degrade performance or create attacker-chosen behavior.",
        (
            "Untrusted sources can write directly to training data.",
            "Labels and preprocessing outputs lack lineage.",
            "Feedback data is retrained automatically without review.",
            "Small targeted changes evade aggregate quality checks.",
        ),
        (
            "Track source, ownership, transformations, and approvals.",
            "Separate untrusted ingestion from trusted training sets.",
            "Apply integrity checks, anomaly review, and controlled promotion.",
            "Protect feedback loops and retraining triggers.",
        ),
        (
            "Reconstruct dataset lineage for each model version.",
            "Compare source and label distributions over time.",
            "Test removal and rollback of suspect data.",
            "Audit who approved data for training.",
        ),
    ),
    DocumentSpec(
        "ml_security",
        "training_attacks",
        "ml_security_backdoors",
        "backdoor_attacks.md",
        "Backdoor and Trojan Attacks in ML Models",
        "backdoor_attacks",
        "https://atlas.mitre.org/",
        "Backdoor attacks create hidden model behavior that activates when a trigger or condition appears while normal performance remains acceptable.",
        (
            "A pretrained checkpoint contains hidden attacker behavior.",
            "Validation data does not include trigger-like conditions.",
            "Fine-tuning preserves malicious features.",
            "Artifact changes are not traceable to a trusted build.",
        ),
        (
            "Use trusted provenance and controlled training pipelines.",
            "Compare model behavior across clean, stress, and trigger-oriented tests.",
            "Restrict external checkpoints and conversion tools.",
            "Support artifact quarantine, rollback, and replacement.",
        ),
        (
            "Verify model hashes, provenance, and build records.",
            "Run behavioral comparisons before promotion.",
            "Test suspicious features and activation patterns cautiously.",
            "Rebuild from trusted sources when provenance is uncertain.",
        ),
    ),
    DocumentSpec(
        "ml_security",
        "model_confidentiality",
        "ml_security_model_extraction",
        "model_extraction.md",
        "Model Extraction and Model Stealing",
        "model_extraction",
        "https://atlas.mitre.org/",
        "Model extraction uses queries, outputs, timing, or other observable behavior to approximate a target model or recover valuable properties.",
        (
            "Detailed probabilities expose more information than needed.",
            "Unlimited queries enable systematic probing.",
            "The API reveals model version, architecture, or internal errors.",
            "Suspicious query patterns are not detected.",
        ),
        (
            "Return only outputs required by the product.",
            "Apply identity, rate, cost, and concurrency controls.",
            "Detect systematic probing and distributed abuse.",
            "Protect model artifacts, telemetry, and administrative interfaces.",
        ),
        (
            "Review output granularity and metadata exposure.",
            "Simulate high-volume and adaptive probing.",
            "Correlate queries across identities and networks.",
            "Measure false positives in abuse detection.",
        ),
    ),
    DocumentSpec(
        "ml_security",
        "privacy",
        "ml_security_membership_inference",
        "membership_inference.md",
        "Membership Inference",
        "membership_inference",
        "https://csrc.nist.gov/pubs/ai/100/2/e2025/final",
        "Membership inference attempts to determine whether a specific record was included in a model's training data.",
        (
            "Overfitting creates distinguishable behavior for training records.",
            "Detailed confidence outputs reveal unnecessary information.",
            "Sensitive populations are represented in small groups.",
            "Privacy risk is assumed low because raw data is not returned.",
        ),
        (
            "Minimize sensitive training data and retention.",
            "Control output detail and query access.",
            "Evaluate privacy leakage under realistic attacker knowledge.",
            "Use privacy-preserving training methods when justified.",
        ),
        (
            "Measure attack performance against appropriate baselines.",
            "Compare train and non-train behavior.",
            "Test high-risk subgroups separately.",
            "Document privacy assumptions and residual risk.",
        ),
    ),
    DocumentSpec(
        "ml_security",
        "privacy",
        "ml_security_model_inversion",
        "model_inversion.md",
        "Model Inversion and Sensitive Attribute Recovery",
        "model_inversion",
        "https://csrc.nist.gov/pubs/ai/100/2/e2025/final",
        "Model inversion seeks to reconstruct representative inputs or sensitive attributes from model outputs, parameters, gradients, or embeddings.",
        (
            "Embeddings and gradients are treated as harmless intermediate data.",
            "Internal debugging endpoints expose detailed activations.",
            "Outputs permit repeated optimization against the model.",
            "Sensitive attributes can be inferred from correlated features.",
        ),
        (
            "Classify embeddings, gradients, and activations as sensitive where appropriate.",
            "Restrict internal endpoints and artifact access.",
            "Reduce unnecessary output detail.",
            "Evaluate privacy leakage before exposing representations.",
        ),
        (
            "Review every interface that exposes model internals.",
            "Test attribute and representation leakage.",
            "Monitor repeated optimization-like query behavior.",
            "Verify retention and deletion controls.",
        ),
    ),
    DocumentSpec(
        "ml_security",
        "data_governance",
        "ml_security_dataset_provenance",
        "dataset_provenance.md",
        "Dataset Provenance and Training-Data Integrity",
        "dataset_provenance",
        "https://www.nist.gov/itl/ai-risk-management-framework",
        "Dataset provenance records origin, ownership, collection conditions, transformations, labels, approvals, versions, and use restrictions.",
        (
            "Training data cannot be reproduced.",
            "Licensing, consent, or policy restrictions are unknown.",
            "Transformations overwrite original lineage.",
            "Dataset versions are referenced by mutable locations.",
        ),
        (
            "Assign immutable dataset versions and manifests.",
            "Record sources, transformations, label processes, and approvals.",
            "Validate integrity before training.",
            "Link each model version to exact datasets and code.",
        ),
        (
            "Rebuild a training set from recorded lineage.",
            "Verify manifests and checksums.",
            "Audit restricted or revoked sources.",
            "Test removal of specific records or sources.",
        ),
    ),
    DocumentSpec(
        "ml_security",
        "supply_chain",
        "ml_security_model_supply_chain",
        "model_supply_chain.md",
        "ML Model and Artifact Supply-Chain Security",
        "model_supply_chain",
        "https://atlas.mitre.org/",
        "The ML supply chain includes datasets, pretrained models, tokenizers, feature code, training frameworks, conversion tools, registries, and deployment artifacts.",
        (
            "Models are downloaded and executed without provenance.",
            "Serialization formats can trigger unsafe code paths.",
            "Conversion tools or plugins run with broad privileges.",
            "Registry access permits silent artifact replacement.",
        ),
        (
            "Use trusted sources, immutable versions, checksums, signatures, and provenance.",
            "Prefer safe serialization formats and controlled loaders.",
            "Sandbox conversion and inspection workflows.",
            "Protect registries with narrow publish and promotion permissions.",
        ),
        (
            "Verify artifacts before loading.",
            "Compare registry metadata with deployment hashes.",
            "Test artifact replacement and rollback controls.",
            "Audit publishers and promotion events.",
        ),
    ),
    DocumentSpec(
        "ml_security",
        "artifacts",
        "ml_security_checkpoint_safety",
        "checkpoint_safety.md",
        "Safe Model Checkpoints and Serialization",
        "checkpoint_security",
        "https://pytorch.org/docs/stable/notes/serialization.html",
        "Model checkpoints are untrusted inputs unless their provenance, format, and integrity are established.",
        (
            "Deserialization executes attacker-controlled code.",
            "Checkpoints include unnecessary optimizer or runtime state.",
            "Artifact hashes are not verified.",
            "Model loading occurs with network, filesystem, or cloud privileges.",
        ),
        (
            "Use safe formats and restricted loading modes where available.",
            "Store only necessary tensors and metadata.",
            "Verify hashes, signatures, and provenance before loading.",
            "Load untrusted artifacts in isolated, least-privileged environments.",
        ),
        (
            "Test loaders against malformed and unexpected artifacts.",
            "Inspect artifact contents before promotion.",
            "Confirm deployment uses approved hashes.",
            "Audit who may upload or replace checkpoints.",
        ),
    ),
    DocumentSpec(
        "ml_security",
        "evaluation",
        "ml_security_robust_evaluation",
        "robust_evaluation.md",
        "Robust and Security-Oriented ML Evaluation",
        "robust_ml_evaluation",
        "https://csrc.nist.gov/pubs/ai/100/2/e2025/final",
        "Security-oriented evaluation measures model and system behavior under explicit adversarial, privacy, integrity, availability, and misuse conditions.",
        (
            "One benchmark is treated as universal evidence.",
            "Attack parameters and assumptions are omitted.",
            "Clean accuracy hides security degradation.",
            "Evaluation code or data is contaminated by the training pipeline.",
        ),
        (
            "Publish threat models, assumptions, parameters, and limitations.",
            "Separate clean, robustness, privacy, and operational metrics.",
            "Use independent evaluation data and controlled tooling.",
            "Compare against baselines and adaptive attacks.",
        ),
        (
            "Make evaluation reproducible.",
            "Track model, dataset, code, and configuration versions.",
            "Review metric gaming and benchmark leakage.",
            "Retest after deployment or interface changes.",
        ),
    ),
    # ------------------------------------------------------------------
    # AI / LLM / RAG security
    # ------------------------------------------------------------------
    DocumentSpec(
        "ai_security",
        "prompt_security",
        "ai_security_prompt_injection",
        "prompt_injection.md",
        "Prompt Injection in LLM Applications",
        "prompt_injection",
        "https://genai.owasp.org/llmrisk/llm01-prompt-injection/",
        "Prompt injection occurs when untrusted instructions influence model behavior in ways that conflict with the application's intended policy.",
        (
            "User content is combined with trusted instructions without clear boundaries.",
            "The model is allowed to authorize actions by itself.",
            "Retrieved documents can override system behavior.",
            "Output validation assumes the model followed instructions.",
        ),
        (
            "Treat every external string as untrusted data.",
            "Keep authorization and policy enforcement outside the model.",
            "Restrict tools, data access, and side effects by explicit identity and scope.",
            "Validate model outputs before downstream use.",
        ),
        (
            "Test direct, indirect, encoded, multilingual, and multi-turn injection.",
            "Verify unauthorized tool and data requests are blocked independently of model behavior.",
            "Audit tool calls and policy decisions.",
            "Measure false positives and business impact of mitigations.",
        ),
    ),
    DocumentSpec(
        "ai_security",
        "prompt_security",
        "ai_security_indirect_prompt_injection",
        "indirect_prompt_injection.md",
        "Indirect Prompt Injection through Retrieved Content",
        "indirect_prompt_injection",
        "https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html",
        "Indirect prompt injection places malicious instructions in documents, web pages, emails, code, images, or tool results that an LLM later processes.",
        (
            "RAG content is treated as trusted because it came from an indexed source.",
            "Documents can instruct the model to reveal secrets or call tools.",
            "Source trust and content trust are conflated.",
            "Citations create false confidence in malicious content.",
        ),
        (
            "Label retrieved content as untrusted evidence, not instructions.",
            "Separate data channels and control channels where possible.",
            "Apply source governance, content scanning, and retrieval policy.",
            "Require external authorization for sensitive actions.",
        ),
        (
            "Seed controlled malicious instructions into test documents.",
            "Test whether retrieved text can change tool permissions.",
            "Record which sources influenced actions.",
            "Quarantine and remove poisoned content quickly.",
        ),
    ),
    DocumentSpec(
        "ai_security",
        "rag_security",
        "ai_security_rag_poisoning",
        "rag_poisoning.md",
        "RAG Knowledge-Base and Retrieval Poisoning",
        "rag_poisoning",
        "https://atlas.mitre.org/",
        "RAG poisoning manipulates indexed content, metadata, embeddings, ranking signals, or ingestion paths to influence retrieved context and generated answers.",
        (
            "Any uploader can write to the production knowledge base.",
            "Source identifiers and provenance are mutable or missing.",
            "Embedding and metadata changes are not audited.",
            "Evaluation does not include malicious or conflicting documents.",
        ),
        (
            "Separate ingestion, review, publication, and deletion permissions.",
            "Store immutable source identifiers, versions, hashes, and provenance.",
            "Validate metadata and content before indexing.",
            "Monitor retrieval shifts and unusual source dominance.",
        ),
        (
            "Trace answers back to exact source versions and chunks.",
            "Test poisoned, duplicated, conflicting, and adversarial documents.",
            "Audit index mutations and rebuilds.",
            "Support source quarantine and deterministic reindexing.",
        ),
    ),
    DocumentSpec(
        "ai_security",
        "output_security",
        "ai_security_insecure_output_handling",
        "insecure_output_handling.md",
        "Secure Handling of LLM Outputs",
        "insecure_output_handling",
        "https://genai.owasp.org/",
        "LLM output is untrusted data and must not be executed, rendered, queried, or forwarded to privileged systems without validation.",
        (
            "Generated text is executed as shell, Python, SQL, or template code.",
            "Generated HTML or Markdown reaches unsafe rendering contexts.",
            "Tool arguments are accepted without schema and policy validation.",
            "Model confidence is mistaken for correctness or authorization.",
        ),
        (
            "Use strict schemas and typed validation.",
            "Escape or sanitize output for its destination context.",
            "Never execute generated code in privileged environments.",
            "Apply allowlists, policy checks, and human approval for sensitive effects.",
        ),
        (
            "Fuzz generated outputs and tool arguments.",
            "Test code, template, query, path, and URL injection boundaries.",
            "Verify failures are safe and observable.",
            "Audit every privileged side effect.",
        ),
    ),
    DocumentSpec(
        "ai_security",
        "privacy",
        "ai_security_sensitive_information",
        "sensitive_information_disclosure.md",
        "Sensitive Information Disclosure in AI Systems",
        "sensitive_information_disclosure",
        "https://genai.owasp.org/",
        "AI systems can disclose sensitive information from prompts, retrieved context, memory, logs, model outputs, tools, or training data.",
        (
            "Secrets enter prompts or retrieved documents.",
            "Cross-session or cross-tenant memory is insufficiently isolated.",
            "Debug traces store full prompts and outputs.",
            "The model can query data beyond the user's authorization.",
        ),
        (
            "Minimize sensitive context and apply data classification.",
            "Authorize retrieval and tools using the user's identity and resource policy.",
            "Isolate tenants, sessions, and memory stores.",
            "Redact logs, traces, examples, and support captures.",
        ),
        (
            "Test cross-tenant and cross-session access.",
            "Search telemetry and indexes for secrets.",
            "Review retrieval authorization independently of generation.",
            "Verify deletion and retention behavior.",
        ),
    ),
    DocumentSpec(
        "ai_security",
        "agents",
        "ai_security_excessive_agency",
        "excessive_agency.md",
        "Excessive Agency in AI Agents",
        "excessive_agency",
        "https://genai.owasp.org/",
        "Excessive agency occurs when an AI system has more functionality, permissions, autonomy, or persistence than required for its task.",
        (
            "The model can select and execute high-impact tools without approval.",
            "Agent credentials have broad access across systems.",
            "Long-running tasks continue after context changes.",
            "The system cannot reconstruct why an action occurred.",
        ),
        (
            "Minimize available tools, permissions, duration, and side effects.",
            "Require deterministic authorization outside the model.",
            "Use approval gates for irreversible or high-impact actions.",
            "Record plans, tool calls, arguments, policy decisions, and outcomes.",
        ),
        (
            "Test unauthorized, ambiguous, and adversarial action requests.",
            "Verify cancellation and revocation.",
            "Review effective tool permissions.",
            "Reconstruct actions from audit evidence.",
        ),
    ),
    DocumentSpec(
        "ai_security",
        "tools",
        "ai_security_secure_tool_use",
        "secure_tool_use.md",
        "Secure Tool Use for LLMs and Agents",
        "secure_tool_use",
        "https://genai.owasp.org/",
        "Secure tool use separates natural-language reasoning from typed, authorized, bounded, and observable system actions.",
        (
            "Free-form model output becomes tool arguments.",
            "Tools inherit broad network, filesystem, database, or cloud permissions.",
            "Tool results contain untrusted instructions.",
            "Retries duplicate irreversible actions.",
        ),
        (
            "Use strict schemas, allowlists, and semantic validation.",
            "Bind tools to narrow workload identities and resource scopes.",
            "Treat tool outputs as untrusted data.",
            "Use idempotency, deadlines, and explicit confirmation for side effects.",
        ),
        (
            "Test malformed and policy-violating arguments.",
            "Verify least-privilege tool credentials.",
            "Exercise retries, partial failure, and cancellation.",
            "Audit tool selection, authorization, input, and result.",
        ),
    ),
    DocumentSpec(
        "ai_security",
        "agents",
        "ai_security_agent_authorization",
        "agent_authorization.md",
        "Authorization Architecture for AI Agents",
        "agent_authorization",
        "https://csrc.nist.gov/projects/zero-trust-architecture",
        "Agent authorization must be enforced by deterministic policy using authenticated identities, resource context, action scope, and current risk state.",
        (
            "The LLM decides whether an action is authorized.",
            "User identity is lost between chat, agent, and tool layers.",
            "Delegated credentials exceed the user's authority.",
            "Policy is evaluated only at session start.",
        ),
        (
            "Propagate authenticated user and workload identity end to end.",
            "Authorize each action at the tool or resource boundary.",
            "Use constrained delegation and short-lived credentials.",
            "Reevaluate policy for sensitive and changing operations.",
        ),
        (
            "Test privilege escalation and confused-deputy scenarios.",
            "Compare user authority with agent and tool authority.",
            "Audit policy decisions and delegation chains.",
            "Verify revocation takes effect promptly.",
        ),
    ),
    DocumentSpec(
        "ai_security",
        "memory",
        "ai_security_memory_poisoning",
        "memory_poisoning.md",
        "Agent Memory Poisoning and Cross-Session Integrity",
        "memory_poisoning",
        "https://atlas.mitre.org/",
        "Memory poisoning inserts false, malicious, or unauthorized information into short-term or long-term agent memory so that future behavior is influenced.",
        (
            "Untrusted statements are stored as durable facts.",
            "Memory from one user or tenant affects another.",
            "The source and confidence of memories are lost.",
            "Deletion and correction are unavailable.",
        ),
        (
            "Separate observations, user claims, verified facts, and policy state.",
            "Attach provenance, owner, timestamp, scope, and confidence.",
            "Require validation before promoting durable memory.",
            "Support correction, expiration, quarantine, and deletion.",
        ),
        (
            "Test cross-session and cross-tenant contamination.",
            "Trace decisions to memory records.",
            "Inject conflicting facts and verify resolution policy.",
            "Audit memory creation and modification.",
        ),
    ),
    DocumentSpec(
        "ai_security",
        "availability",
        "ai_security_model_dos",
        "model_denial_of_service.md",
        "Model Denial of Service and Resource Exhaustion",
        "model_denial_of_service",
        "https://genai.owasp.org/",
        "AI denial of service targets token budgets, context windows, retrieval, tools, concurrency, accelerators, memory, storage, or downstream costs.",
        (
            "Requests have no token, time, recursion, or tool-call limits.",
            "Large documents trigger unbounded ingestion or retrieval work.",
            "Retries amplify overload.",
            "A single tenant consumes shared model capacity.",
        ),
        (
            "Enforce input, output, context, retrieval, tool, time, and cost budgets.",
            "Apply rate, concurrency, queue, and tenant limits.",
            "Use deadlines, cancellation, backpressure, and bounded retries.",
            "Degrade safely and protect critical capacity.",
        ),
        (
            "Load-test worst-case request shapes.",
            "Exercise cancellation and dependency failure.",
            "Monitor queue depth, accelerator utilization, token use, latency, and cost.",
            "Verify tenant isolation and overload behavior.",
        ),
    ),
    DocumentSpec(
        "ai_security",
        "supply_chain",
        "ai_security_supply_chain",
        "ai_supply_chain.md",
        "AI and LLM Supply-Chain Security",
        "ai_supply_chain",
        "https://genai.owasp.org/",
        "The AI supply chain includes models, datasets, embeddings, tokenizers, adapters, runtimes, plugins, tools, prompt templates, and external services.",
        (
            "Models or adapters are loaded from mutable or untrusted locations.",
            "Prompt templates and policies change without review.",
            "External AI services receive sensitive context unexpectedly.",
            "Plugins and tools expand privileges silently.",
        ),
        (
            "Maintain inventories, provenance, versions, hashes, and approvals.",
            "Pin and verify models, adapters, runtimes, and prompts.",
            "Review data flows to external services.",
            "Restrict plugin and tool installation and permissions.",
        ),
        (
            "Reproduce deployed configurations from versioned artifacts.",
            "Verify hashes and signatures before loading.",
            "Audit external-service and plugin changes.",
            "Exercise supplier compromise and rollback procedures.",
        ),
    ),
    DocumentSpec(
        "ai_security",
        "observability",
        "ai_security_observability",
        "security_observability.md",
        "Security Observability for RAG and AI Agents",
        "ai_security_observability",
        "https://opentelemetry.io/docs/concepts/signals/traces/",
        "Security observability links identity, input, retrieval, policy, model, tool, output, and side-effect events without exposing sensitive content.",
        (
            "Logs omit the source and policy behind an action.",
            "Full prompts and retrieved documents leak sensitive data.",
            "Tool calls cannot be correlated with user requests.",
            "Telemetry can be altered or deleted by the workload.",
        ),
        (
            "Trace request, identity, retrieval, reranking, generation, policy, tool, and response stages.",
            "Record bounded metadata, source IDs, model versions, and policy decisions.",
            "Redact or hash sensitive fields.",
            "Protect telemetry integrity, retention, and access.",
        ),
        (
            "Reconstruct representative incidents from telemetry.",
            "Test redaction and tenant isolation.",
            "Alert on unusual source dominance, tool use, policy denials, and cost.",
            "Verify clocks, retention, and export reliability.",
        ),
    ),
)


def _render(spec: DocumentSpec) -> str:
    risks = "\n".join(f"- {item}" for item in spec.risks)
    controls = "\n".join(f"- {item}" for item in spec.controls)
    verification = "\n".join(f"- {item}" for item in spec.verification)

    return f"""---
source_id: {spec.source_id}
title: "{spec.title}"
domain: {spec.domain}
topic: {spec.topic}
url: "{spec.url}"
license: reference-only
language: en
source_type: official_documentation_summary
---

# {spec.title}

## Definition

{spec.definition}

This document is defensive engineering guidance. It is intended for secure
design, hardening, governance, detection, evaluation, incident response, and
risk reduction. It does not authorize testing against systems without explicit
permission.

## Security objectives

A mature implementation should preserve confidentiality, integrity,
availability, authenticity, accountability, and recoverability while keeping
operational behavior observable and testable.

The control design should answer:

- what asset or decision is protected;
- which identity or component is trusted;
- where trust changes;
- which failure or abuse case is prevented;
- which signal detects control failure;
- how the system contains and recovers from failure.

## Common risks

{risks}

## Engineering controls

{controls}

## Architecture guidance

Keep policy enforcement outside probabilistic components whenever a
deterministic decision is required. Treat network input, files, model output,
retrieved text, serialized artifacts, tool results, and external metadata as
untrusted until validated.

Use narrow interfaces and explicit trust boundaries. Separate ingestion,
review, publication, execution, administration, and incident-response
permissions. Prefer immutable versions, reproducible builds, bounded resource
usage, safe defaults, and fail-closed behavior for sensitive operations.

Security controls should remain effective during timeout, retry, cancellation,
partial failure, degraded dependencies, rollback, and recovery. A control that
works only on the happy path is incomplete.

## Verification

{verification}

## Operational telemetry

Record bounded and redacted evidence for:

- authenticated user and workload identity;
- action, resource, and authorization result;
- source, artifact, model, dataset, or policy version;
- validation failures and denied operations;
- latency, timeout, retry, queue, rate, and resource state;
- control changes, deployment events, and administrative access.

Do not place secrets, raw credentials, unrestricted prompts, sensitive
documents, or private model inputs in logs. Protect audit data as a
security-sensitive asset.

## Incident readiness

Define ownership, severity, escalation, containment, evidence preservation,
credential rotation, rollback, recovery validation, and lessons-learned
procedures. Preserve enough provenance to identify which data, model, source,
policy, identity, and deployment version contributed to an incident.

## Engineering checklist

- Threat model and trust boundaries are documented.
- Least privilege is enforced for users, services, pipelines, and tools.
- Inputs and outputs are validated at system boundaries.
- Versions and provenance are immutable and reviewable.
- Abuse cases and negative authorization paths are tested.
- Telemetry supports detection and investigation without leaking secrets.
- Rollback, revocation, quarantine, and recovery are tested.
- Residual risks and limitations are stated explicitly.
"""


def write_documents(*, force: bool) -> tuple[int, int]:
    created = 0
    skipped = 0

    for spec in SPECS:
        target = RAW_DATA_DIR / spec.domain / spec.category / spec.filename
        target.parent.mkdir(parents=True, exist_ok=True)

        if target.exists() and not force:
            skipped += 1
            continue

        target.write_text(_render(spec), encoding="utf-8")
        created += 1

    return created, skipped


def audit() -> None:
    expected_domains = {
        "cybersecurity",
        "linux_security",
        "ml_security",
        "ai_security",
    }

    source_ids: set[str] = set()
    domain_counts: dict[str, int] = {}

    for spec in SPECS:
        if spec.domain not in expected_domains:
            raise ValueError(f"Unsupported generated domain: {spec.domain}")

        if spec.source_id in source_ids:
            raise ValueError(f"Duplicate source_id: {spec.source_id}")

        source_ids.add(spec.source_id)
        domain_counts[spec.domain] = domain_counts.get(spec.domain, 0) + 1

        target = RAW_DATA_DIR / spec.domain / spec.category / spec.filename
        if not target.exists():
            raise FileNotFoundError(target)

        content = target.read_text(encoding="utf-8")
        required = (
            f"source_id: {spec.source_id}",
            f"domain: {spec.domain}",
            f"topic: {spec.topic}",
            "source_type: official_documentation_summary",
            "## Definition",
            "## Common risks",
            "## Engineering controls",
            "## Verification",
        )
        for marker in required:
            if marker not in content:
                raise ValueError(f"{target}: missing marker {marker!r}")

    print("Cybersecurity corpus audit passed.")
    print(f"Documents: {len(SPECS)}")
    for domain, count in sorted(domain_counts.items()):
        print(f"  {domain}: {count}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a defensive cybersecurity corpus for the local RAG."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing generated files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    created, skipped = write_documents(force=args.force)
    audit()
    print(f"Created: {created}")
    print(f"Skipped: {skipped}")


if __name__ == "__main__":
    main()
