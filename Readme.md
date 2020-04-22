# Fastai2 template with Fastapi

## Usage

You will need to supply a model for your app. Clone the repo and open up `app/server.py` and replace `export_url = "url"` to your host of choice.

### Dropbox

If you decide to use dropbox make sure you have `dl=1` at the end of your url. EX: `"https://www.dropbox.com/s/randnumbers/<export_name>.pkl?dl=1"`

## To run (with docker)

Clone the repo and use `docker build . -t fastapi-fastai2` Then you can use `docker run -p 8888:8000 fastapi-fastai2` and go to `localhost:8888` to see the app.

### Windows 10

When running `docker run -p 8888:8000 fastapi-fastai2` after installation you may not be able to use `localhost:8888`. Docker was mapping ports to `127.0.0.1:8888` on my machine. Otherwise you can try `netstat -a` in your powershell to find the ip/port.

## To run (without docker)

You can try `python app/server.py` although I've not been able to get pytorch/fastai to play nice on my windows machine. And on my ubuntu 19.04 machine I had several problems as well. Still unsolved.

## Why?

I had quite a few difficulties getting the [fastai2-starlette](https://github.com/muellerzr/fastai2-Starlette) app working (it wouldn't) on my machine (windows 10). This repo may work for you, and if it does great! If not or, if you prefer FastAPI, please consider using this repo.

I want to thank muellerzr for his work on that repo as without it I wouldn't have had a straightforward reference. Please check out his [walk with fastai2](https://forums.fast.ai/t/a-walk-with-fastai2-vision-study-group-and-online-lectures-megathread/59929) it's really great!
