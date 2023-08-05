import websocket
from .Utils.RateLimiter import RateLimiter
import time
from .Utils.FrameModel.FrameModel import FrameModel
import logging
import _thread as thread
from .Utils import WebSocketUtils


class WebSockClient:
    _SB_ai = '2515BDA8-9D3A-47CF-9325-330BC37ADA13'

    def __init__(self, access_token, user_id, enable_trace=False, print_chat=True, print_websocket_frames=False,
                 other_logging=True, global_blacklist_users=None, global_blacklist_words=None):
        self._user_id = user_id
        if global_blacklist_words is None:
            global_blacklist_words = set()
        if global_blacklist_users is None:
            global_blacklist_users = set()
        assert isinstance(global_blacklist_words, set), "blacklists must be set()s"
        assert isinstance(global_blacklist_users, set), "blacklists must be set()s"
        self.global_blacklist_words = global_blacklist_words
        self.global_blacklist_users = global_blacklist_users

        self.channelid_sub_pairs = {}
        self.RateLimiter = RateLimiter

        logging.basicConfig(level=logging.INFO, datefmt='%H:%M', format='%(asctime)s, %(levelname)s: %(message)s')
        self.logger = logging.getLogger("websocket")
        self.logger.disabled = not other_logging

        websocket.enableTrace(enable_trace)
        socket_base = "wss://sendbirdproxyk8s.chat.redditmedia.com"
        ws_params = {
            "user_id": self._user_id,
            "access_token": access_token,
            "p": "Android",
            "pv": 30,
            "sv": "3.0.144",
            "ai": self._SB_ai,
            "SB-User-Agent": "Android%2Fc3.0.144",
            "active": "1"
        }

        self.ws = self._get_ws_app(WebSocketUtils._get_ws_url(socket_base, ws_params))

        self.ws.on_open = lambda ws: self.on_open(ws)
        # self.ws.on_ping = lambda ws, r: self.on_ping(ws, r)
        # self.ws.on_pong = lambda ws, r: self.on_pong(ws, r)

        self.req_id = int(time.time() * 1000)
        self.own_name = None
        self.print_chat = print_chat
        self.print_websocket_frames = print_websocket_frames
        self.last_err = None
        self.is_logi_err = False

        self.after_message_hooks = []

    def _get_ws_app(self, ws_url):
        ws = websocket.WebSocketApp(ws_url,
                                    on_message=lambda ws, msg: self.on_message(ws, msg),
                                    on_error=lambda ws, msg: self.on_error(ws, msg),
                                    on_close=lambda ws: self.on_close(ws))
        return ws

    def on_open(self, ws):
        self.logger.info("### successfully connected to the websocket ###")

    def on_message(self, ws, message):
        resp = FrameModel.get_frame_data(message)
        if self.print_chat:
            WebSocketUtils.print_chat_(resp, self.channelid_sub_pairs)
        if self.print_websocket_frames:
            print(message)

        if resp.type_f == "LOGI":
            self.logger.info(message)
            self._logi(resp)

        if resp.type_f == "MESG" and resp.user.name in self.global_blacklist_users:
            return

        thread.start_new_thread(self._response_loop, (resp,))

    def _logi(self, resp):
        try:
            logi_err = resp.error
        except AttributeError:
            logi_err = False
        if not logi_err:
            self.channelid_sub_pairs = WebSocketUtils._get_current_channels(self._user_id, resp.key)
            self.own_name = resp.nickname
        else:
            self.logger.error(f"err: {resp.message}")
            self.is_logi_err = True

    def _response_loop(self, resp):
        for func in self.after_message_hooks:
            if func(resp):
                break

    def ws_send_message(self, text, channel_url):
        if self.RateLimiter.is_enabled and self.RateLimiter._check():
            return
        if any(blacklist_word in text.lower() for blacklist_word in self.global_blacklist_words):
            return
        payload = f'MESG{{"channel_url":"{channel_url}","message":"{text}","data":"{{\\"v1\\":{{\\"preview_collapsed\\":false,\\"embed_data\\":{{}},\\"hidden\\":false,\\"highlights\\":[],\\"message_body\\":\\"{text}\\"}}}}","mention_type":"users","req_id":"{self.req_id}"}}\n'
        self.ws.send(payload)
        self.req_id += 1

    def ws_send_snoomoji(self, snoomoji, channel_url):
        if self.RateLimiter.is_enabled and self.RateLimiter._check():
            return
        payload = f'MESG{{"channel_url":"{channel_url}","message":"","data":"{{\\"v1\\":{{\\"preview_collapsed\\":false,\\"embed_data\\":{{\\"site_name\\":\\"Reddit\\"}},\\"hidden\\":false,\\"snoomoji\\":\\"{snoomoji}\\"}}}}","mention_type":"users","req_id":"{self.req_id}"}}\n'
        self.ws.send(payload)
        self.req_id += 1

    def ws_send_typing_indicator(self, channel_url):
        payload = f'TPST{{"channel_url":"{channel_url}","time":{int(time.time() * 1000)},"req_id":""}}\n'
        self.ws.send(payload)

    def on_error(self, ws, error):
        self.logger.error(error)
        self.last_err = error

    def on_close(self, ws):
        self.logger.warning("### websocket closed ###")

    # def on_ping(self, ws, r):
    #     print("ping")
    #
    # def on_pong(self, ws, r):
    #     print("pong")
