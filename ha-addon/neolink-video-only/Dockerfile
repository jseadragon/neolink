FROM rust:1.85-bookworm AS builder
RUN apt-get update && apt-get install -y --no-install-recommends libgstrtspserver-1.0-dev libgstreamer1.0-dev protobuf-compiler
WORKDIR /src
# Pin the reviewed video-only implementation; add-on packaging updates separately.
RUN git init . && git remote add origin https://github.com/jseadragon/neolink.git && git fetch --depth 1 origin 4d50e39d88328e0c7495166c1110c08732bc53ba && git checkout FETCH_HEAD
ENV CARGO_BUILD_JOBS=2
RUN cargo build --locked --release
FROM quantumentangledandy/neolink:latest
RUN apt-get update && apt-get install -y --no-install-recommends python3 && rm -rf /var/lib/apt/lists/*
COPY --from=builder /src/target/release/neolink /usr/local/bin/neolink
COPY run.py /run.py
ENTRYPOINT ["python3", "/run.py"]
CMD []
