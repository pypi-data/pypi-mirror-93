import gwcomm as comm

lg = comm.logger(__name__)
comm.add_env(["API_HTTP", "API_HOST", "API_PORT",
              "API_DATA", "API_USR", "API_PWD"])


def get(url):
    import requests
    from .auth import get_header
    conf = comm.sysconf
    dataurl = conf.get("api", {}).get("data", "") if conf.get("api", {}).get(
        "data", "") != "" else "{}://{}:{}{}".format(conf.get("api_http", "http"), conf.get("api_host", "127.0.0.1"), conf.get("api_port", "5000"), conf.get("api_data", "/"))
    url = "{}{}".format(dataurl, url)
    header = get_header(conf.get("token", None))
    lg.info(f"init - url: {url}")
    try:
        res = requests.get(url, headers=header)
    except:
        lg.error(f"Error - connection fail - {url}")
        comm.sysconf["token"] = None
        return {}

    if res.status_code != 200:
        lg.error(f"Error - {res.json()}")
        comm.sysconf["token"] = None
        return {}
    return res.json()


def upsert(url, data):
    import requests
    from .auth import get_header
    conf = comm.sysconf
    dataurl = conf.get("api", {}).get("data", "") if conf.get("api", {}).get(
        "data", "") != "" else "{}://{}:{}{}".format(conf.get("api_http", "http"), conf.get("api_host", "127.0.0.1"), conf.get("api_port", "5000"), conf.get("api_data", "/"))
    url = "{}{}".format(dataurl, url)
    header = get_header(conf.get("token", None))
    lg.info(f"init - url: {url}")
    try:
        res = requests.post(url, json=data, headers=header)
    except:
        lg.error(f"Error - connection fail - {url}")
        comm.sysconf["token"] = None
        return False
    if res.status_code != 200:
        lg.error(f"Error - {res.json()}")
        comm.sysconf["token"] = None
        return False
    return True
