package main

import (
	"net"
	"net/http"
	"time"

	"github.com/labstack/echo"
)

type ApijsonServerhealth struct {
	Health string `json:"health"`
}

type ApijsonMsg struct {
	Status string `json:"status"`
}

func main() {
	e := echo.New()
	e.GET("/", root)
	e.GET("/mc/:ip/:port", mc)
	e.Logger.Fatal(e.Start(":9090"))
}

func root(c echo.Context) error {
	msg := &ApijsonServerhealth{
		Health: "online",
	}
	return c.JSON(http.StatusOK, msg)
}

func mc(c echo.Context) error {
	ip := c.Param("ip")
	port := c.Param("port")
	timeout := time.Duration(1 * time.Second)
	_, err := net.DialTimeout("tcp", ip+":"+port, timeout)
	if err != nil {
		msg := &ApijsonMsg{
			Status: "down",
		}
		return c.JSON(http.StatusOK, msg)
	}
	msg := &ApijsonMsg{
		Status: "up",
	}
	return c.JSON(http.StatusOK, msg)
}
