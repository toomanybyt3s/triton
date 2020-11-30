package main

import (
	"fmt"
	"os/exec"
	"strings"

	"github.com/gofiber/fiber/v2"
)

func main() {
	app := fiber.New()

	app.Get("/", func(c *fiber.Ctx) error {
		return c.SendString("Hello, World 👋!")
	})

	app.Get("/mc/*", func(c *fiber.Ctx) error {
		ip := c.Params("*")
		out, _ := exec.Command("ping", ip, "-c 4", "-i 3", "-w 10").Output()
		if strings.Contains(string(out), "Destination Host Unreachable") {
			msg := fmt.Sprintf("Its down :(")
			return c.SendString(msg)
		}
		msg := fmt.Sprintf("IT'S ALIVEEE")
		return c.SendString(msg)
	})

	app.Listen(":9090")
}
