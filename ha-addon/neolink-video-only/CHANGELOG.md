# Changelog

## 0.1.2

- Download tested, prebuilt multi-architecture images instead of compiling on Home Assistant.
- Build and publish images using native amd64 and arm64 GitHub Actions runners.
- Retain the restored open-file limits and video-only default.

## 0.1.1

- Restore the upstream container's open-file limit (65535) for multiple RTSP streams.
- Keep the same pinned Neolink source and video-only behavior.

## 0.1.0

- Initial Home Assistant OS packaging with optional audio suppression.
