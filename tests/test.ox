define recursive(number) {
    if number > 0 {
        print(number)
        recursive(number - 1)   // calls parent *could* be function defintion scope
    }
}
recursive(6)