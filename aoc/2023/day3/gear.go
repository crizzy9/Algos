package main

import (
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
)

func main() {
    part1()
}

func part1() {
    content := readFileInput("aoc/day3/full_input.txt")
    // fmt.Println(string(content))
	schematics := strings.Split(strings.TrimSpace(string(content)), "\n")

    nums := []string{}
    
    for i, line := range schematics {
        // fmt.Println(i, line)

        var num_start, num_end int = -1, -1
        var curr_num string

        for j := range line {
            c := string(line[j])

            if isNum(c) {
                curr_num += c
                if num_start == -1 {
                    num_start = j
                }
                if j == len(line) - 1 || !isNum(string(line[j+1])) {
                    num_end = j
                }

                symbols := "@#$%&*-+=/"
                // symbols2 := "%/=@+$*-#&"
                if num_start >= 0 && num_end >= 0 {
                    // fmt.Println("num:", curr_num, "start:", num_start, "end:", num_end)
                    // fmt.Println("i", i, "len", len(schematics), "j", j, "len-line", len(line))
                    // fmt.Println("line:", line)
                    var start int
                    var end int

                    if num_start > 0 {
                        start = num_start - 1
                    } else {
                        start = num_start
                    }

                    if num_end != len(line) - 1 {
                        end = num_end + 1
                    } else {
                        end = num_end
                    }

                    if i < len(schematics) - 1 && strings.ContainsAny(string(schematics[i+1][start:end+1]), symbols) {
                        // check_down := string(schematics[i+1][start:end+1])
                        // fmt.Println("down:", check_down)
                        // fmt.Println("start:", start, "end:", end+1)
                        // if strings.ContainsAny(check_down, symbols) {
                        //     nums = append(nums, curr_num)
                        // }
                        // fmt.Println("down:", string(schematics[i+1][start:end+1]))
                        nums = append(nums, curr_num)
                    } else if i != 0 && strings.ContainsAny(string(schematics[i-1][start:end+1]), symbols) {
                        // check_up := string(schematics[i-1][start:end+1])
                        // fmt.Println("up:", check_up)
                        // fmt.Println("start:", start, "end:", end+1)
                        // if strings.ContainsAny(check_up, symbols) {
                        //     nums = append(nums, curr_num)
                        // }
                        // fmt.Println("up:", string(schematics[i-1][start:end+1]))
                        nums = append(nums, curr_num)
                    } else if start > 0 && strings.ContainsAny(string(line[start]), symbols) {
                        // fmt.Println("left:", string(line[j-1]))
                        nums = append(nums, curr_num)
                    } else if end < len(line)-1 && strings.ContainsAny(string(line[end]), symbols) {
                        // fmt.Println("right:", string(line[j+1]))
                        nums = append(nums, curr_num)
                    }
                    num_start, num_end = -1, -1
                    curr_num = ""
                }
            }
        }
    }

    fmt.Println(nums)
    fmt.Println(sumArr(nums))
}

func isNum(char string) bool {
    return char >= "0" && char <= "9"
}

func sumArr(arr []string) (s int) {
	s = 0
	for _, a := range arr {
        n, err := strconv.Atoi(a)
        if err != nil {
            fmt.Println("Error converting to int: ", err)
        }
		s += n
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
