$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot
& "$projectRoot\.venv\Scripts\python.exe" -m streamlit run app.py --server.headless true --server.port 8501
