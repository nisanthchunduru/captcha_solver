package main

import (
	"os"

	"github.com/dchest/captcha"
)

func main() {
	// Create a new captcha with digits and letters of length 6
	captchaText := captcha.NewLen(6)

	// Save the captcha image to a file
	file, err := os.Create("dchest_example_captcha.png")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	// Write the captcha image to the file
	err = captcha.WriteImage(file, captchaText, 240, 80)
	if err != nil {
		panic(err)
	}
}
