# Playwright Course — Test Suite & CI Pipeline

Playwright + pytest end-to-end tests against `rahulshettyacademy.com`, with a
Docker image and a Jenkins pipeline for running them in CI.

## Layout

```
playwright_course/
  config.py            # Credential lookup (env vars -> credentials.json fallback)
  conftest.py
  page_objects/        # Page Object Model classes
  utils/api_base.py    # API helpers (order create/delete, token)
  data/credentials.json# Fallback credentials for local runs
  test_*.py            # Tests
Dockerfile             # Playwright image + deps, runs the suite
Jenkinsfile            # Declarative CI pipeline
requirements.txt
.env.example           # Template for local credentials
```

## Running locally

```bash
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt   # Linux/mac: .venv/bin/pip
playwright install --with-deps                   # browsers

pytest playwright_course -v
```

Reports (optional):

```bash
pytest playwright_course --junitxml=results.xml --html=report.html --self-contained-html -v
```

## Credentials

Credentials come from environment variables, loaded from a local `.env` file if
present (via `python-dotenv`) or injected by CI. If the env vars are unset, the
suite falls back to `playwright_course/data/credentials.json`, so local runs work
with no setup.

| Env var                            | Used by                                |
| ---------------------------------- | -------------------------------------- |
| `API_USER_EMAIL` / `API_USER_PASSWORD` | API login in `utils/api_base.py`   |
| `UI_USER_EMAIL` / `UI_USER_PASSWORD`   | Primary UI user in `test_web_api.py` |
| `UI_USER_EMAIL_2` / `UI_USER_PASSWORD_2` | Optional 2nd UI user (both required to add it) |

To use env vars locally, copy the template and fill it in (`.env` is gitignored):

```bash
cp .env.example .env
```

## Docker

The image is based on the official Playwright image (browsers + OS deps
preinstalled), tagged to match `playwright==1.60.0`.

```bash
docker build -t playwright-tests .
docker run --rm --ipc=host \
  -e API_USER_EMAIL -e API_USER_PASSWORD \
  -e UI_USER_EMAIL -e UI_USER_PASSWORD \
  playwright-tests
```

`--ipc=host` prevents Chromium crashing on a small `/dev/shm` in containers.
Omit the `-e` flags to use the `credentials.json` fallback.

## Jenkins pipeline

The `Jenkinsfile` is a declarative pipeline that builds the Dockerfile, runs the
suite inside it, publishes the JUnit results, and archives the HTML report.

**One-time setup**

1. Run Jenkins with access to a Docker daemon (socket mounted):
   ```bash
   docker run -d --name jenkins -p 8080:8080 \
     -v jenkins_home:/var/jenkins_home \
     -v /var/run/docker.sock:/var/run/docker.sock \
     jenkins/jenkins:lts
   ```
2. Unlock (`docker logs jenkins`), install suggested plugins **+ Docker Pipeline**.
3. Add credentials (Manage Jenkins → Credentials → Secret text) with these IDs:
   `api-user-email`, `api-user-password`, `ui-user-email`, `ui-user-password`.
4. New Item → **Pipeline** → "Pipeline script from SCM" → Git → your repo URL.
   It auto-discovers the `Jenkinsfile`.

**Run**

- **Build Now** to run manually.
- Automate with a GitHub webhook to `http://<jenkins>/github-webhook/`, or
  "Poll SCM" if Jenkins isn't publicly reachable.

Results appear per-test in the build page (JUnit); `report.html` is a downloadable
build artifact. For an inline HTML view, install the HTML Publisher plugin and
swap `archiveArtifacts` for `publishHTML`.

## Recommended workflow

Build and run the Docker image locally first — if it's green there, Jenkins runs
the exact same thing, so debug in Docker (fast loop) rather than in Jenkins.

## Notes / TODO

- `test_web_api.py` / `test_framework_web_api.py` assert a hardcoded item name
  (`"ZARA COAT 3"`) — brittle once running unattended.
- Tests hit the live `rahulshettyacademy.com`, so CI needs outbound internet.
- `data/credentials.json` remains as a local fallback; it also lives in git
  history. Scrub history separately if those secrets ever become real.
