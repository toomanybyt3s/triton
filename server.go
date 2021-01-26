package main

import (
	"net"
	"net/http"
	"time"

	"github.com/labstack/echo"
)

type apijsonServerhealth struct {
	health string `json:"health"`
}

type apijsonMsg struct {
	status string `json:"status"`
}

func main() {
	e := echo.New()
	e.GET("/", root)
	e.GET("/mc/:ip/:port", mc)
	e.Logger.Fatal(e.Start(":9090"))
}

func root(c echo.Context) error {
	msg := &apijsonServerhealth{
		health: "online",
	}
	return c.JSON(http.StatusOK, msg)
}

func mc(c echo.Context) error {
	ip := c.Param("ip")
	port := c.Param("port")
	timeout := time.Duration(1 * time.Second)
	_, err := net.DialTimeout("tcp", ip+":"+port, timeout)
	if err != nil {
		msg := &apijsonMsg{
			status: "down",
		}
		return c.JSON(http.StatusOK, msg)
	}
	msg := &apijsonMsg{
		status: "up",
	}
	return c.JSON(http.StatusOK, msg)
}
