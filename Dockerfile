# Official Playwright image: Python + all browsers + OS deps preinstalled.
# Tag matches your playwright==1.60.0 so the browser binaries line up.
FROM mcr.microsoft.com/playwright/python:v1.60.0-noble

WORKDIR /app

# Install Python deps first so this layer is cached until requirements change.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project.
COPY . .

# Run the suite. Point pytest at the package dir so `utils`/`page_objects`
# imports resolve, and emit both a JUnit report (for Jenkins to parse) and a
# self-contained HTML report (for humans to read).
CMD ["pytest", "playwright_course", \
     "--junitxml=results.xml", \
     "--html=report.html", "--self-contained-html", \
     "-v"]
