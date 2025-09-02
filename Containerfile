FROM rust:alpine as builder
WORKDIR /usr/src/pivert-server
COPY server .
RUN apk add --no-cache alpine-sdk
RUN cargo install --path .

FROM alpine:latest
COPY --from=builder /usr/local/cargo/bin/pivert-server /usr/local/bin/pivert-server
CMD ["pivert-server"]
