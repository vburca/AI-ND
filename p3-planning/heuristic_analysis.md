# Project 3 - Planning Search Problems

## Air Cargo Problem. Metrics for non-heuristic planning solution searches

Before we start analyzing each problem with each of the search algorithms, let's define the `optimality` of a problem. First, we will find the optimal solution to the problem and describe the plan. The length of the optimal solution will be `len_opt_sol`. Then, the `optimality` is defined as: `len_opt_sol / len_current_search * 100`
#### Results for the `air_cargo_p1` problem.
Problem definition:
```
Init(At(C1, SFO) ∧ At(C2, JFK)
    ∧ At(P1, SFO) ∧ At(P2, JFK)
    ∧ Cargo(C1) ∧ Cargo(C2)
    ∧ Plane(P1) ∧ Plane(P2)
    ∧ Airport(JFK) ∧ Airport(SFO))
Goal(At(C1, JFK) ∧ At(C2, SFO))
```
Optimal solution:
```
Load(C1, P1, SFO)
Load(C2, P2, JFK)
Fly(P2, JFK, SFO)
Unload(C2, P2, SFO)
Fly(P1, SFO, JFK)
Unload(C1, P1, JFK)
```
Length of optimal solution: `len_opt_sol = 6`.
| Algorithm | Expansions | Goal Tests | Time (s) | Optimality |
| :-------------: | :-------------: | :---------: | :-------: | :-------: |
| breadth_first_search      | 43   | 56         | 0.053912139001113246     | 100% | 
| depth_first_graph_search  | 21         | 22         | 0.022073595000620116       | 30% |
| depth_limited_search      | 101         | 271         | 0.15392913300092914       | 12% |
| uniform_cost_search       | 55         | 57         | 0.07226297700071882      | 100% |

#### Results for the `air_cargo_p2` problem.
Problem definition:
```
Init(At(C1, SFO) ∧ At(C2, JFK) ∧ At(C3, ATL)
    ∧ At(P1, SFO) ∧ At(P2, JFK) ∧ At(P3, ATL)
    ∧ Cargo(C1) ∧ Cargo(C2) ∧ Cargo(C3)
    ∧ Plane(P1) ∧ Plane(P2) ∧ Plane(P3)
    ∧ Airport(JFK) ∧ Airport(SFO) ∧ Airport(ATL))
Goal(At(C1, JFK) ∧ At(C2, SFO) ∧ At(C3, SFO))
```
Optimal solution:
```
Load(C1, P1, SFO)
Load(C2, P2, JFK)
Load(C3, P3, ATL)
Fly(P2, JFK, SFO)
Unload(C2, P2, SFO)
Fly(P1, SFO, JFK)
Unload(C1, P1, JFK)
Fly(P3, ATL, SFO)
Unload(C3, P3, SFO)
```
Length of optimal solution: `len_opt_sol = 9`.
| Algorithm | Expansions | Goal Tests | Time (s) | Optimality |
| :-------------: | :-------------: | :---------: | :-------: | :-------: |
| breadth_first_search      | 3343   | 4609         | 24.304792158000055     | 100% | 
| depth_first_graph_search  | 624        | 625         | 5.251924964000864       | 1.453% |
| depth_limited_search      | n/a         | n/a         | > 10 mins       | n/a |
| uniform_cost_search       | 4852         | 4854         | 69.47413250000136      | 100% |

#### Results for the `air_cargo_p3` problem.
Problem definition:
```
Init(At(C1, SFO) ∧ At(C2, JFK) ∧ At(C3, ATL) ∧ At(C4, ORD)
    ∧ At(P1, SFO) ∧ At(P2, JFK)
    ∧ Cargo(C1) ∧ Cargo(C2) ∧ Cargo(C3) ∧ Cargo(C4)
    ∧ Plane(P1) ∧ Plane(P2)
    ∧ Airport(JFK) ∧ Airport(SFO) ∧ Airport(ATL) ∧ Airport(ORD))
Goal(At(C1, JFK) ∧ At(C3, JFK) ∧ At(C2, SFO) ∧ At(C4, SFO))
```
Optimal solution:
```
Load(C1, P1, SFO)
Load(C2, P2, JFK)
Fly(P2, JFK, ORD)
Load(C4, P2, ORD)
Fly(P1, SFO, ATL)
Load(C3, P1, ATL)
Fly(P1, ATL, JFK)
Unload(C1, P1, JFK)
Unload(C3, P1, JFK)
Fly(P2, ORD, SFO)
Unload(C2, P2, SFO)
Unload(C4, P2, SFO)
```
Length of optimal solution: `len_opt_sol = 12`.
| Algorithm | Expansions | Goal Tests | Time (s) | Optimality |
| :-------------: | :-------------: | :---------: | :-------: | :-------: |
| breadth_first_search      | 14663   | 18098         | 161.9008968679991     | 100% | 
| depth_first_graph_search  | 408        | 409         | 2.6251068919991667      | 3.061% |
| depth_limited_search      | n/a         | n/a         | > 10 mins       | n/a |
| uniform_cost_search       | n/a         | n/a         | > 10 mins      | n/a |

#### Comments
As we can see, the `breadth_first_search` always produces the optimal solution in the shortest time. This is expected, given the description of the algorithm. Moreover, this is also a factor that influences the large number of expansions and goal tests associated with `breadth_first_search`. On the other hand, `depth_first_graph_search` has a lower expansion number, but it fails to produce the optimal solution due to its approach of continuously expanding deeper instead of checking for the shortest path.