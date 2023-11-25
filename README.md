# GitHub Actions for building and pushing Docker images to Docker Hub
2023-11-25, J. Köppern
[Link to GitHub Repository](https://github.com/koeppern/github_actions)

## Overview

Note: YouÄll need to fork this repository to your own GitHub account to be able to use GitHub Actions (also configure your own PAT). Be aware that the forked repository will be public!

### Our goal we want to achieve with GitHub Actions

- Build a Docker image for this repo's FastAPI application.
- Push the Docker image to GitHub Container Registry.
- Trigger: Whenever a commit is pushed to the main branch.

### What are GitHub Actions?

- GitHub Actions: Automate, customize, and execute your software development workflows right in your repository.
- Will build and push a Docker image to GitHub Container Registry.
- GitHub Actions have a trigger, a workflow, and one or more jobs.
- Job: A set of steps that execute on the same runner.
- Hint/CR_PAT: Container Registry Personal Access Token

### What is GitHub Container Registry?

- GitHub Container Registry: Store and manage container images within GitHub Packages.
- Dockwer Images consist of multiple layers -> multiple files. All files are bundeled into a single .tar file called a Docker Image.
- Docker Images are stored in a Docker Registry. Docker Hub is the most popular one but we'll use GitHub Container Registry for simplicity.


### How to create the QR-PAT (Container Registry Personal Access Token)?

- GitHub website -> Settings -> Developer Settings -> Personal Access Tokens -> Generate new token -> classic
- Set note e.g. "CR_PAT"
- Select the following scopes: `read:packages` and `write:packages`
- Click "Generate token"
- Copy the token to youtr clipboard
- Add the token to your repository's secrets as `CR_PAT` (in GitHub repository settings, go to your repository first).
  - Secrets and variables -> Actions -> Click "New repository secret" -> Name: `CR_PAT` -> Value: Paste the token from your clipboard -> Click "Add secret"
  - The name of this token must be refleected in the GitHub Actions workflow yaml file (see below).



### Where can I find my images in the GitHub Container Registry?

- GitHub website -> Your repository -> Packages -> Container registry
- You should see the Docker image that was built and pushed by the GitHub Action.

## Starting the Uvicorn server locally

```bash
# Starting the Uvicorn server locally
uvicorn app:app --reload
```

## Building the Docker image locally

```bash
# Building and running the Docker image for the FastAPI application
docker buildx build -t my-python-app .
```

```bash
# Running the container in interactive terminal mode with port mapping
docker run -it -p 8000:8000 my-python-app
```

## Set-Up GitHub Actions

### Prerequisite: CR_PAT (Container Registry Personal Access Token) for authentication

- Create a new Personal Access Token (PAT) with the `read:packages` and `write:packages` scopes.
- Store the PAT in the GitHub repository's secrets as `CR_PAT` (in GitHub repository settings).


### Create a GitHub Actions workflow

- Create a new file in the `.github/workflows` directory.
- Name the file `build-and-push-docker-image.yml`.
- Add the following content to the file:

```yaml
name: Build and Push Docker Image

on:
  push:
    paths:
      - 'app.py'
      - 'Dockerfile'
      - '.github/workflows/build-and-push-docker-image.yml'
    branches:
      - master

jobs:
  build_and_push:
    runs-on: ubuntu-latest

    steps:
      - name: Check Out Repo
        uses: actions/checkout@v2

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v1

      - name: Login to GitHub Container Registry
        uses: docker/login-action@v1
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.CR_PAT }}

      - name: Build and Push Docker Image
        uses: docker/build-push-action@v2
        with:
          context: .
          file: ./Dockerfile
          push: true
          tags: ghcr.io/${{ github.repository }}/my-python-app:${{ github.run_number }}
```

