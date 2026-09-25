# Running DataHub on Windows — Step-by-Step Guide

## Purpose

This guide is designed to set up a **local DataHub environment on Windows** for learning, experimentation, and the DataHub/RAG capstone work.

The approach uses:

- Windows
- Docker Desktop
- WSL 2 backend
- Python virtual environment
- DataHub CLI (`acryl-datahub`)
- DataHub Docker Quickstart

> **Important:** Follow the steps sequentially. Do not proceed to the next step until the current step is working. Use the chat to ask questions about the current step only.

---

# Step 1 — Check Windows prerequisites

Open **PowerShell**.

Run:

```powershell
systeminfo
```

The machine should have enough resources to run DataHub through Docker.

A practical target is approximately:

- **RAM:** 16 GB recommended
- **CPU:** 4 cores or more recommended
- **Free disk:** at least 20 GB
- **Windows:** recent Windows 10/11 installation with WSL 2 support

### What to check

The main concern is whether the machine can comfortably run several Docker containers simultaneously.

### Stop here

Do **not** install anything yet.

If there is uncertainty about the machine's suitability, paste the relevant output of:

```powershell
systeminfo
```

and ask about **Step 1**.

---

# Step 2 — Install Docker Desktop

Download and install **Docker Desktop for Windows** from the official Docker website.
**Note**: https://www.docker.com/products/docker-desktop/?utm_source=chatgpt.com
The website asks to choose an installer for ARM64 or AMD64. 
On a typical Windows PC with an **Intel Core i3/i5/i7** processor, use **AMD64**. Despite the name, **AMD64 does not mean “AMD processor.”** It is the standard 64-bit **x86-64 architecture**, used by both Intel and AMD CPUs.
### Confirm it on Windows

In PowerShell, run:

```
$env:PROCESSOR_ARCHITECTURE
```

If it returns:

```
AMD64
```

→ **Use AMD64.**


During installation, use the **WSL 2 backend** when offered.

After installation:

1. Restart Windows if requested.
2. Start Docker Desktop.
3. Wait until Docker Desktop reports that it is running.

### Verify Docker

Open a **new PowerShell** window and run:

```powershell
docker --version
```

Then:

```powershell
docker compose version
```

Finally run:

```powershell
docker run hello-world
```

The last command should complete successfully and display Docker's hello-world message.

### Stop here

Do not continue to Step 3 until:

```powershell
docker run hello-world
```

works successfully.

---

# Step 3 — Check/install Python

First check whether Python is already installed:

```powershell
python --version
```

Also check:

```powershell
pip --version
```

A currently supported Python version should be used.

If Python is not installed, install it before continuing.

### Stop here

Do not create the DataHub environment yet.

Confirm that:

```powershell
python --version
```

and

```powershell
pip --version
```

work.

---

# Step 4 — Create a DataHub working directory

Create a dedicated directory:

```powershell
mkdir C:\datahub
cd C:\datahub
```

Verify the current directory:

```powershell
pwd
```

It should show something similar to:

```text
Path
----
C:\datahub
```

### Stop here

The expected working directory is:

```text
C:\datahub
```

---

# Step 5 — Create a Python virtual environment

From:

```text
C:\datahub
```

run:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

The PowerShell prompt should now contain:

```text
(.venv)
```

For example:

```text
(.venv) PS C:\datahub>
```

### If PowerShell blocks activation

If an execution-policy error appears, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try again:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Stop here

Do not install DataHub until the virtual environment is successfully activated.

---

# Step 6 — Install the DataHub CLI

First upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Then install the DataHub CLI:

```powershell
pip install acryl-datahub
```

Verify the installation:

```powershell
datahub version
```

A DataHub CLI version should be displayed.

### Why this package is needed

The Python package provides the DataHub command-line tooling used for tasks such as:

- running ingestion commands
- managing ingestion recipes
- interacting with DataHub during development

It does **not** install the DataHub server itself.

The DataHub server will be started through Docker.

### Stop here

Do not start DataHub until:

```powershell
datahub version
```

works.

---

# Step 7 — Start DataHub

This is the point where the DataHub server environment is started.

Run:

```powershell
datahub docker quickstart
```

On the first run, DataHub will download the required Docker images and start the DataHub services.

This may take some time because several containers/images are involved.

You may see messages such as:

```text
Pulling...
Creating...
Starting...
```

This is normal.

### Important

Do not interrupt the process simply because it takes several minutes.

### Stop here

Wait until the Quickstart command finishes or clearly reports that DataHub is running.

If an error occurs, stop here and ask about **Step 7** rather than changing multiple things at once.

---

# Step 8 — Check the Docker containers

Open another PowerShell window.

Run:

```powershell
docker ps
```

For a cleaner view:

```powershell
docker ps --format "table {{.Names}}	{{.Status}}	{{.Ports}}"
```

DataHub will run several containers.

The important thing is that the relevant containers should show a status similar to:

```text
Up ...
```

rather than:

```text
Exited
```

or:

```text
Restarting
```

### Stop here

If any DataHub container is:

```text
Exited
```

or:

```text
Restarting
```

do not continue.

Ask about **Step 8** and provide the output of:

```powershell
docker ps -a
```

---

# Step 9 — Open the DataHub UI

Open a browser and navigate to:

```text
http://localhost:9002
```

The DataHub web interface should load.

This is the main interface used to explore:

- datasets
- metadata
- ownership
- domains
- glossary terms
- lineage
- tags
- data products
- other metadata

### Stop here

Do not configure ingestion yet.

First verify that the DataHub UI loads successfully.

---

# Step 10 — Log in

If the local DataHub installation presents a login screen, use the credentials provided by the version of DataHub installed through Quickstart.

