from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
import requests
import json 
import os




app = FastAPI()

# Nastavení Google Custom Search API
API_KEY = "AIzaSyDqy1RL_R9BJgQnTBtd-RBs_LrZNzUuZr0"
CX = "f51cd7d8b534d4a46"
GOOGLE_API_URL = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={CX}"

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())

@app.post("/search")
async def search(request: Request):
    data = await request.json()
    query = data.get("query")

    if not query:
        return {"error": "Query is required"}

    response = requests.get(GOOGLE_API_URL, params={"q": query})
    if response.status_code != 200:
        return {"error": "Failed to fetch data from Google"}

    search_results = response.json().get("items", [])
    results = []
    for item in search_results:
        results.append({
            "title": item.get("title"),
            "link": item.get("link"),
            "snippet": item.get("snippet")
        })


    # Uložení do dočasného souboru
    file_path = "OteGSresults.json"
    with open(file_path, "w", encoding="utf-8") as file4save:
        json.dump(results, file4save, indent=4)

     # Vrátit výsledky jako JSON odpověď
    return JSONResponse(content=results)

@app.get("/download")
async def download_file():
    file_path = "OteGSresults.json"
    return FileResponse(
        path=file_path,
        filename="OteGSresults.json",
        media_type="application/json"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)