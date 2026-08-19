# --- Stage 1: Builder ---
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod ./
COPY . .
# Build a static binary without CGO dependencies
RUN CGO_ENABLED=0 GOOS=linux go build -o myapp .

# --- Stage 2: Minimal Runtime ---
FROM alpine:latest
# Run as a non-root user for security
RUN adduser -D appuser
USER appuser
WORKDIR /home/appuser

# Copy ONLY the compiled binary from Stage 1
COPY --from=builder /app/myapp .

CMD ["./myapp"]
