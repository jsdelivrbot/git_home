// This program plays poker.
// The first one plays out the hand wins.
// N cards are hidden from the players.
// Legal moves are:
//     1) Single card
//     2) Double
//     3) 5 or more consecutive singles
//     4) 3 or more consecutive doubles
//     5) Triple with either a single or a double
//     6) 2 or more consecutive triples
//     7) Bomb (4 same value cards)
//     8) Jet (4 same value cards with any two cards)
package main

import "fmt"

import "log"
import "time"
import "math/rand"
import "math"
import "sort"
import "errors"
import "strconv"
import "utils"

func InitCardValues() map[int]string {
  CardValues := make(map[int]string, 15)
  for i := 1; i < 9; i++ {
    CardValues[i] = strconv.Itoa(i + 2)
  }
  CardValues[9] = "J"
  CardValues[10] = "Q"
  CardValues[11] = "K"
  CardValues[12] = "A"
  CardValues[13] = "2"
  CardValues[14] = "joker"
  CardValues[15] = "Joker"
  return CardValues
}

// Create n full deck(s)
func GetNewDeck(n int) []int {
  // Initialize a single deck
  base_deck := []int{14, 15}
  for i := 1; i < 14; i++ {
    for j := 1; j <= 4; j++ {
      base_deck = append(base_deck, i)
    }
  }
  var deck []int
  for i := 0; i < n; i++ {
    deck = append(deck, base_deck...)
  }
  return deck
}

// Distribute cards to players.
func Deal(P, N int) ([]int, map[int][]int) {
  var deck []int = GetNewDeck(1)
  // Shuffle the sorted deck
  rand.Seed(42)
  shuffle_index := rand.Perm(len(deck))
  var deck_random []int
  for _, x := range shuffle_index {
    deck_random = append(deck_random, deck[x])
  }
  hide_out := deck_random[:N]
  sort.Ints(hide_out)

  player_decks := make(map[int][]int)
  p := int(0)
  for _, c := range deck_random[N:] {
    player_decks[p] = append(player_decks[p], c)
    p++
    p = p % P
  }

  for k, _ := range player_decks {
    sort.Ints(player_decks[k])
  }

  return hide_out, player_decks
}

// Description of a Hand
type Hand struct {
  Cards  []int
  Shape  string
  Length int
  Value  int
}

// Find consecutive cards with minimum length.
func FindConsecutiveCards(cards []int, min_len int) ([][]int, error) {
  err := error(nil)
  var result [][]int
  if len(cards) < min_len {
    err = errors.New("No hand found!")
    return result, err
  }

  cards_copy := make([]int, len(cards))
  copy(cards_copy, cards)
  sort.Ints(cards_copy)

  // Here to implement a code that finds consecutive numbers.
  // Do recursion.
  cur := []int{}
  for i := 0; i < len(cards); i++ {
    FindConsecutiveCardsRecursion(cards_copy, min_len, &result, cur, i)
  }
  if len(result) == 0 {
    err = errors.New("No hand found!")
  }
  return result, err
}

func FindConsecutiveCardsRecursion(cards []int, min_len int, result *[][]int, cur []int, i int) {
  if len(cur) == 0 || cards[i]-1 == cur[len(cur)-1] {
    cur = append(cur, cards[i])
  }
  if len(cur) >= min_len {
    *result = append(*result, cur)
  }
  if i == len(cards)-1 || cards[i+1]-cards[i] != 1 {
    return
  }
  FindConsecutiveCardsRecursion(cards, min_len, result, cur, i+1)
}

func ThreeToAce(card int) bool {
  return card >= 1 && card <= 12
}

func ComposeSingle(cards []int) []Hand {
  options := []Hand{}
  selection := []int{} // Useful when the hand is more than 1 card.
  var shape string     // {"single", "double", "singles", "doubles", "triple-singles", "triple-doubles", "bomb", "jet"}
  var length int
  var value int
  var hand Hand
  cards_counter := utils.Counter(cards) // Count each card
  for card, _ := range cards_counter {
    selection = []int{card}
    shape = "single"
    length = 1
    value = card
    hand = Hand{selection, shape, length, value}
    options = append(options, hand)
  }
  return options
}

func ComposeSingles(cards []int) []Hand {
  options := []Hand{}
  var shape string // {"single", "double", "singles", "doubles", "triple-singles", "triple-doubles", "bomb", "jet"}
  var length int
  var value int
  var hand Hand
  cards_counter := utils.Counter(cards) // Count each card
  // Find singles hand.
  singles := utils.FilterIntSlice(utils.SearchByValue(cards_counter, 1, utils.IntGreaterEqual), ThreeToAce)
  combos, err := FindConsecutiveCards(singles, 5)
  if err == nil {
    for _, combo := range combos {
      shape = "singles"
      length = len(combo)
      value = utils.MaxInt(combo)
      hand = Hand{combo, shape, length, value}
      options = append(options, hand)
    }
  }
  return options
}

