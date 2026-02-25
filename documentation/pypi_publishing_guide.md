# Publishing `cutlass` to PyPI

**Objective**: A step-by-step guide to publishing your local `cutlass` package to the Python Package Index (PyPI), making it installable by anyone via `pip install cutlass`.

## 1. Prerequisites and Setup

Before pushing to the public index, we need to ensure your package metadata is correct and you have the right accounts.

### 1.1 Update `pyproject.toml`
Your `c:\Users\jason\ODU\cutlass\pyproject.toml` is already in fantastic shape, using the modern `[project]` standards. However, you should update a few placeholder fields before publishing:

1.  **Version**: It's currently `"0.1.0"`. This is perfect for a first release.
2.  **Authors**: Update `[{name = "CUTLASS Contributors"}]` to include your actual name and email, e.g., `[{name = "Your Name", email = "your.email@odu.edu"}]`.
3.  **URLs**: Update the placeholder URLs at the bottom:
    ```toml
    [project.urls]
    Homepage = "https://github.com/yourusername/cutlass"
    Repository = "https://github.com/yourusername/cutlass"
    ```
 *(Note: If you haven't pushed `cutlass` to a public GitHub repo yet, you should do that first!)*

### 1.2 Create a PyPI Account
1.  Go to [pypi.org](https://pypi.org/) and create an account.
2.  Enable Two-Factor Authentication (2FA) on your account (PyPI requires this for all uploaders).
3.  Go to your PyPI Account Settings -> **API tokens** and click "Add API token".
4.  Name the token (e.g., "Cutlass Upload") and set the Scope to "Entire account" (since you haven't published the package yet).
5.  **Copy the token immediately!** (It starts with `pypi-`). You will need this later, and PyPI will never show it to you again.

---

## 2. Build the Distribution Files

Python packages are distributed in two formats: a source archive (`.tar.gz`) and a built distribution wheel (`.whl`). Your `pyproject.toml` requires the `build` package to create these.

Open your specific terminal (e.g., Anaconda Prompt or PowerShell) and navigate to the `cutlass` directory:

```bash
cd c:\Users\jason\ODU\cutlass
```

Upgrade the builder to the latest version and run the build command:
```bash
python -m pip install --upgrade build setuptools wheel
python -m build
```

This will create a new folder called `dist/` containing two files:
*   `cutlass-0.1.0.tar.gz` (Source Archive)
*   `cutlass-0.1.0-py3-none-any.whl` (Built Wheel)

---

## 3. Upload to TestPyPI (Optional but Highly Recommended)

Before permanently publishing to the real PyPI index, it is best practice to publish to **TestPyPI**. This ensures your package builds correctly and renders its README properly on the web.

1.  Create a separate account on [test.pypi.org](https://test.pypi.org/) (Accounts are not shared between TestPyPI and real PyPI).
2.  Generate an API token on TestPyPI just like you did above.
3.  Install `twine`, the official PyPI upload tool:
    ```bash
    python -m pip install --upgrade twine
    ```
4.  Upload the `dist/` folder to TestPyPI:
    ```bash
    python -m twine upload --repository testpypi dist/*
    ```
    *   **Username**: Enter `__token__` (literally type underscore-underscore-token-underscore-underscore).
    *   **Password**: Paste your TestPyPI API token (the one starting with `pypi-`).

If successful, check the provided URL. If it looks good, you're ready for the real deal.

---

## 4. Publish to the Real PyPI

This is the final step. Once published here, it is permanent (you can delete it, but you can never reuse the exact `0.1.0` version number again).

Run twine against the real PyPI server:
```bash
python -m twine upload dist/*
```
*   **Username**: Enter `__token__`.
*   **Password**: Paste your *real* PyPI API token.

🎉 **Congratulations!** Your package is now live. Anyone in the world can now run:
```bash
pip install cutlass
```

### 4.1 Releasing Future Versions
When you make changes to your codebase and want to publish an update:
1.  Open `pyproject.toml` and increment the version (e.g., from `"0.1.0"` to `"0.1.1"`).
2.  Delete the old files in your `dist/` folder.
3.  Run `python -m build`
4.  Run `python -m twine upload dist/*`

---
## Final Checklist Before Building
*   Ensure all temporary/experimental scratch files (like old `case_1_...` scripts) are moved out of the folder or ignored.
*   Double check that your virtual environment is active before running the `build` command so that dependencies gather correctly.
