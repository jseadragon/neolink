"""Translate Supervisor options into a private Neolink configuration."""
import json
import os
from pathlib import Path


def make_config(options):
    quote = lambda value: json.dumps(str(value), ensure_ascii=True)
    lines = [f'bind = {quote(options.get("bind", "127.0.0.1"))}',
             f'bind_port = {int(options.get("bind_port", 8558))}']
    streams = {"Main": "mainStream", "Sub": "subStream", "Both": "both"}
    cameras = options.get("cameras", [])
    if not cameras:
        raise ValueError("Add at least one camera in the add-on Configuration tab.")
    names = [camera["name"] for camera in cameras]
    if len(names) != len(set(names)):
        raise ValueError("Camera names must be unique.")
    for camera in cameras:
        lines += ["", "[[cameras]]"]
        for key in ("name", "address", "username", "password"):
            lines.append(f'{key} = {quote(camera[key])}')
        lines += [f'stream = {quote(streams[camera.get("stream", "Main")])}',
                  'discovery = "local"', 'push_notifications = false']
    return "\n".join(lines) + "\n"


def main():
    options = json.loads(Path("/data/options.json").read_text())
    os.umask(0o077)
    config = Path("/data/neolink.toml")
    config.write_text(make_config(options))
    config.chmod(0o600)
    if options.get("disable_audio", True):
        os.environ["NEOLINK_DISABLE_AUDIO"] = "1"
    else:
        os.environ.pop("NEOLINK_DISABLE_AUDIO", None)
    os.environ["RUST_LOG"] = options.get("log_level", "info")
    os.execv("/usr/local/bin/neolink", ["neolink", "rtsp", "--config", str(config)])


if __name__ == "__main__":
    main()
