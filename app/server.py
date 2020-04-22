from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastai2.vision.all import *
import uvicorn
import asyncio
import aiohttp
import aiofiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

path = Path(__file__).parent
# REPLACE THIS WITH YOUR URL
export_url = "url"
export_file_name = 'export.pkl'


async def download_file(url, dest):
    if dest.exists():
        return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                f = await aiofiles.open(dest, mode='wb')
                await f.write(await response.read())
                await f.close()


async def setup_learner():
    await download_file(export_url, path / export_file_name)
    try:
        learn = load_learner(path/export_file_name)
        learn.dls.device = 'cpu'
        return learn
    except RuntimeError as e:
        if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
            print(e)
            message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
            raise RuntimeError(message)
        else:
            raise

learn = None
@app.on_event("startup")
async def startup_event():
    """Setup the learner on server start"""
    global learn
    loop = asyncio.get_event_loop()  # get event loop
    tasks = [asyncio.ensure_future(setup_learner())]  # assign some task
    learn = (await asyncio.gather(*tasks))[0]  # get tasks


@app.get('/')
async def homepage():
    html_content = (path / 'views' / 'index.html').open().read()
    return HTMLResponse(content=html_content, status_code=200)


@app.post("/analyze")
async def analyze(file: bytes = File(...)):
    pred = learn.predict(file)
    return {"result": pred[0]}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
