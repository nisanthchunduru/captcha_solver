package main

import (
	"fmt"
	"os"
	"path"
	"path/filepath"
	"strconv"
	"strings"

	"github.com/dchest/captcha"
)

func main() {
	if len(os.Args) < 3 {
		fmt.Println("Usage: go run generate_captchas.go <count> <destination_directory>")
		os.Exit(1)
	}

	count, err := strconv.Atoi(os.Args[1])
	if err != nil {
		fmt.Println("Please provide the number of captchas you'd like to generate as the first argument")
		os.Exit(1)
	}

	destinationDirectory := filepath.Clean(os.Args[2])

	generateCaptchas(count, destinationDirectory)
}

func generateCaptchas(count int, destinationDirectory string) {
	if err := os.MkdirAll(destinationDirectory, 0755); err != nil {
		panic(err)
	}

	startIndex := findStartIndex(destinationDirectory)

	for i := startIndex; i < count; i++ {
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

func findStartIndex(destinationDirectory string) int {
	files, err := os.ReadDir(destinationDirectory)
	if err != nil {
		panic(err)
	}

	maxIndex := 0
	for _, file := range files {
		name := file.Name()
		if strings.HasSuffix(name, ".png") {
			parts := strings.Split(name, "_")
			if len(parts) > 0 {
				index, err := strconv.Atoi(parts[0])
				if err == nil && index > maxIndex {
					maxIndex = index
				}
			}
		}
	}
	return maxIndex
}
