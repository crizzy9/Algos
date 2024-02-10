package main

import (
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
)

func main() {
	content := readFileInput("aoc/day2_full_input.txt")
	// content := readFileInput("aoc/day2_input.txt")
	games := strings.Split(strings.TrimSpace(string(content)), "\n")

	// input := map[string]int { "red":12, "green": 13, "blue": 14 }
	//
	// invalidGames := []int{}
	powCubes := []int{}

	for _, game := range games {
		igame := strings.Split(game, ":")[1]
		// fmt.Println(i, igame)
		minCubes := map[string]int { "red":0, "green": 0, "blue": 0 }

		for _, c := range strings.Split(igame, ";") {
			for _, item := range strings.Split(c, ",") {
				it := strings.Split(strings.TrimSpace(item), " ")
				num, color := it[0], it[1]
				n, _ := strconv.Atoi(num);
				// part 1: check against input and mark invalids
				// if input[color] < int(n) {
				// 	invalidGames = append(invalidGames, i+1)
				// 	goto out
				// }
				// part 2: get minimum num cubes required
				if n > minCubes[color] {
					minCubes[color] = n
				}
			}
		}
		// out:
		powCubes = append(powCubes, minCubes["red"]*minCubes["green"]*minCubes["blue"])
	}

	// fmt.Println(invalidGames)
	// gamelen := len(games)
	// out := ((gamelen + 1)*gamelen/2) - sumArr(invalidGames)
	// fmt.Println(out)

	fmt.Println(sumArr(powCubes))

}

func sumArr(arr []int) (s int) {
	s = 0
	for _, a := range arr {
		s += a
	}
	return 
}

func readFileInput(filename string) (content []byte) {
	file, err := os.Open(filename)
	if err != nil {
		fmt.Println("Error opening file: ", err)
	}
	defer file.Close()

	content, err = io.ReadAll(file)
	if err != nil {
		fmt.Println("Error while reading: ", err)
	}

	return content
}

