# 1. Start from a Python image that already has Python installed
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the dependency list first (for better caching)
COPY requirements.txt .

# 4. Install Python dependencies inside the container
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your app code into the container
COPY . .

# 6. Expose the port Streamlit runs on (default is 8501)
EXPOSE 8501

# 7. Command to start the Streamlit app when the container runs
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
