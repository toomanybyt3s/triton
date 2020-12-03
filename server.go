package main

import (
	"fmt"
	"net"
	"net/http"
	"time"

	"github.com/labstack/echo"
)

func main() {
	e := echo.New()
	e.GET("/", root)
	e.GET("/mc/:ip/:port", mc)
	e.Logger.Fatal(e.Start(":9090"))
}

func root(c echo.Context) error {
	return c.String(http.StatusOK, "Hello, World 👋!")
}

func mc(c echo.Context) error {
	ip := c.Param("ip")
	port := c.Param("port")
	timeout := time.Duration(1 * time.Second)
	_, err := net.DialTimeout("tcp", ip+":"+port, timeout)
	if err != nil {
		msg := fmt.Sprintf("Its down :(")
		return c.String(http.StatusOK, msg)
	}
	msg := fmt.Sprintf("IT'S ALIVEEE")
	return c.String(http.StatusOK, msg)
}
