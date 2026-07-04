import os
from uuid import uuid4
import pytest
import tempfile
import requests

from pychadwick.chadwick import Chadwick


@pytest.fixture
def chadwick():
    return Chadwick()


@pytest.fixture
def team_events():
    team_events = ["1982OAK.EVA", "1991BAL.EVA", "1954PHI.EVN"]
    return team_events


RETROSHEET_RAW = "https://raw.githubusercontent.com/chadwickbureau/retrosheet/master"


def event_url(name):
    # Retrosheet serves event files under seasons/<year>/; year = leading 4 chars
    year = name[:4]
    return f"{RETROSHEET_RAW}/seasons/{year}/{name}"


def get_event_path(url):
    file_path = tempfile.gettempdir() + "/tmp.EVA"
    with open(file_path, "w") as fh:
        fh.write(requests.get(url).text)
    return file_path


def test_chadwick():
    _ = Chadwick()


def test_load_games(chadwick, team_events):
    for team_event in team_events:
        event_path = get_event_path(
            event_url(team_event)
        )
        games = chadwick.games(event_path)
        game = next(games)
        game_it = chadwick.process_game(game)
        record = next(game_it)
        assert "GAME_ID" in record.keys()


def test_load_games_to_df(chadwick, team_events):
    for team_event in team_events:
        event_path = get_event_path(
            event_url(team_event)
        )
        games = chadwick.games(event_path)
        df = chadwick.games_to_dataframe(games)

    games = chadwick.games(event_path)
    df = chadwick.game_to_dataframe(next(games))


def test_load_games_to_df_missing_path(chadwick, team_events):
    event_path = os.path.join(tempfile.gettempdir(), uuid4().hex)
    games = chadwick.games(event_path)
    with pytest.raises(FileNotFoundError):
        _ = chadwick.games_to_dataframe(games)


def test_game_to_csv(chadwick, team_events):
    for team_event in team_events:
        event_path = get_event_path(
            event_url(team_event)
        )
        games = chadwick.games(event_path)
        dfs = [chadwick.process_game_csv(game) for game in games]


def test_init_read_league(chadwick):
    file_path = get_event_path(event_url("TEAM1982"))
    _ = chadwick.cw_league_read(bytes(file_path, "utf8"))
