from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

redis = get_redis_connection(
    host="localhost",
    port=6379,
    decode_responses=True
)

@app.get('/parse/{timestamp}/')
@app.get('/parse/{timestamp}/{market}/')
@app.get('/parse/{timestamp}/{market}/{exchange}/')
async def parse(timestamp: int, market: str = '*', exchange: str = '*'):
    keys = redis.keys(f"prices:{timestamp}:{market}:{exchange}")
    data = {}
    for key in keys:
        data[key] = redis.get(key)

    return {'data': data}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)