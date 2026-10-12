# Docker Style Guide

A style guide for Docker images, Compose files and developing with containers.
It is based on Docker's [building best practices](https://docs.docker.com/build/building/best-practices/), the [Dockerfile reference](https://docs.docker.com/reference/dockerfile/) and the rules of [hadolint](https://github.com/hadolint/hadolint).

The house rules apply to Docker files as well: continuation lines and YAML are indented by 4 spaces, lines are at most 80 characters long, and files use UTF-8 and LF line endings.

## Table of contents

[TOC]

## Principles

- **Containers are ephemeral.**
  A container can be stopped, destroyed and replaced by a new one with no extra setup.
  State lives in volumes or external services, never in the container.
- **Images are small.**
  Smaller images build, push and start faster, and contain fewer vulnerabilities.
- **Builds are reproducible.**
  Building the same commit twice produces the same image.
- **One concern per container.**
  Run one service per container, and connect containers over networks.
- **Secure by default.**
  Images run as a non-root user, and never contain secrets.

## Files

### Dockerfile names

A project with a single image has a `Dockerfile` at the root of the build context.

A project with several images names each Dockerfile after the image, with the `.Dockerfile` extension, and builds them with `--file`.

```text
api.Dockerfile
worker.Dockerfile
```

```bash
docker build --file api.Dockerfile --tag lrssn/api .
```

### .dockerignore

Every build context has a `.dockerignore` file.
It keeps the build context small, which makes builds faster, and keeps files out of the image that do not belong there.

```text
# Version control and editor files.
.git
.vscode

# Dependencies and build output, which are created inside the image.
node_modules
dist

# Local configuration and secrets.
.env
*.pem

# Files that are not needed to build the image.
*.md
compose*.yaml
Dockerfile
```

A Dockerfile with a custom name can have its own ignore file next to it, named after the Dockerfile, such as `api.Dockerfile.dockerignore`.

### Compose file names

