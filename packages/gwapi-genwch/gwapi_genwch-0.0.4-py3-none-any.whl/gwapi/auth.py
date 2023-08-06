import gwcomm as comm

lg = comm.logger(__name__)
comm.add_env(["API_HTTP", "API_HOST", "API_PORT",
              "API_DATA", "API_USR", "API_PWD"])


def get_token():
    import requests
    conf = comm.sysconf
    url = conf.get("api", {}).get("auth", "") if conf.get("api", {}).get(
        "auth", "") != "" else "{}://{}:{}/auth".format(conf.get("api_http", "http"), conf.get("api_host", "127.0.0.1"), conf.get("api_port", "5000"))
    body = {"usr_cde": conf.get("api_usr", ""),
            "password": conf.get("api_pwd", "")}
    lg.info(f"init - url: {url}")
    try:
        res = requests.post(url, json=body)
    except:
        lg.error(f"Error - connection fail - {url}")
        comm.sysconf["token"] = None
        return None
    if res.status_code != 200:
        lg.error(f"Error - {res.msg}")
        comm.sysconf["token"] = None
        return None
    token = res.json().get("access_token")
    comm.sysconf["token"] = token
    return token


def get_header(token=None):
    token = get_token() if token == None else token
    if token == None:
        lg.error("Error - no token")
        return {}
    return {"Authorization": f"Bearer {token}"}
