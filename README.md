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
docker run -it --rm -v $PWD:/app -p 5001:5001 gastro-gpt bash
```
This maps the backend port 5001 to your host and starts an interactive shell inside the container.

###  3. Build the React frontend
Inside the container:

```bash
cd rag-frontend
npm run build
```
This creates a production build in rag-frontend/build that the Flask backend will serve.

###  4. Start the Flask backend
Inside the container:

```bash
cd backend
python app.py
```
The backend will start on:
http://127.0.0.1:5001

###  5. Open the app in your browser
Visit:
http://127.0.0.1:5001

You should see the Restaurant RAG Assistant interface.
It will auto-detect your location and allow you to ask location-aware restaurant questions like:

I want to eat Chinese food.

