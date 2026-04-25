FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
# expose both common ports (Streamlit default 8501 and HTTP 80)
EXPOSE 80 8501

# Wrapper script will choose which server to run based on START_MODE env var:
# START_MODE=api   -> runs uvicorn on port $PORT or 80
# START_MODE=streamlit -> runs streamlit on port $PORT or 8501
COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
