from fastapi import FastAPI

app = FastAPI()

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        port=8020,
        app="main:app",
        reload=True
    )