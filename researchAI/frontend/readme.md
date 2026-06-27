# Frontend local run guide

## Run the app locally

1. Start the backend API first.
   - From the project root, run:
     ```bash
     cd researchAI/model/api
     python main.py
     ```
   - The API should be available at `http://localhost:8000`.

2. Start the Streamlit frontend in a second terminal.
   - From the project root, run:
     ```bash
     cd researchAI/frontend
     streamlit run app.py
     ```

## API URL configuration

The frontend now uses the API URL from the environment if it is provided:

```python
api_url = os.environ.get("API_URL", "http://localhost:8000")
```

If you want to point the frontend to a different backend, set:

```bash
set API_URL=http://your-api-host:8000
```

## Local testing

You can run the non-cloud test workflow from the repository root with:

- PowerShell: `./scripts/run_local_tests.ps1`
- Bash: `./scripts/run_local_tests.sh`

## Notes

The current UI includes topic-graph support, evidence cards, related-item suggestions, and MCP-style research exploration, so the local workflow is now more aligned with the latest product changes.

