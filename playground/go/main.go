package main

import (
	"flag"
	"fmt"
	"math/rand/v2"
	"time"
)

func main() {
	min := 4
	max := 8

	minDur := flag.Duration("min", 4*time.Second, "Minimum pickup time")
	maxDur := flag.Duration("max", 8*time.Second, "Maximum pickup time")

	// Generates a random number in the range [min, max]
	// rand.IntN(n) returns a random number in the range [0, n).
	// To get an inclusive max, the range is max - min + 1.
	randomNumber := rand.IntN(max-min+1) + min
	fmt.Println("Random number between 4 and 8:", randomNumber)

	randomDuration := *minDur + time.Duration(rand.Int64N(int64(*maxDur-*minDur+1)))

	fmt.Println("Random number between 4 and 8:", randomDuration)
}
