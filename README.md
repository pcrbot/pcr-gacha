# Usage

## Quickstart

Install packages: `pip install -r requirements.txt`

Run `python3 gacha.py`

Open your browser to visit `http://127.0.0.1:5001/`

## Maintaining the prize pool

Just put any picture in the `icon` folder, the prize pool would refresh every 5 minutes.

## Deploy to nginx

Step 1: Creat file `uwsgi.ini` like this and **remove all comment**

```ini
[uwsgi]
socket = 127.0.0.1:5001
chdir = /path/to/your/project/ ; change it to your project path
module  = gacha:app
processes = 4 ; depends on your serving
threads = 2 ; depends on your serving
master = true
daemonize = uwsgi.log
pidfile = uwsgi.pid
vacuum = true
```

Step 2: Run `uwsgi uwsgi.ini --wsgi-disable-file-wrapper`

Please notice that `--wsgi-disable-file-wrapper` is neccessary because
`BytesIO` is used.

Step 3:

Add this to your Nginx config file

```nginx
location = /gacha.jpg {
    include uwsgi_params;
    uwsgi_pass 127.0.0.1:5001;
}
```

Now visit `your.domain/gacha.jpg`
