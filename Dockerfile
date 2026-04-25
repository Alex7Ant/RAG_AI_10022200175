FROM continuumio/miniconda3:latest

WORKDIR /app

# Copy project files
COPY . /app
COPY requirements.txt /app/requirements.txt

# Create conda environment `rag_env` with Python 3.10 and install pip requirements
RUN conda create -y -n rag_env python=3.10 && \
	/bin/bash -lc "source /opt/conda/etc/profile.d/conda.sh && conda activate rag_env && pip install --no-cache-dir -r /app/requirements.txt"

# Expose common ports (Streamlit default 8501 and HTTP 80)
EXPOSE 80 8501

# Copy and make the start script executable
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Use the start wrapper which activates `rag_env` then launches the selected server
CMD ["/start.sh"]
