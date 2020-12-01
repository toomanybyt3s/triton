package main

import (
	"fmt"
	"net/http"
	"os/exec"
	"strings"

	"github.com/labstack/echo"
)

func main() {
	e := echo.New()
	e.GET("/", root)
	e.GET("/mc/:ip", mc)
	e.Logger.Fatal(e.Start(":9090"))
}

func root(c echo.Context) error {
	return c.String(http.StatusOK, "Hello, World 👋!")
}

func mc(c echo.Context) error {
	ip := c.Param("ip")
	out, _ := exec.Command("ping", ip, "-c 4", "-i 1", "-w 5").Output()
	if strings.Contains(string(out), "Destination Host Unreachable") {
		msg := fmt.Sprintf("Its down :(")
		return c.String(http.StatusOK, msg)
	}
	msg := fmt.Sprintf("IT'S ALIVEEE")
	return c.String(http.StatusOK, msg)
}
