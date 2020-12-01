FROM golang:latest

WORKDIR /cmd

COPY . .

RUN go mod init example.com/example
RUN go mod tidy

RUN go build server.go

ENTRYPOINT [ "./server" ]