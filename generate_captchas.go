package main

import (
	"fmt"
	"os"
	"path"

	"github.com/dchest/captcha"
)

func main() {
	generateCaptchas(10, "./data/captchas/")
}

func generateCaptchas(count int, destinationDirectory string) {
	// Ensure the destination directory exists
	if err := os.MkdirAll(destinationDirectory, 0755); err != nil {
		panic(err)
	}

	for i := 0; i < count; i++ {
		captchaDigits := captcha.RandomDigits(6)
		captchaDummyId := "dummyId"
		captchaWidth := 120
		captchaHeight := 80
		captchaImage := captcha.NewImage(captchaDummyId, captchaDigits, captchaWidth, captchaHeight)
		captchaText := make([]byte, len(captchaDigits))
		for j, digit := range captchaDigits {
			captchaText[j] = digit + '0'
		}

		captchaFileName := fmt.Sprintf("%d_%s.png", i+1, string(captchaText))
		captchaFilePath := path.Join(destinationDirectory, captchaFileName)
		file, err := os.Create(captchaFilePath)
		if err != nil {
			panic(err)
		}
		defer file.Close()
		_, err = captchaImage.WriteTo(file)
		if err != nil {
			panic(err)
		}
	}
}