The Compose file is named `compose.yaml`.
Development overrides go in `compose.override.yaml`, which Docker Compose merges automatically.
See [Docker Compose](#docker-compose).

### Line endings

Scripts that are copied into Linux images must have LF line endings, or they fail with errors such as `env: 'sh\r': No such file or directory`.
Add the scripts to `.gitattributes`, as described in the [Bash style guide](./Bash.md#line-endings).

## Dockerfile structure

A Dockerfile consists of the following, in order:

1. The `syntax` parser directive.
1. A comment that describes the image.
1. Global `ARG` instructions for base image versions.
1. The build stages, in the order they depend on each other.
1. The final stage, which produces the image that is shipped.

### Syntax directive

Start every Dockerfile with the `syntax` directive.
It makes BuildKit use the latest stable Dockerfile syntax, which supports features such as cache mounts, secret mounts and here documents.

```dockerfile
# syntax=docker/dockerfile:1
```

### Header comment

Describe what the image is for and how to build it.

```dockerfile
# syntax=docker/dockerfile:1

# The API server.
#
# Build: docker build --tag lrssn/api .
# Run:   docker run --publish 8080:8080 lrssn/api
```

### Instruction order within a stage

Order the instructions of a stage from the least to the most frequently changing.
Docker reuses the cached layers up to the first instruction whose input has changed, so instructions that rarely change should come first.

1. `FROM`.
1. `ARG` and `ENV` for the build.
1. System packages.
1. Users and groups.
1. `WORKDIR`.
1. Dependency manifests, such as `package.json` and `go.mod`.
1. Installing dependencies.
1. The source code.
1. Building the application.
1. `USER`, `EXPOSE`, `HEALTHCHECK`, `ENTRYPOINT` and `CMD`.

## Formatting

### Instruction case

Write instructions in upper case, and keywords such as `AS` in upper case as well.

```dockerfile
# Good:
FROM golang:1.24-bookworm AS build

# Bad:
from golang:1.24-bookworm as build
```

### Comments

Comments start with `#` at the beginning of a line.
Dockerfiles do not support comments at the end of a line: a `#` after an instruction is passed to the instruction as an argument.

```dockerfile
# Good: install the certificates for HTTPS requests.
RUN apk add --no-cache ca-certificates

# Bad: the comment is passed to apk as package names.
RUN apk add --no-cache ca-certificates # For HTTPS requests.
```

### Blank lines

Separate logical groups of instructions with a single blank line, and stages with a blank line and a comment that describes the stage.

### Line length and continuation

Lines are at most 80 characters long.
Split long `RUN` instructions with a backslash at the end of each line.

- Indent continuation lines by 4 spaces.
- Start continuation lines with `&&` when chaining commands.
- Put each package on its own line, indented by 8 spaces, and sort the packages alphabetically.
  Sorted lists are easier to review and avoid duplicates.

```dockerfile
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        git \
    && rm -rf /var/lib/apt/lists/*
```

### Here documents

Use a here document for scripts that are longer than a few commands.
It is easier to read than a long chain of `&&` and backslashes.

```dockerfile
RUN <<EOF
set -eu
apt-get update
apt-get install -y --no-install-recommends ca-certificates curl
rm -rf /var/lib/apt/lists/*
EOF
```

Start every here document with `set -eu`, so that it stops at the first failing command.
Scripts that are longer than about 10 lines belong in a separate file that is copied into the image.

### Exec form

Write `ENTRYPOINT`, `CMD` and `SHELL` in exec form, as a JSON array.
JSON requires double quotes.

```dockerfile
# Good:
CMD ["node", "server.js"]

# Bad: runs in a shell, so the process does not receive signals.
CMD node server.js
```

### Key-value format

Write `ENV`, `ARG` and `LABEL` as `key=value`.
The older `ENV key value` format is deprecated.

```dockerfile
# Good:
ENV NODE_ENV=production

# Bad:
ENV NODE_ENV production
```

## Base images

### Official and minimal images

Use [Docker Official Images](https://docs.docker.com/trusted-content/official-images/) or images from verified publishers as the base.
Use the smallest image that works:

| Image | Use for |
| --- | --- |
| `-slim` variants, such as `python:3.12-slim-bookworm` | Most applications |
| `alpine` | Small images, if the application works with the musl C library |
| `gcr.io/distroless/*` | Runtime images that need no shell or package manager |
| `scratch` | Static binaries, such as Go programs built with `CGO_ENABLED=0` |

### Pin the version

Never use the `latest` tag, or no tag at all, as the base image changes without warning.
Pin at least the minor version and the distribution.

```dockerfile
# Good:
FROM node:22.11-bookworm-slim

# Bad:
FROM node
FROM node:latest
```

For fully reproducible builds, pin the digest as well, and let a tool such as [Dependabot](https://docs.github.com/en/code-security/dependabot) or [Renovate](https://docs.renovatebot.com/) keep it up to date.

```dockerfile
FROM node:22.11-bookworm-slim@sha256:<digest>
```

### Versions as arguments

Put the versions of base images in `ARG` instructions at the top of the file, so that they are easy to find and to update.

```dockerfile
ARG GO_VERSION=1.24
ARG DEBIAN_VERSION=bookworm

FROM golang:${GO_VERSION}-${DEBIAN_VERSION} AS build
```

### Rebuild regularly

Rebuild images regularly with `--pull`, so that they include the security updates of the base image.
Do not run `apt-get upgrade` in a Dockerfile; update the base image instead.

## Multi-stage builds

Use multi-stage builds to keep build tools out of the final image.
The build stages compile the application, and the final stage only copies the result.

- Name every stage with `AS`, in lowercase, such as `build`, `test` and `runtime`.
- Copy files between stages with `COPY --from=<stage>`.
- Put the stage that is shipped last, so that a build without `--target` produces it.

```dockerfile
# syntax=docker/dockerfile:1

ARG GO_VERSION=1.24

# Compile a static binary.
FROM golang:${GO_VERSION}-bookworm AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /out/server ./cmd/server

# Ship only the binary.
FROM gcr.io/distroless/static-debian12:nonroot AS runtime
COPY --from=build /out/server /server
# The nonroot user of the distroless image.
USER 65532:65532
EXPOSE 8080
ENTRYPOINT ["/server"]
```

## Instructions

### LABEL

Label images with the [OCI annotation keys](https://github.com/opencontainers/image-spec/blob/main/annotations.md), in a single `LABEL` instruction.
Pass values that change on every build, such as the version, as build arguments.

```dockerfile
ARG VERSION=dev
LABEL org.opencontainers.image.title="api" \
    org.opencontainers.image.description="The Lrssn API server" \
    org.opencontainers.image.source="https://github.com/Lrssn-blog/api" \
    org.opencontainers.image.licenses="MIT" \
    org.opencontainers.image.version="${VERSION}"
```

### RUN

#### Package managers

Run the package index update and the install in the same `RUN` instruction.
If they are separate, Docker reuses an old cached index when the package list changes.

- Use `--no-install-recommends` with `apt-get install`, so that only the required packages are installed.
- Remove the package lists in the same instruction, so they do not end up in the layer.
- Use `apk add --no-cache` on Alpine, which does not store the index.

```dockerfile
# Debian and Ubuntu:
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Alpine:
RUN apk add --no-cache \
    ca-certificates \
    curl
```

Do not pin the versions of distribution packages.
Old versions are removed from the package repositories, which breaks the build, and pinning prevents security updates.
Pin the base image instead, and pin application dependencies with lock files.

#### Pipes

The default shell does not fail when a command in a pipe fails.
Set `pipefail` with a `SHELL` instruction before any `RUN` that uses a pipe.

```dockerfile
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -fsSL https://example.com/install.sh | bash
```

#### Cache mounts

Use cache mounts for package manager caches.
The cache is kept between builds but is not part of the image.

```dockerfile
# The cache mount keeps the pip cache out of the image.
# hadolint ignore=DL3042
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --requirement requirements.txt
```

hadolint warns about pip's cache directory (`DL3042`) because it does not know about cache mounts, so disable the warning for that instruction with a comment that explains why.

#### Other rules

- Do not use `cd` in `RUN`; set the directory with `WORKDIR` instead.
- Do not use `sudo`, as the build already runs as root until `USER` is set.
- Do not use `RUN` to start services; containers start their process with `ENTRYPOINT` and `CMD`.

### COPY versus ADD

Use `COPY` to copy files into the image.
Only use `ADD` to download a remote file with a checksum, or to extract a local archive.

```dockerfile
COPY package.json package-lock.json ./

ADD --checksum=sha256:<checksum> \
    https://example.com/tool.tar.gz /tmp/tool.tar.gz
```

hadolint 2.12 cannot parse the `--checksum` flag and reports it as invalid, even though Docker supports it.

Copy only the files a step needs.
Copy dependency manifests and install the dependencies before copying the rest of the source, so that the dependencies are cached when only the source changes.

```dockerfile
# Good: the dependencies are only installed again when the manifests change.
COPY package.json package-lock.json ./
RUN npm ci
COPY . .

# Bad: every source change installs the dependencies again.
COPY . .
RUN npm ci
```

Set the owner of copied files with `--chown` instead of a separate `RUN chown`, which would duplicate the files in a new layer.

### ENV and ARG

Use `ARG` for values that are only needed while building, and `ENV` for values that the running container needs.
Both are visible in the image history, so neither may contain secrets.
See [Secrets](#secrets).

```dockerfile
ARG NODE_VERSION=22.11
ENV NODE_ENV=production
ENV PATH="/app/bin:${PATH}"
```

### WORKDIR

Set the working directory with `WORKDIR`, using an absolute path.
`WORKDIR` creates the directory if it does not exist.

```dockerfile
WORKDIR /app
```

### USER

Run the container as a non-root user.
Create the user with a fixed numeric ID, and set it with the numeric ID, so that orchestrators can verify that the user is not root.

```dockerfile
RUN groupadd --system --gid 10001 app \
    && useradd --system --uid 10001 --gid app --no-create-home app
USER 10001:10001
```

Official images often include a non-root user that can be used instead, such as `node` (ID 1000) in the Node.js images and `nonroot` (ID 65532) in the distroless images.

### EXPOSE

Document the ports the application listens on with `EXPOSE`.
Listen on a port above 1024, since a non-root user cannot bind to lower ports.

```dockerfile
EXPOSE 8080
```

### ENTRYPOINT and CMD

Use `ENTRYPOINT` for the main executable of the image, and `CMD` for its default arguments.
Users can then override the arguments without repeating the executable.

```dockerfile
ENTRYPOINT ["/app/server"]
CMD ["--port", "8080"]
```

The process in the container runs as PID 1, which must handle signals and reap child processes.
If the application does not do this, run the container with `docker run --init`, or use [tini](https://github.com/krallin/tini) as the entrypoint.

Entry point scripts end with `exec "$@"`, so that the main process replaces the shell and receives signals.

```bash
#!/bin/sh
set -eu

# Wait for the database before starting.
/app/wait-for-db

exec "$@"
```

### HEALTHCHECK

Add a `HEALTHCHECK` to images that run a service, unless the orchestrator defines its own health checks.

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
    CMD ["curl", "-fsS", "http://localhost:8080/healthz"]
```

### VOLUME

Use `VOLUME` for data that the container writes and that must outlive it, such as database files.
Do not declare volumes in base images, as images built on them cannot change the files in the volume.

### ONBUILD

Do not use `ONBUILD`.
It runs instructions in images that are built from yours, which is hard to see and to debug.

## Secrets

Never put secrets in an image.
Values in `ENV`, `ARG`, `LABEL` and copied files stay in the image layers and history, even if a later instruction removes them.

Use secret mounts to make a secret available to a single `RUN` instruction.

```dockerfile
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
    npm ci
```

```bash
docker build --secret id=npmrc,src="${HOME}/.npmrc" .
```

Use SSH mounts to clone private repositories during the build.

```dockerfile
RUN --mount=type=ssh \
    git clone git@github.com:Lrssn-blog/private-repo.git
```

Pass secrets to running containers at runtime, as environment variables or with the secrets of the orchestrator or of [Docker Compose](https://docs.docker.com/compose/how-tos/use-secrets/).

## Image names and tags

### Image names

Image names are lowercase, with hyphens between words, and include the registry and the organization.

```text
ghcr.io/lrssn-blog/api
```

### Tags

Tag release images with their [Semantic Version](./Git.md#versioning), and with the shorter versions that point to the newest matching release.

| Tag | Points to |
| --- | --- |
| `1.4.2` | Exactly this release, never moved |
| `1.4` | The newest `1.4.x` release |
| `1` | The newest `1.x.y` release |
| `sha-3f2c1a9` | The image built from this commit |
| `latest` | The newest stable release |

Deploy images by their full version or digest, never by `latest` or a moving tag.
Only the full version tag is guaranteed to point to the same image every time.

## Running containers

- Run one process per container.
- Write logs to `STDOUT` and `STDERR`, not to files, so that Docker and the orchestrator can collect them.
- Read configuration from environment variables.
- Shut down cleanly when the container receives `SIGTERM`.
- Use a read-only root file system (`--read-only`) where possible, and write temporary files to a `tmpfs` mount.
- Drop the Linux capabilities that the application does not need.

## Docker Compose

### Formatting

Compose files are YAML, indented by 4 spaces.

- Do not add the `version` key, which is obsolete.
- Name services in lowercase with hyphens between words.
- Quote port mappings, so that they are always read as strings.
- Put `build` or `image` first in each service, followed by the other keys in a consistent order.

```yaml
services:
    api:
        build:
            context: .
            target: runtime
        environment:
            DATABASE_URL: postgres://app@db:5432/app
        ports:
            - "8080:8080"
        depends_on:
            db:
                condition: service_healthy

    db:
        image: postgres:17.2-bookworm
        environment:
            POSTGRES_USER: app
            POSTGRES_PASSWORD_FILE: /run/secrets/db_password
        secrets:
            - db_password
        volumes:
            - db-data:/var/lib/postgresql/data
        healthcheck:
            test: ["CMD", "pg_isready", "--username", "app"]
            interval: 10s
            retries: 5

secrets:
    db_password:
        file: ./secrets/db_password.txt

volumes:
    db-data:
```

### Environment files

Keep local configuration in a `.env` file, which Compose reads automatically.
Never commit `.env`; add it to `.gitignore`, and commit a `.env.example` with every variable and safe placeholder values.
The same applies to files that hold Compose secrets.

### Dependencies between services

Use `depends_on` with `condition: service_healthy` when a service needs another one to be ready, not only started.
The service it depends on needs a `healthcheck`.

### Volumes

Use named volumes for data that must be kept, such as databases.
Use bind mounts only for development, to share the source code with the container.

### Profiles

Put optional services, such as debugging tools, in a profile, so that they only start when asked for.

```yaml
services:
    adminer:
        image: adminer:4.8.1
        profiles: ["debug"]
        ports:
            - "8081:8080"
```

```bash
docker compose --profile debug up
```

## Development

### One Dockerfile for all environments

Use the same Dockerfile for development and production, with a stage for each.
The development stage includes the development dependencies and tools, and the runtime stage only what is needed to run.

```dockerfile
# syntax=docker/dockerfile:1

ARG NODE_VERSION=22.11

# Shared base with the production dependencies.
FROM node:${NODE_VERSION}-bookworm-slim AS base
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev

# Development: all dependencies and live reloading.
FROM base AS dev
RUN npm ci
COPY . .
CMD ["npm", "run", "dev"]

# Build the production bundle.
FROM dev AS build
COPY . .
RUN npm run build

# Production: only the built application.
FROM base AS runtime
ENV NODE_ENV=production
COPY --from=build /app/dist ./dist
# The node user of the base image.
USER 1000:1000
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

### Development overrides

Put development settings in `compose.override.yaml`, which `docker compose up` merges with `compose.yaml` automatically.

```yaml
services:
    api:
        build:
            target: dev
        environment:
            LOG_LEVEL: debug
        develop:
            watch:
                - action: sync
                  path: ./src
                  target: /app/src
                - action: rebuild
                  path: package.json
```

Start the services with [Compose Watch](https://docs.docker.com/compose/how-tos/file-watch/), which syncs source changes into the container and rebuilds it when the dependencies change.

```bash
docker compose watch
```

### Dev containers

Projects that need a complete development environment can define a [dev container](https://containers.dev/).
It works with VS Code and GitHub Codespaces, and gives every developer the same tools.

```json
{
    "name": "api",
    "dockerComposeFile": ["../compose.yaml", "../compose.override.yaml"],
    "service": "api",
    "workspaceFolder": "/app",
    "customizations": {
        "vscode": {
            "extensions": [
                "editorconfig.editorconfig",
                "ms-azuretools.vscode-docker"
            ]
        }
    }
}
```

The file is stored at `.devcontainer/devcontainer.json`.

### Docker on Windows and macOS

On Windows, use Docker Desktop with the WSL 2 backend, and keep the source code inside the WSL file system.
Bind mounts from the Windows file system are much slower.

Files created in a bind mount by a container belong to the user the container runs as.
Run development containers with your own user and group IDs to avoid files owned by root on Linux.

## Tooling

### hadolint

Lint every Dockerfile with [hadolint](https://github.com/hadolint/hadolint), which also runs ShellCheck on the `RUN` instructions.
Add this `.hadolint.yaml` to the root of the repository:

```yaml
failure-threshold: warning
ignored:
    # Distribution package versions are not pinned. See "Package managers".
    - DL3008
    - DL3018
trustedRegistries:
    - docker.io
    - gcr.io
    - ghcr.io
```

```bash
hadolint Dockerfile
```

### Build checks

Run Docker's built-in build checks, which find problems such as inconsistent instruction casing and shell-form commands.

```bash
docker build --check .
```

### Vulnerability scanning

Scan images for known vulnerabilities before they are published, with [Docker Scout](https://docs.docker.com/scout/) or [Trivy](https://trivy.dev/).

```bash
docker scout cves ghcr.io/lrssn-blog/api:1.4.2
trivy image ghcr.io/lrssn-blog/api:1.4.2
```

## See also

- [Docker building best practices](https://docs.docker.com/build/building/best-practices/)
- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [Compose file reference](https://docs.docker.com/reference/compose-file/)
- [hadolint rules](https://github.com/hadolint/hadolint#rules)