Avoid relying on credentials copied from old tutorials because DataHub's authentication and local setup have changed across versions.

### Stop here

Confirm that the DataHub UI can be accessed successfully before proceeding.

---

# Step 11 — Verify the local DataHub service

The local DataHub installation exposes services used by the UI and ingestion tooling.

The primary local endpoints commonly include:

```text
http://localhost:9002
```

for the DataHub UI and:

```text
http://localhost:8080
```

for the DataHub metadata service/API.

A basic PowerShell check can be attempted with:

```powershell
curl http://localhost:8080/health
```

The exact health response can vary by DataHub version.

### Stop here

If the UI works but the API/health check behaves unexpectedly, ask about **Step 11** before changing anything.

---

# Step 12 — Understand the local architecture

At this point the basic environment should look conceptually like this:

```text
Windows
│
├── Docker Desktop
│   │
│   └── DataHub
│       ├── DataHub Frontend
│       ├── DataHub GMS
│       ├── Kafka
│       ├── Search/indexing service
│       ├── Database
│       └── Supporting services
│
└── Python virtual environment
    │
    └── DataHub CLI
```

The Docker Quickstart manages the infrastructure required by DataHub.

### Important

Do **not** separately install:

- Kafka
- Elasticsearch/OpenSearch
- MySQL/PostgreSQL
- Kubernetes

for this initial local setup.

---

# Step 13 — Understand ingestion

Once the server is working, the next major concept is **ingestion**.

The general DataHub ingestion model is:

```text
Source
   │
   │ ingestion
   ▼
DataHub
   │
   ├── Metadata
   ├── Schema
   ├── Ownership
   ├── Lineage
   ├── Tags
   └── Other metadata
```

For example:

```text
PostgreSQL
     │
     ▼
DataHub ingestion recipe
     │
     ▼
DataHub
```

A typical recipe contains a source and a DataHub sink.

Example structure:

```yaml
source:
  type: postgres
  config:
    host_port: localhost:5432
    database: mydatabase
    username: myuser
    password: mypassword

sink:
  type: datahub-rest
  config:
    server: http://localhost:8080
```

This is only an illustrative example.

**Do not run this recipe yet.**

The actual recipe depends on the source system being connected.

---

# Step 14 — Test ingestion

Once the DataHub server is confirmed to be working, create an ingestion recipe for a small test source.

The general command is:

```powershell
datahub ingest -c recipe.yml
```

The workflow is:

```text
Create recipe
      │
      ▼
Validate recipe
      │
      ▼
Run ingestion
      │
      ▼
Check DataHub UI
      │
      ▼
Inspect imported metadata
```

### Recommended first test

Use a very small and controlled source rather than immediately connecting a large enterprise system.

The purpose of the first ingestion test is simply to verify:

1. source connectivity
2. recipe configuration
3. DataHub ingestion
4. metadata visibility in the UI

---

# Step 15 — DataHub for the RAG/AI project

Once the basic DataHub installation and ingestion work, the environment can be extended for the capstone/RAG experiment.

The conceptual architecture is:

```text
                 ┌──────────────────────┐
                 │       DataHub        │
                 │                      │
                 │ Metadata / Governance│
                 └──────────┬───────────┘
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
        Documents        Chunks        Data Products
             │
             ▼
        RAG Pipeline
             │
       ┌─────┴─────┐
       ▼           ▼
   Vector DB    Graph DB
       │           │
       └─────┬─────┘
             ▼
            LLM
```

The initial goal should **not** be to build the entire architecture immediately.

Recommended progression:

```text
1. Get DataHub running
2. Verify Docker services
3. Explore DataHub UI
4. Ingest a small dataset
5. Explore metadata model
6. Add ownership/domain/glossary metadata
7. Understand DataHub APIs
8. Connect the RAG corpus
9. Catalog documents/chunks
10. Explore graph relationships
```

---

# Troubleshooting

## Docker has insufficient memory

Open:

**Docker Desktop → Settings → Resources**

A practical starting point is:

```text
CPU:       4+
Memory:    8 GB+
Disk:      20 GB+
```

If DataHub repeatedly fails to start, insufficient Docker resources are one of the first things to investigate.

---

## A port is already in use

If DataHub reports that a port is unavailable, identify the process/container using that port before changing configuration.

For example:

```powershell
netstat -ano | findstr :9002
```

or:

```powershell
netstat -ano | findstr :8080
```

Do not randomly change DataHub ports until the conflict is understood.

---

## A container is restarting

Run:

```powershell
docker ps -a
```

Identify the affected container.

Then:

```powershell
docker logs <container-name>
```

For continuously updating logs:

```powershell
docker logs -f <container-name>
```

Paste the relevant error when asking for help.

---

# Resetting the local installation

For a learning/POC environment, it may sometimes be easier to recreate the DataHub environment.

Be careful with commands that remove Docker volumes.

For example:

```powershell
docker compose down -v
```

The `-v` option can remove persisted Docker volumes and therefore delete stored DataHub data.

**Do not run this as a troubleshooting step unless specifically instructed.**

---

# Recommended operating principle for this guide

Use this document interactively.

At each stage:

```text
Read Step
   │
   ▼
Run commands
   │
   ▼
Check result
   │
   ├── Success ──► Continue
   │
   └── Error ────► Ask about this step
```

Do not make several configuration changes simultaneously.

That makes troubleshooting much easier because the cause of a failure remains isolated to the current step.

---

# End State

The desired initial end state is:

```text
Windows
│
├── Docker Desktop
│     │
│     └── DataHub running locally
│
├── Python
│     │
│     └── .venv
│           │
│           └── acryl-datahub CLI
│
└── Browser
      │
      └── http://localhost:9002
```

Once this works, the next stage is to start using DataHub rather than spending time on installation.

