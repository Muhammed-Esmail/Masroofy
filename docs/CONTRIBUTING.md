# Contributing to Masroofy

To maintain code quality and ensure the stability of our budget engine, all contributors must follow this workflow.

## 1. Branching Strategy

We use a two-tier branching model to separate stable baselines from active development:

* **`main` Branch**: 
    * Contains only fully tested, production-ready code.
    * Represents the working baseline for the **previous milestone**.
    * Direct commits are prohibited.
* **`dev` Branch**: 
    * The primary integration branch for new features and bug fixes.
    * Features here may be in-progress or partially tested, but should not break the build.
* **Feature Branches**: 
    * Created for specific tasks (e.g., implementing a new UI component or budget logic).
    * Always branched off `dev`.

## 2. Naming Conventions

Consistent naming helps us track requirements (FR/NFR) directly in our Git history.

### Branch Naming
Format: `type/req-id-short-description`
* **Features**: `feat/fr-01-initial-setup`
* **Bug Fixes**: `fix/logic-error-daily-limit`
* **Refactors**: `refactor/optimize-sqlite-queries`
* **Testing**: `test/add-rollover-unit-tests`

### Pull Request (PR) Titles
Format: `[Req-ID] Brief description of changes`
* *Example*: `[FR-02] Implement rapid-entry 3-tap interface`
* *Example*: `[NFR-04] Secure local PIN hashing implementation`

## 3. Pull Request Workflow

Every merge into `dev` or `main` requires a formal Pull Request.

1.  **Preparation**: Ensure your code passes all local unit tests (especially math logic for the budget engine).
2.  **Submission**: Open a PR from your feature branch into `dev`.
3.  **Review**: At least **one approval** from another developer is required to merge.
4.  **Verification**: The reviewer must verify:
    * Code aligns with the specific Functional Requirement (FR).
    * The change does not violate Non-Functional Requirements (e.g., performance or offline availability).
5.  **Merging to Main**: Merges from `dev` to `main` occur only when a milestone is 100% complete and verified.

## 4. Branch Protection Rules (Admin Setup)

The `main` branch is protected with the following GitHub settings:
* **Require a pull request before merging**: Enabled.
* **Required number of approvals**: 1.
* **Bypass Permissions**: Repository administrators may bypass these requirements for emergency hotfixes or final milestone baselining, but should still utilize PRs for transparency.

## 5. Definition of Done
A task is considered "Done" when:
* Code is merged into `dev`.
* Associated Unit Tests are passing.
* Documentation is updated to reflect progress and changes.