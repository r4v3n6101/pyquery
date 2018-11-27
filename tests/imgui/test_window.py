import time

from imgui import *

from vquery import *

controllers = []
host = "46.174.48.49"
port = 27201
goldsrc = False


def players_header(players):
    expand, _ = collapsing_header("Players")
    if expand:
        columns(4, "players")
        separator()
        header = ["ID", "Name", "Duration", "Score"]
        for title in header:
            text(title)
            next_column()
        separator()
        for player in players:
            text(str(player["index"]))
            next_column()
            text(player["name"])
            next_column()
            text(str(player["duration"]))
            next_column()
            text(str(player["score"]))
            next_column()
        columns(1)
        separator()


def rules_header(rules):
    expand, _ = collapsing_header("Rules")

    if expand:
        columns(2, "rules")
        separator()
        header = ["Rule", "Value"]
        for title in header:
            text(title)
            next_column()
        separator()
        for rule, value in rules.items():
            text(rule)
            next_column()
            text(value)
            next_column()
        columns(1)
        separator()


def info_header(info):
    pass  # TODO


def server_info(controller):
    _, opened = begin(controller.name, True)

    if button("Update"):
        controller.update()
    same_line()
    text("Updated in {}ms".format(controller.ping))

    info_header(controller.info)
    players_header(controller.players)
    rules_header(controller.rules)

    end()

    return opened


def server_setup():
    global controllers, host, port, goldsrc

    begin("Server producer")
    _, host = input_text('Host', host, 256)
    _, port = input_int('Port', port)
    _, goldsrc = checkbox("GoldSrc", goldsrc)
    if button("Connect"):
        controller = QueryController(
            "{}:{}".format(host, port),
            ValveQuery(host, port, GOLDSRC if goldsrc else SOURCE)
        )
        controller.update()
        controllers.append(controller)
    end()


def imgui_loop():
    global controllers
    server_setup()  # Show setup
    controllers[:] = [x for x in controllers if server_info(x)]  # Keep opened windows & show them


class QueryController:
    def __init__(self, name, query):
        self._query = query
        self._info = {}
        self._name = name
        self._players = []
        self._rules = []
        self._ping = 0

    def update(self):
        before = time.time()
        challenge = self._query.get_challenge()
        self._info = self._query.a2s_info()
        self._players = self._query.a2s_player(challenge)['players']  # TODO : And what?
        self._rules = self._query.a2s_rules(challenge)['rules']
        after = time.time()
        self._ping = int((after - before) * 1000)  # In ms

    @property
    def name(self):
        return self._name

    @property
    def info(self):
        return self._info

    @property
    def players(self):
        return self._players

    @property
    def rules(self):
        return self._rules

    @property
    def ping(self):
        return self._ping
