from fastapi import FastAPI
# from app.services.forex import get_forex_rates
# from app.services.news import get_news

app = FastAPI()

@app.get("/health")
def health():
    try:
        #check_api() #not implemented
        return {"status": "ok"}
    except:
        return {"status": "degraded"}

@app.get("/forex")
def forex():
    return
    return get_forex_rates()

@app.get("/news")
def news():
    return
    return get_news()