# **Development Constraints and Architectural Rules**

These constraints establish the required architecture, data models, and logic flow for the Progressive Overload Log (P.O. Log) application.

## **I. Strict Three-Module Architecture**

All code must adhere to the **strict separation** of the three core services defined in the PRD:

* **Plan Management & Ingestion Service (P-MIS):** Only manages the user's **scheduled plan**.  
* **Logbook & Data Persistence Service (L-DPS):** The **immutable source of truth** for all historical performance data.  
* **Workout Session & Reference Engine (S-RE):** The **presentation layer**; it owns no permanent data and acts as an orchestrator, directing read/write operations.

Services must be independent and should ideally communicate via well-defined API endpoints.

## **II. Adherence to Data Schemas**

The data models defined in the PRD are **final**. Do not add or remove fields without explicit instruction.

### **P-MIS Plan Schema**

* Plan ID  
* User ID  
* Day  
* Target Body Parts  
* List of Planned Exercises

### **L-DPS Log Entry Schema**

* Log Entry ID  
* User ID  
* Exercise Name  
* Timestamp  
* Set Number  
* Weight Used  
* Reps Completed  
* *Other measurable insights (Duration/Distance/RPE are optional but supported).*

## **III. Immutable Logbook Principle**

The L-DPS must be treated as an **append-only ledger**. A logged set, once saved, should not be editable. To correct a mistake, a user would need to delete and re-log the entry. This ensures data integrity.

## **IV. Reference Retrieval Logic is Specific (F.5.0)**

The query for the "Progressive Overload Reference" is critical and must be implemented precisely as described:

1. When a user starts an exercise, the S-RE must query the L-DPS for the Exercise Name.  
2. The query must find the **single most recent session** where that exercise was performed. A "session" is defined by a cluster of logs with close timestamps for that user.  
3. The query must return **all sets** (e.g., Set 1, Set 2, Set 3, etc.) from that single past session. The query should not just fetch the single heaviest set or the last set.

## **V. Data Flow is Unidirectional**

The flow of data between the services must strictly follow these rules:

* The **S-RE** reads from **P-MIS** to generate the daily to-do list.  
* The **S-RE** reads from **L-DPS** to get historical reference data.  
* The **S-RE** writes new log entries to the **L-DPS** after each set is performed.  
* **Under no circumstances** should the S-RE write data back to the P-MIS. The plan is separate from the performance log.

## **VI. Technology Stack Assumption**

Unless specified otherwise, assume a modern web stack:

* **Frontend (S-RE):** A component-based JavaScript framework (e.g., React, Vue, Svelte).  
* **Backend (P-MIS, L-DPS):** A service-oriented backend (e.g., Node.js with Express, Python with FastAPI).  
* **Database (for L-DPS):** A database that handles high-frequency writes and timestamp-based queries well (e.g., PostgreSQL, MongoDB).

\# Additional Project Rules

| \#  | Rule                              | Description / Example                                                           |  
|----|-----------------------------------|---------------------------------------------------------------------------------|  
| 1  | OOP Structure                     | All code must use object-oriented best practices; classes for entities, encapsulation. |  
| 2  | Modular Design                    | Each core component/service in a separate module/package; expose via APIs.      |  
| 3  | AI Workflow Constraints           | AI code suggestions limited by user-specified scope; multi-module changes summarized & require approval. |  
| 4  | Acceptance Criteria Adherence     | Code changes must fulfill PRD requirements; referenced in comments/commits.     |  
| 5  | Security & Privacy                | Sensitive data encrypted in storage/transfer; no PII in logs.                   |  
| 6  | Access Control & Permissions      | Role-based access for critical operations; only admins set project rules.        |  
| 7  | Audit Logging & Transparency      | Maintain immutable logs of CRUD/code changes and AI actions.                    |  
| 8  | Environment & Dependency Management| All dependencies declared and pinned per environment; separate dev/staging/prod. |  
| 9  | Code Quality & Review             | All changes require lint/test checks & peer/AI review.                          |  
| 10 | Error Handling & Input Validation | Sanitize inputs, catch exceptions, never show sensitive info in errors.         |  
| 11 | Testing & Continuous Integration  | All modules unit/integration tested; code merges blocked unless all checks pass.|  
| 12 | Documentation                     | All modules/classes/functions must be documented.                               |  
| 13 | Prompt & Action Clarity           | All prompts must summarize intent, actions, and seek approval as needed.        |  
| 14 | Internationalization & Accessibility| Localize user-facing strings; ensure accessibility.                           |

