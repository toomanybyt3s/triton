FROM golang:latest

WORKDIR /cmd

COPY . .

RUN go build server.go

ENTRYPOINT [ "./server" ]