# Neolink Video Only for Home Assistant OS

An experimental add-on that builds this fork's video-only workaround from a
pinned source revision. Supports amd64 and aarch64. The first installation
compiles Neolink on the Home Assistant machine and can take several minutes.

## Install

1. Stop any other Neolink instance that connects to the same cameras.
2. In Settings > Add-ons > Add-on Store > Repositories, add:
   `https://github.com/jseadragon/neolink#video-only-audio-workaround`
3. Install **Neolink Video Only**.
4. Add your cameras in the Configuration tab. Each needs a unique name,
   address (`camera-host:9000`), username, and password. Use Main for full quality.
5. Leave `disable_audio: true`, save, and start the add-on.
6. Check Logs for camera login and stream availability.

## Streams and local access

With the default loopback binding and host networking, Home Assistant and
host-networked apps such as Scrypted can use:

`rtsp://127.0.0.1:8558/<camera-name>/main`

Set RTSP transport to TCP in consumers. The default binding keeps RTSP off the
LAN. This add-on does not configure RTSP authentication, so changing `bind` to
`0.0.0.0` makes streams accessible to other devices that can reach the host.

## Options

- `bind`: listening address; defaults to loopback.
- `bind_port`: defaults to 8558 to avoid other RTSP servers.
- `disable_audio`: true omits audio; false restores upstream audio handling,
  including any existing decoder incompatibilities.
- `log_level`: error, warn, info, or debug.
- `cameras`: name, address, username, password, and optional stream
  (Main, Sub, or Both).

Camera credentials remain in Supervisor options and a private generated config;
they are not printed by the launcher. Keep Home Assistant backups private.
This package has no web interface; use the Home Assistant dashboard or Scrypted.