func ComposeDouble(cards []int) []Hand {
  options := []Hand{}
  selection := []int{} // Useful when the hand is more than 1 card.
  var shape string     // {"single", "double", "singles", "doubles", "triple-singles", "triple-doubles", "bomb", "jet"}
  var length int
  var value int
  var hand Hand
  cards_counter := utils.Counter(cards) // Count each card
  for _, card := range utils.SearchByValue(cards_counter, 2, utils.IntGreaterEqual) {
    selection = []int{card, card}
    shape = "double"
    length = 1
    value = card
    hand = Hand{selection, shape, length, value}
    options = append(options, hand)
  }
  return options
}

func ComposeDoubles(cards []int) []Hand {
  options := []Hand{}
  selection := []int{} // Useful when the hand is more than 1 card.
  var shape string     // {"single", "double", "singles", "doubles", "triple-singles", "triple-doubles", "bomb", "jet"}
  var length int
  var value int
  var hand Hand
  cards_counter := utils.Counter(cards) // Count each card
  // Find doubles hand.
  doubles := utils.SearchByValue(cards_counter, 2, utils.IntGreaterEqual)
  combos, err := FindConsecutiveCards(doubles, 3)
  if err == nil {
    for _, combo := range combos {
      selection = []int{}
      for _, card := range combo {
        selection = append(selection, []int{card, card}...)
      }
      shape = "doubles"
      length = len(combo)
      value = utils.MaxInt(combo)
      hand = Hand{selection, shape, length, value}
      options = append(options, hand)
    }
  }
  return options
}

func ComposeTripleSingles(cards []int) []Hand {
  options := []Hand{}
  selection := []int{} // Useful when the hand is more than 1 card.
  var hand Hand
  cards_counter := utils.Counter(cards) // Count each card
  // Find triple-single(s) and triple-double(s)
  triples := utils.SearchByValue(cards_counter, 3, utils.IntGreaterEqual)
  combos, err := FindConsecutiveCards(triples, 1)
  selection_placeholder := []int{}
  remaining_cards := make(map[int]int)
  if err == nil {
    for _, combo := range combos {
      selection = []int{}
      for _, card := range combo {
        selection = append(selection, []int{card, card, card}...)
      }
      remaining_cards = utils.Counter(utils.SliceDifference(cards, selection))
      minor_singles := utils.ChooseFrom(remaining_cards, len(combo))
      for _, single := range minor_singles {
        selection_placeholder = make([]int, len(selection))
        copy(selection_placeholder, selection)
        hand = Hand{append(selection_placeholder, single...), "triple-singles", len(combo), utils.MaxInt(combo)}
        options = append(options, hand)
      }
    }
  }
  return options
}

func ComposeTripleDoubles(cards []int) []Hand {
  options := []Hand{}
  selection := []int{} // Useful when the hand is more than 1 card.
  var hand Hand
  cards_counter := utils.Counter(cards) // Count each card
  // Find triple-single(s) and triple-double(s)
  triples := utils.SearchByValue(cards_counter, 3, utils.IntGreaterEqual)
  combos, err := FindConsecutiveCards(triples, 1)
  selection_placeholder := []int{}
  remaining_cards := make(map[int]int)
  if err == nil {
    for _, combo := range combos {
      selection = []int{}
      for _, card := range combo {
        selection = append(selection, []int{card, card, card}...)
      }
      remaining_cards = utils.Counter(utils.SliceDifference(cards, selection))
      double_candidates := make(map[int]int) // map[Card]pairs
      for _, card := range utils.SearchByValue(remaining_cards, 2, utils.IntGreaterEqual) {
        double_candidates[card] = remaining_cards[card] / 2
      }
      minor_doubles := utils.ChooseFrom(double_candidates, len(combo))
      for _, double := range minor_doubles {
        selection_placeholder = make([]int, len(selection))
        copy(selection_placeholder, selection)
        double = append(double, double...)
        sort.Ints(double)
        hand = Hand{append(selection_placeholder, double...), "triple-doubles", len(combo), utils.MaxInt(combo)}
        options = append(options, hand)
      }
    }
  }
  return options
}

