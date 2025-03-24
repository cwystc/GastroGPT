# GastroGPT

An LLM-powered restaurant recommendation app that meets users’ personalized needs.

---

##  Getting Started (with Docker)

To ensure a stable and reproducible environment, we recommend running this project inside a Docker container.

###  1. Build the Docker image

```bash
docker build -t gastro-gpt .
```

###  2. Run the app (interactive dev mode)

Mount your local project directory and run the app inside a container:

```bash
docker run -it --rm -v $PWD:/app gastro-gpt bash
```

Then inside the container:

```bash
python main.py
```
