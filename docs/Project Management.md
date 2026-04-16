# Project Management: Masroofy Requirements Tracker

## 1. Functional Requirements (FR)
These requirements define the specific features and behaviors the application must provide.

| ID | Feature | Description | Status |
| :--- | :--- | :--- | :--- |
| **FR-01** | Allowance Initialization | Users can set a total allowance and define specific start/end dates for the budget cycle. | [ ] |
| **FR-02** | Transaction Management | A rapid-entry interface to log expenses with amount, category, and date. | [ ] |
| **FR-03** | Dynamic Daily Limit | System automatically recalculates the "Safe Daily Limit" based on remaining funds and days. | [ ] |
| **FR-04** | Spending Insights | Visual dashboards (charts/graphs) showing spending habits and categorical distributions. | [ ] |
| **FR-05** | History & CRUD | View a chronological log of all transactions with the ability to edit or delete entries. | [ ] |
| **FR-06** | Security Lock | Local authentication layer (PIN or Biometrics) to protect sensitive financial data. | [ ] |
| **FR-07** | Threshold Alerts | Local notifications triggered when spending reaches a defined percentage of the total budget. | [ ] |

---

## 2. Non-Functional Requirements (NFR)
These requirements define the quality attributes, constraints, and performance standards.

| ID | Category | Description | Status |
| :--- | :--- | :--- | :--- |
| **NFR-01** | Usability | The app must be intuitive. A core transaction should be completed in 3 taps or less. | [ ] |
| **NFR-02** | Performance | The application must launch and be ready for input in under 2 seconds. | [ ] |
| **NFR-03** | Reliability | Data must be saved to local storage immediately upon entry to prevent loss during crashes. | [ ] |
| **NFR-04** | Privacy | All data remains strictly on the user's device. No data is uploaded to external servers. | [ ] |
| **NFR-05** | Availability | The application must be 100% functional without an active internet connection. | [ ] |
| **NFR-06** | Portability | The UI must be responsive across various Android screen sizes (API level 24 and above). | [ ] |
| **NFR-07** | Scalability | Local database must handle long-term transaction history without performance degradation. | [ ] |

---

## 3. Requirement Traceability Matrix (Testing)
Use this section to confirm that each requirement has been verified through testing.

| Req ID | Test Case Description | Verified |
| :--- | :--- | :--- |
| **FR-03** | Verify daily limit updates correctly after a transaction is logged. | [ ] |
| **NFR-02** | Cold start timer check (must be < 2s). | [ ] |
| **NFR-04** | Audit network logs to ensure zero data transmission. | [ ] |
| **NFR-05** | Test all core features in Airplane Mode. | [ ] |