func ComposeBomb(cards []int) []Hand {
  options := []Hand{}
  selection := []int{} // Useful when the hand is more than 1 card.
  var shape string     // {"single", "double", "singles", "doubles", "triple-singles", "triple-doubles", "bomb", "jet"}
  var length int
  var value int
  var hand Hand
  cards_counter := utils.Counter(cards) // Count each card
  // Find bomb
  for _, card := range utils.SearchByValue(cards_counter, 4, utils.IntEqual) {
    selection = []int{card, card, card, card}
    shape = "bomb"
    length = 1
    value = card
    hand = Hand{selection, shape, length, value}
    options = append(options, hand)
  }
  return options
}

func ComposeJet(cards []int) []Hand {
  options := []Hand{}
  var hand Hand
  // Find jet
  bombs := ComposeBomb(cards)
  for _, bomb_hand := range bombs {
    for _, minors := range utils.ChooseFrom(utils.Counter(utils.SliceDifference(cards, bomb_hand.Cards)), 2) {
      hand = Hand{append(bomb_hand.Cards, minors...), "jet", 1, bomb_hand.Value}
      options = append(options, hand)
    }
  }
  return options
}

// The cards to beat on the table
type Target struct {
  player int // the id of the player who played the hand
  hand   Hand
}

// Compose options based on the best hand on table
// cards: current player's deck
// id: current player's id
// target: current best hand on table
func ComposeOptions(cards []int, id int, target Target) []Hand {
  options := []Hand{}
  candidates := []Hand{}
  var opponent Hand

  if id == target.player {
    opponent = Hand{Cards: []int{}, Shape: "empty", Value: 0, Length: 0}
  } else {
    opponent = target.hand
  }

  // Bomb is always useful unless there is a bigger bomb on table
  bombs := ComposeBomb(cards)
  for _, bomb := range bombs {
    if !(opponent.Shape == "bomb" && opponent.Value >= bomb.Value) {
      options = append(options, bomb)
    }
  }

  if opponent.Shape == "single" || opponent.Shape == "empty" {
    candidates = append(candidates, ComposeSingle(cards)...)
  }
  if opponent.Shape == "singles" || opponent.Shape == "empty" {
    candidates = append(candidates, ComposeSingles(cards)...)
  }
  if opponent.Shape == "double" || opponent.Shape == "empty" {
    candidates = append(candidates, ComposeDouble(cards)...)
  }
  if opponent.Shape == "doubles" || opponent.Shape == "empty" {
    candidates = append(candidates, ComposeDoubles(cards)...)
  }
  if opponent.Shape == "triple-singles" || opponent.Shape == "empty" {
    candidates = append(candidates, ComposeTripleSingles(cards)...)
  }
  if opponent.Shape == "triple-doubles" || opponent.Shape == "empty" {
    candidates = append(candidates, ComposeTripleDoubles(cards)...)
  }
  if opponent.Shape == "jet" || opponent.Shape == "empty" {
    candidates = append(candidates, ComposeJet(cards)...)
  }

  for _, candidate := range candidates {
    if candidate.Length == opponent.Length && candidate.Value > opponent.Value ||
      opponent.Shape == "empty" {
      options = append(options, candidate)
    }
  }

  if id != target.player {
    empty_hand := Hand{[]int{}, "empty", 0, 0}
    options = append(options, empty_hand)
  }

  return options
}

// Reduce hand by played cards.
func ReduceHand(cards, played []int) []int {
  return utils.SliceDifference(cards, played)
}

type State struct {
  Parent  *State
  Child   []State
  Visited int
  Value   float64
  Cards   []int
  Actions []Hand // Available actions
}

// Calculate Upper Confidence Bound
// state must not be nil and must have been visited
func (state *State) GetUCB() float64 {
  var ucb float64
  var root *State
  // Find the total simulations at root
  root = state.Parent
  for {
    if root.Parent != nil {
      root = root.Parent
    } else {
      break
    }
  }
  ucb = float64(state.Value)/float64(state.Visited) +
    math.Sqrt(2*math.Log(float64(root.Visited))/float64(state.Visited))
  return ucb
}

