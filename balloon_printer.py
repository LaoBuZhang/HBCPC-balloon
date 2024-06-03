from Lib.Config.config import Config
from Lib.Oauth.oauth import Oauth
from Lib.Protocol.rpc_client import RpcClient
from Lib.Api.yly_print import YlyPrint
import datetime
import random
import json


def generate_order_number():
    current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    random_digits = str(random.randint(0, 999)).zfill(3)
    order_number = f'{current_time}{random_digits}'
    return order_number

def printer():
    cfg=""
    with open('./config/cfg.json', 'r') as f:
        cfg = json.load(f)
    client_id=cfg['client_id']
    client_secret=cfg['client_secret']
    machine_id=cfg['machine_id']

    config = Config(client_id, client_secret)
    oauth_client = Oauth(config)

    token_data = oauth_client.get_token()
    access_token = token_data['body']['access_token']

    rpc_client = RpcClient(config, access_token)

    with open('./data/printer.txt', 'r',encoding="UTF-8") as file:
        contents = file.read()


    print_service = YlyPrint(rpc_client)
    response=print_service.index(machine_id, contents, generate_order_number())
