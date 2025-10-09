from fastapi import FastAPI, Request
import time
import asyncio

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    await asyncio.sleep(10)  # Simulate delay
    response = await call_next(request)
    process_time = round(time.time() - start_time, 4)
    response.headers["X-Process-Time"] = str(process_time)

    # Print all response headers
    print("Response headers:")
    for key, value in response.headers.items():
        print(f"{key}: {value}")

    return response


@app.get("/hello")
async def hello():
    return {"message": "Hello, world!"}

