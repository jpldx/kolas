from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ProjectSaveForm(BaseModel):
    project_name: str
    icon_url: str

@app.post("/project/save")
async def save_project(form: ProjectSaveForm):
    return "ok"

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        port=8020,
        app="main:app",
        reload=True
    )