# Contributing to SecureData Layer

First off, thank you for considering contributing to SecureData Layer! It's people like you that make this tool such a great standard for secure IoT data exchange.

## 🤝 Code of Conduct
By participating in this project, you agree to abide by our Code of Conduct. We expect all contributors to treat others with respect and professional courtesy.

## 🛠️ Development Workflow

1.  **Fork & Clone**: Fork the repo and clone it locally.
2.  **Environment Setup**:
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
3.  **Branching Strategy**:
    -   `main`: Stable, production-ready code.
    -   `develop`: Integration branch for next release.
    -   `feature/foo-bar`: Your feature branch.
4.  **Testing**:
    -   Run the simulation runner: `python -m src.simulation_runner`
    -   Ensure all tests pass: `pytest`

## 📝 Style Guidelines

-   **Python**: We follow [PEP 8](https://peps.python.org/pep-0008/).
-   **Type Hinting**: All public interfaces must be fully type-hinted.
-   **Documentation**: Update `docs/` if you change architecture or APIs.

## 🔒 Reporting Security Issues
**Do not create public GitHub issues for security vulnerabilities.**
Please email `security@securedata.io` with details. We will respond within 48 hours.

## 📬 Commit Messages
We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:
-   `feat: add CP-ABE engine`
-   `fix: resolve replay attack vulnerability`
-   `docs: update architecture diagram`

Happy Coding!
The SecureData Team
