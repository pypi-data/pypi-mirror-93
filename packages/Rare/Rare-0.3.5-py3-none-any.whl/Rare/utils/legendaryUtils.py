import logging
import os
import subprocess

from PyQt5.QtCore import QProcess, QProcessEnvironment
from legendary.core import LegendaryCore

logger = logging.getLogger("LGD")
core = LegendaryCore()


def get_installed():
    return sorted(core.get_installed_list(), key=lambda name: name.title)


def get_installed_names():
    return [i.app_name for i in core.get_installed_list()]


def get_not_installed():
    games = []
    installed = get_installed_names()
    for game in get_games():
        if not game.app_name in installed:
            games.append(game)
    return games


# return (games, dlcs)
def get_games_and_dlcs():
    if not core.login():
        print("Login Failed")
        exit(1)
    return core.get_game_and_dlc_list()


def get_game_by_name(name: str):
    return core.get_game(name)


def get_games():
    if not core.login():
        print("Login Failed")
        return None

    return sorted(core.get_game_list(), key=lambda x: x.app_title)


def get_games_sorted():
    if not core.login():
        logging.error("No login")


def launch_game(app_name: str, lgd_core: LegendaryCore, offline: bool = False, skip_version_check: bool = False,
                username_override=None,
                wine_bin: str = None, wine_prfix: str = None, language: str = None, wrapper=None,
                no_wine: bool = os.name == "nt", extra: [] = None):
    game = lgd_core.get_installed_game(app_name)
    if not game:
        print("Game not found")
        return None
    if game.is_dlc:
        print("Game is dlc")
        return None
    if not os.path.exists(game.install_path):
        print("Game doesn't exist")
        return None

    if not offline:
        print("logging in")
        if not lgd_core.login():
            return None
        if not skip_version_check and not core.is_noupdate_game(app_name):
            # check updates
            try:
                latest = lgd_core.get_asset(app_name, update=True)
            except ValueError:
                print("Metadata doesn't exist")
                return None
            if latest.build_version != game.version:
                print("Please update game")
                return None
    params, cwd, env = lgd_core.get_launch_parameters(app_name=app_name, offline=offline,
                                                      extra_args=extra, user=username_override,
                                                      wine_bin=wine_bin, wine_pfx=wine_prfix,
                                                      language=language, wrapper=wrapper,
                                                      disable_wine=no_wine)
    process = QProcess()
    process.setWorkingDirectory(cwd)
    environment = QProcessEnvironment()
    for e in env:
        environment.insert(e, env[e])
    process.setProcessEnvironment(environment)
    process.start(params[0], params[1:])
    return process


def get_updates():
    update_games = []
    for game in core.get_installed_list():
        update_games.append(game) if get_game_by_name(game.app_name).app_version != game.version else None
    return update_games


def logout():
    core.lgd.invalidate_userdata()


def install(app_name: str, path: str = None):
    subprocess.Popen(f"legendary -y install {app_name}".split(" "))
    # TODO


def login(sid):
    code = core.auth_sid(sid)
    if code != '':
        return core.auth_code(code)
    else:
        return False


def get_name():
    return core.lgd.userdata["displayName"]


def uninstall(app_name: str, core):
    igame = core.get_installed_game(app_name)
    try:
        # Remove DLC first so directory is empty when game uninstall runs
        dlcs = core.get_dlc_for_game(app_name)
        for dlc in dlcs:
            if (idlc := core.get_installed_game(dlc.app_name)) is not None:
                logger.info(f'Uninstalling DLC "{dlc.app_name}"...')
                core.uninstall_game(idlc, delete_files=True)

        logger.info(f'Removing "{igame.title}" from "{igame.install_path}"...')
        core.uninstall_game(igame, delete_files=True, delete_root_directory=True)
        logger.info('Game has been uninstalled.')

    except Exception as e:
        logger.warning(f'Removing game failed: {e!r}, please remove {igame.install_path} manually.')


def import_game(core: LegendaryCore, app_name: str, path: str):
    logger.info("Import " + app_name)
    igame = core.get_game(app_name)
    manifest, jgame = core.import_game(igame, path)
    exe_path = os.path.join(path, manifest.meta.launch_exe.lstrip('/'))
    total = len(manifest.file_manifest_list.elements)
    found = sum(os.path.exists(os.path.join(path, f.filename))
                for f in manifest.file_manifest_list.elements)
    ratio = found / total
    if not os.path.exists(exe_path):
        logger.error(f"Game {igame.app_title} failed to import")
        return False
    if ratio < 0.95:
        logger.error(
            "Game files are missing. It may be not the lates version ore it is corrupt")
        return False
    core.install_game(jgame)
    if jgame.needs_verification:
        logger.info(logger.info(
            f'NOTE: The game installation will have to be verified before it can be updated '
            f'with legendary. Run "legendary repair {app_name}" to do so.'))

    logger.info("Successfully imported Game: " + igame.app_title)
    return True
