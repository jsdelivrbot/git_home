package main

import "fmt"
import "errors"
import "sort"

type options struct {
  hands map[string][]int
}

func SearchByValue(some_map map[int]int, target int, f func(int, int) bool) ([]int, error) {
  result := []int{}
  err := error(nil)
  for k, v := range some_map {
    if f(v, target) {
      result = append(result, k)
    }
  }
  if len(result) == 0 {
    err = errors.New("Not found")
  }
  return result, err
}

func CopyMap(original_map map[int]int) map[int]int {
  copy_map := make(map[int]int, len(original_map))
  for key, val := range original_map {
    copy_map[key] = val
  }
  return copy_map
}

func ChooseFrom(pool map[int]int, n int) [][]int {
  keys := []int{}
  for key, _ := range pool {
    keys = append(keys, key)
  }
  sort.Ints(keys)
  fmt.Println(keys)
  combos := [][]int{}
  // for i:= 0; i < len(keys); i++ {
  //   ChooseFromRecursion(pool, n, i, []int{}, keys, &combos)
  // }
  ChooseFromRecursion(pool, n, 0, []int{}, keys, &combos)
  return combos
}

func ChooseFromRecursion(pool map[int]int, n int, x int, cur []int, order []int, result *[][]int) {

  pool_copy := make(map[int]int)

  if len(cur) == n {
    *result = append(*result, cur)
    return
  }

  if x == len(order) {
    return
  }

  for i := x; i < len(order); i++ {
    if pool[order[i]] > 0 {
      pool_copy = CopyMap(pool)
      pool_copy[order[i]]--
      ChooseFromRecursion(pool_copy, n, i, append(cur, order[i]), order, result)
    }
  }
}

func ModifyMap(original_map map[int]int) {
  some_map := make(map[int]int, len(original_map))
  for key, val := range original_map {
    some_map[key] = val
  }
  for key, val := range some_map {
    some_map[key] = val * 2
  }
}

type State struct {
  Parent  *State
  Child   []*State
  Visited int
  Value   int
  Cards   []int
  Actions [][]int // Available actions
}

// Generate one simulation from current state to a terminal state.
// current_player is the player id that played action.
// func SimToEnd(current_player int, action []int, played []int, card_counts map[int]int, DECK []int) int {
//   if cards, err := card_counts[current_player]; err {
//     next_player := 0
//   } else {
//     next_player := current_player + 1
//   }
//   remaining := utils.SliceDifference(DECK, action)
//   remaining = utils.SliceDifference(remaining, played)
//   hand := RandomHand(remaining, card_counts[next_player])
//   options := FindOptions()
//
// }
func GetNewSlice(s []int) []int {
  s = append(s, s...)
  s = append(s, s...)
  return s
}

func F1(a int, b int) int {
  return a - b
}

func F2(a int, b int) int {
  return a + b
}

func F3(a int, b int) int {
  return a * b
}

func main() {
  o := make(map[string][]int)
  o["single"] = []int{1, 2, 3}
  fmt.Printf("Options are %v\n", o)
  s1 := []int{1, 2, 3}
  s2 := []int{4, 5, 6}
  s1 = append(s1, s2...)
  fmt.Println(s1)
  some_map := map[int]int{1: 1, 2: 2, 3: 3}
  fmt.Printf("Before modification the map is %+v\n", some_map)
  ModifyMap(some_map)
  fmt.Printf("After modification the map is %+v\n", some_map)
  pointer_to_map := &some_map
  fmt.Printf("Dereference the pointer to the map: %v\n", *pointer_to_map)
  fmt.Printf("Dereference the pointer to the map[1]: %v\n", (*pointer_to_map)[1])
  (*pointer_to_map)[1] = 100
  fmt.Printf("After changing the pointer, the original map is: %+v\n", some_map)
  combinations := ChooseFrom(some_map, 2)
  fmt.Println(combinations)
  fmt.Printf("Original slice: %v\n", s1)
  fmt.Printf("Now the slice is: %v\n", s1)
  func_array := []func(int, int) int{F1, F2, F3}
  for _, f := range func_array {
    fmt.Println(f(1, 2))
  }
  var some_state *State
  if some_state == nil {
    fmt.Println("The pointer is nil.")
  } else {
    fmt.Printf("The pointer is not nil. It is %p.\n", some_state)
  }
  another_map := make(map[int][]int)
  another_map[1] = []int{1,2,3}
  another_map[2] = []int{2,4,6}
  another_map[3] = []int{3,6,9}
  fmt.Printf("Now I have another map %+v\n", another_map)
  xxx := []int{100,200,300}
  another_map[1] = xxx
  fmt.Printf("I have changed value of '1' to xxx: %v, now the map is %+v\n", xxx, another_map)
  xxx[2] = 333
  fmt.Printf("Then I changed xxx[2] to 333, now the map is %+v, and xxx is %+v\n", another_map, xxx)
}
