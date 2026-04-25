Environment setup (conda, recommended)

This project uses some heavy binary packages (pandas, numpy, faiss, sentence-transformers). On Windows, building these from source with pip is error-prone because of MSVC build-tool requirements. Use Anaconda/Miniconda to install binary wheels.

Quick steps (Anaconda Prompt)

1. Open Anaconda Prompt.
2. Run the helper script:
   powershell
   .\scripts\env_setup_ps1

Or run commands manually:

```powershell
conda create -n rag_env python=3.10 -y
conda activate rag_env
conda config --env --add channels conda-forge
conda config --env --set channel_priority strict
conda install -y -c conda-forge numpy pandas scikit-learn sentence-transformers faiss-cpu
conda install -y -c pytorch cpuonly pytorch
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

Notes
- If `faiss-cpu` is not available on your platform, skip installing it; the repo contains a fallback vector search.
- If you prefer to use `openai` instead of `ollama`, set `LLM_PROVIDER=openai` and add `OPENAI_API_KEY` in your environment.
- After setup, run the app with:

```powershell
streamlit run app.py
```
