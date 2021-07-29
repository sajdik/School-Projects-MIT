FROM golang:1.14.3-alpine

WORKDIR /src
COPY . .
RUN go build -o /bin/fetch cmd/fetch/main.go