// Simulate future plays using Monte Carlo Tree Search
// deck: current player's cards
// id: current player id
// target: the best hand on the table
// played: played cards so far
// counts: number of cards of each player
// max_iters: total iterations in MCTS
func MCTS(deck []int, id int, target Target, played []int, counts []int, max_iters int) Hand {
  start_time := time.Now()
  fmt.Printf("Start at %v\n", start_time)
  var DECK []int = GetNewDeck(1)
  // Winning early is better.
  var DISCOUNT float64 = 0.99
  // Initialize the current state as the root of MCTS
  CurrentState := State{
    Parent:  nil,
    Child:   []State{},
    Visited: 1,
    Value:   -1,
    Cards:   deck,
    Actions: []Hand{},
  }
  // Only the actions are deterministic
  CurrentState.Actions = append(CurrentState.Actions, ComposeOptions(deck, id, target)...)
  var ChildState State
  // Initialize immediate children
  for _, action := range CurrentState.Actions {
    ChildState = State{
      Parent:  &CurrentState,
      Child:   []State{},
      Visited: 0,
      Value:   0,
      Cards:   ReduceHand(deck, action.Cards),
      Actions: []Hand{},
    }
    CurrentState.Child = append(CurrentState.Child, ChildState)
    // fmt.Printf("Child node: %+v\n", ChildState.Cards)
  }
  var next_player int = id + 1
  if next_player >= len(counts) {
    next_player = 0
  }
  var new_target Target
  var new_played []int
  var new_counts []int
  // Start doing MCTS...
  // Simulate from each child that is not visited or has the highest value
  var StartChild *State
  var GoodChildren []*State
  var StartAction Hand
  var GoodActions []Hand
  var best_ucb float64
  var random_index int
  cards := make(map[int][]int)
  for iter := 0; iter < max_iters; iter++ {
    // Find the highest UCB child or the first unvisited child.
    best_ucb = -1
    StartChild = nil
    GoodChildren = []*State{}
    for cid, child := range CurrentState.Child {
      // Visit each child for at least N times before making selection
      // based on UCB score.
      if child.Visited <= 30 {
        StartChild = &CurrentState.Child[cid]
        StartAction = CurrentState.Actions[cid]
        break
      } else if len(GoodChildren) == 0 || child.GetUCB() > best_ucb {
        best_ucb = child.GetUCB()
        GoodChildren = []*State{&CurrentState.Child[cid]}
        GoodActions = []Hand{CurrentState.Actions[cid]}
      } else if child.GetUCB() == best_ucb {
        GoodChildren = append(GoodChildren, &CurrentState.Child[cid])
        GoodActions = append(GoodActions, CurrentState.Actions[cid])
      }
    }
    if StartChild == nil {
      // Break tie
      random_index = rand.Intn(len(GoodChildren))
      StartChild = GoodChildren[random_index]
      StartAction = GoodActions[random_index]
    }
    StartChild.Visited += 1
    CurrentState.Visited += 1
    if len(StartChild.Cards) == 0 {
      // Early return if no more card is left then win
      return StartAction
    }
    new_target = target
    if StartAction.Shape != "empty" {
      new_target = Target{player: id, hand: StartAction}
    }
    new_played = make([]int, len(played))
    copy(new_played, played)
    new_played = append(new_played, StartAction.Cards...)
    new_counts = make([]int, len(counts))
    cards = make(map[int][]int)
    for _, card := range StartChild.Cards {
      cards[id] = append(cards[id], card)
    }
    copy(new_counts, counts)
    new_counts[id] = len(StartChild.Cards)
    if len(cards[id]) != new_counts[id] {
      fmt.Printf("Counts: %v, Cards: %+v\n", new_counts, cards)
      log.Fatal("Inconsistent cards.")
    }
    winner, depth := ExpandTree(new_target, new_played, new_counts, &cards, next_player, &DECK, 0)
    if winner == id {
      StartChild.Value += 1*math.Pow(DISCOUNT, depth)
    }
  }

  var max_ucb float64 = -1
  var BestAction []Hand
  for cid, child := range CurrentState.Child {
    fmt.Printf("Child %v --- action: %v --- visited: %v --- value: %v --- prob: %v --- UCB: %v\n",
      cid, CurrentState.Actions[cid], child.Visited, child.Value,
      float32(child.Value)/float32(child.Visited), child.GetUCB())
    if child.Value > CurrentState.Value {
      CurrentState.Value = child.Value
    }
    if child.GetUCB() > max_ucb {
      BestAction = []Hand{CurrentState.Actions[cid]}
      max_ucb = child.GetUCB()
    } else if child.GetUCB() == max_ucb {
      BestAction = append(BestAction, CurrentState.Actions[cid])
    }
  }

  finish_time := time.Now()
  fmt.Printf("Using time: %v\n", finish_time.Sub(start_time))
  fmt.Printf("Best UCB: %v\n", max_ucb)
  // If there is a tie then pick one randomly
  return BestAction[rand.Intn(len(BestAction))]
}

