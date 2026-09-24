# Architecture decisions

The dividing line: a choice that touches the data's shape, the system's trust or consistency boundaries, or the hardware or platform target is expensive to reverse and is decided before the first story. A choice swappable behind an interface, or affecting one vertical story, waits until the story that needs it.

Walk only the groups that match the system. An item the code already settles (an existing database, an existing auth scheme) is stated in the feature header, never asked.

## Before the first story

**Any system**

* Monolith or services, and the service boundaries.
* Primary data store type and engine (SQL or NoSQL, which vendor); schema and query shapes follow from it.
* Primary key scheme (UUID, sequential, composite); touches every table and foreign reference.
* Sharding or partitioning key for data at scale.
* Consistency model (strong or eventual) for core transactional data.
* Synchronous request-response or event-driven backbone between components.
* Public API contract style (REST, GraphQL, gRPC).
* Multi-tenancy model (shared database, schema per tenant, database per tenant).
* Authentication and identity architecture (session or token, SSO, multi-region).
* Encryption at rest and key management.
* Cloud provider or on-premises, and the core infrastructure primitives.
* Data residency and compliance boundaries for regulated data.
* Core language and runtime per component.

**Mobile**

* Native or cross-platform framework.
* Minimum supported OS version.
* Offline-first or online-only, and the local persistence engine.
* App-wide navigation and state-management architecture.
* Module boundaries for a large app; they set build times permanently.

**Games**

* Engine (Unity, Unreal, custom).
* Core architecture pattern (ECS or object-oriented).
* Multiplayer networking model (authoritative server or peer-to-peer; lockstep or rollback).
* Save-game serialization format that must stay backward compatible.
* Rendering pipeline (forward or deferred).
* Target platform set; memory, controller and performance budgets follow from it.

**Firmware and embedded**

* MCU or SoC (memory, peripherals, power envelope).
* RTOS, bare metal, or embedded Linux.
* Flash and RAM memory map and partitioning.
* Bootloader and over-the-air update architecture.
* Bus and protocol (I2C, SPI, CAN, UART); baked into the PCB.
* Interrupt priority and real-time scheduling model.

**Data and ML**

* Core event or data schema for the warehouse or lake.
* Batch or streaming processing.
* Training-serving and feature-store architecture.

## When a story forces it

**Any system**

* Caching layer; add when a measured bottleneck appears.
* Message queue implementation, when behind an interface.
* Logging and observability vendor, when instrumentation is standard.
* CI/CD tooling specifics.
* Search engine.
* Feature flag system.
* A/B testing framework.
* ORM or query builder, when data access is behind an interface.
* Extracting a service from the monolith.
* Rate-limiting implementation.
* Admin and internal dashboard tooling.
* Retry and backoff policies on non-critical paths.
* Internal folder structure and code organisation.

**Mobile**

* UI component or styling library.
* Analytics SDK vendor.
* Animation and transition polish.
* Push notification provider, when behind an interface.

**Games**

* Enemy AI tuning and balancing.
* Cosmetic asset pipeline and tooling.
* Audio middleware.
* Level-streaming optimisation.

**Firmware and embedded**

* Sensor calibration algorithms.
* Compression or serialization codec for telemetry.
* Power-management tuning beyond the basic budget.
* Diagnostic and logging format over the debug interface.

**Data and ML**

* Recommendation or ranking model tuning.
* Secondary and derived metrics schema.
* Visualisation or BI tool.
* Model retraining cadence and automation.

**Product surface**

* Internationalisation string tooling; design for it early, translate later.
* Accessibility polish beyond the design intent.
* Payment provider integration, when behind a payments interface.
