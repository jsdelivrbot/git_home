// Some functions for manipulating containers.
package utils

import "sort"

// Mimics Python collections.Counter
func Counter(some_slice []int) map[int]int {
  counter := make(map[int]int)
  for _, x := range some_slice {
    counter[x]++
  }
  return counter
}

func SearchByValue(some_map map[int]int, target int, f func(int, int) bool) []int {
  result := []int{}
  for k, v := range some_map {
    if f(v, target) {
      result = append(result, k)
    }
  }
  return result
}

func Map2SliceByValue(some_map map[int]int, target int, f func(int, int) bool) []int {
  result := []int{}
  for k, v := range some_map {
    if f(v, target) {
      for i := 0; i < v; i++ {
        result = append(result, k)
      }
    }
  }
  return result
}

// Get max number.
func MaxInt(some_slice []int) int {
  current_max := some_slice[0]
  for _, v := range some_slice {
    if v > current_max {
      current_max = v
    }
  }
  return current_max
}

func FilterIntSlice(some_slice []int, f func(int) bool) []int {
  result := []int{}
  for _, x := range some_slice {
    if f(x) {
      result = append(result, x)
    }
  }
  return result
}

// Get the elements in A that are not in B.
func SliceDifference(A, B []int) []int {
  A_counter := Counter(A)
  B_counter := Counter(B)
  diff_counter := make(map[int]int)
  for key, val := range A_counter {
    diff_counter[key] = val - B_counter[key]
  }
  result := []int{}
  for key, val := range diff_counter {
    if val > 0 {
      for i := 1; i <= val; i++ {
        result = append(result, key)
      }
    }
  }
  return result
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
  combos := [][]int{}
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

func IntEqual(x, y int) bool {
  return x == y
}

func IntGreater(x, y int) bool {
  return x > y
}

func IntLess(x, y int) bool {
  return x < y
}

func IntGreaterEqual(x, y int) bool {
  return x >= y
}

func IntLessEqual(x, y int) bool {
  return x <= y
}
