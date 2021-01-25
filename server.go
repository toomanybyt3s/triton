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
	return c.JSON(http.StatusOK, {health: "online",})
}

func mc(c echo.Context) error {
	ip := c.Param("ip")
	port := c.Param("port")
	timeout := time.Duration(1 * time.Second)
	_, err := net.DialTimeout("tcp", ip+":"+port, timeout)
	if err != nil {
		return c.JSON(http.StatusOK, {status: "down",})
	}
	return c.JSON(http.StatusOK, {status: "up",})
}
