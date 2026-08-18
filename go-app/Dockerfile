# Stage 1: Build binary
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod ./
COPY main.go ./
RUN CGO_ENABLED=0 GOOS=linux go build -o app .

# Stage 2: Production runtime (minimal image ~5-10MB)
FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/app .
CMD ["./app"]