// Expand search tree to a leaf.
// The starting point has known
//   1) best hand on table -> target
//   2) played cards by far -> played
//   3) card counts for each player -> counts
//   4) the next player to play -> id (starting from 0)
// DECK: all cards
// depth: recursion depth
// Return: winner id
func ExpandTree(target Target, played []int, counts []int, cards *map[int][]int, id int, DECK *[]int, depth float64) (winner int, end_depth float64) {
  // Initialize the current player's hand
  if len((*cards)[id]) != counts[id] {
    var card_pool []int = utils.SliceDifference(*DECK, played)
    var random_order []int = rand.Perm(len(card_pool))
    for i := 0; i < counts[id]; i++ {
      (*cards)[id] = append((*cards)[id], card_pool[random_order[i]])
    }
  }
  // fmt.Printf("Player %v cards %v\n", id, (*cards)[id])
  var options []Hand = ComposeOptions((*cards)[id], id, target)
  var option Hand = options[rand.Intn(len(options))]
  (*cards)[id] = ReduceHand((*cards)[id], option.Cards)
  if len((*cards)[id]) == 0 {
    // Return the current player's id if no card is left.
    return id, depth
  } else {
    // Otherwise do recursion until someone wins.
    var next_player int = id + 1
    if next_player >= len(counts) {
      next_player = 0
    }
    new_played := make([]int, len(played))
    copy(new_played, played)
    new_played = append(new_played, option.Cards...)
    // new_counts := make([]int, len(counts))
    // copy(new_counts, counts)
    counts[id] = len((*cards)[id])
    var new_target Target = target
    if option.Shape != "empty" {
      new_target = Target{player: id, hand: option}
    }
    return ExpandTree(new_target, new_played, counts, cards, next_player, DECK, depth+1)
  }
}

// Human friendly format of hand
func PrintHand(hand Hand){
  if hand.Shape == "empty" {
    fmt.Println("Pass...")
  } else {
    value_map := InitCardValues()
    for _, card := range hand.Cards {
      fmt.Printf("%v ", value_map[card])
    } 
    fmt.Println("")
  }
}
func main() {
  // hidden_deck, player_decks := Deal(3, 2)
  // fmt.Printf("The hidden deck is %v\n", hidden_deck)
  // fmt.Printf("The players's decks are %+v\n", player_decks)
  // rand.Seed(42)
  // own_deck := player_decks[int(rand.Intn(len(player_decks)))]
  // fmt.Printf("Own deck is %v\n", own_deck)
  // card_values := InitCardValues()
  // fmt.Printf("Card values: %v\n", card_values)
  // some_slice := []int{1, 1, 1, 2, 2, 3}
  // some_slice_counter := utils.Counter(some_slice)
  // fmt.Printf("Counter of %v is %v\n", some_slice, some_slice_counter)
  // result := [][]int{}
  // cards := []int{1, 2, 3, 5, 6, 7, 8, 9}
  // cur := []int{}
  // for i := 0; i < len(cards); i++ {
  //   FindConsecutiveCardsRecursion(cards, 4, &result, cur, i)
  // }
  // fmt.Printf("Result is %v\n", result)
  // opp := Hand{Cards: []int{2, 2, 3, 3, 4, 4}, Shape: "doubles", Length: 3, Value: 4}
  // target := Target{player: 0, hand: opp}
  // options := ComposeOptions(own_deck, 1, target)
  // fmt.Printf("Options are %+v\n", options)
  // fmt.Println(ComposeOptions([]int{1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5}, 1, target))
  // opponent := Hand{Cards: []int{1, 1, 1, 4}, Shape: "triple-singles", Length: 1, Value: 1}
  // target = Target{player: 0, hand: opponent}
  // found_options := ComposeOptions([]int{1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4}, 1, target )
  // fmt.Println(found_options)

  deck := []int{1,2,3,3,4,4,5,6,6,7,8,8,9,9,9,10,11,11,12,12,12,13,13}
  fmt.Printf("Remaining cards: %v\n", len(deck))
  played := []int{}
  target := Target{player: 1, hand: Hand{Cards: []int{}, Shape: "empty", Length: 0, Value: 0}}
  choice := MCTS(deck, 1, target, played, []int{46-len(deck)-len(played), len(deck)}, 1000000)
  fmt.Printf("When iteration is %v the choice is: %+v.\n", 1000000, choice)
  PrintHand(choice)
  // options := ComposeOptions(deck, 1, target)
  // fmt.Println(options)
  // var full_deck []int = GetNewDeck(1)
  // fmt.Println(len(utils.ChooseFrom(utils.Counter(utils.SliceDifference(full_deck, deck)), 23)))
}
