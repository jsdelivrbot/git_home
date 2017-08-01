float IntegerProgramming(objective, constraints){
    auto start = lp(objective, constraints)
    if (start.boundary == int(start.boundary)){
        return start.val;
    }
    else {
        return IntegerProgrammingHelper(objective, constraints, start);
    }
}

float IntegerProgrammingHelper(objective, constraints, starting_point){
    auto new_constraints = Branch(constraints, starting_point.boundary);
    if (new_constraints > constraints){
        return starting_point;
    }
    
    auto sol = lp(objective, new_constrains);
    if (sol.val < starting_point.val){
        return starting_point;
    }

    return IntegerProgrammingHelper(objective, new_constraints, sol);
}
