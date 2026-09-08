from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="ASEEL Project API")

# ربط ملف routes بالتطبيق الرئيسي
app.include_router(router)

@app.get("/")
def root():
    return {"status": "FastAPI is active"}