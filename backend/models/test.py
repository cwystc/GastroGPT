# 1) Install PuLP if needed:
#    pip install pulp

import pulp

# The given directed graph (with edge lengths)
graph = {
    's': [('B', 1), ('D', 2)],
    'B': [('E', 3), ('t', 7)],
    'D': [('E', 3), ('C', 6)],
    'E': [('t', 4), ('C', 2)],
    'C': [('t', 1)],
    't': []
}

# We'll use a fixed order just for neat printing:
vertex_order = ['s','B','C','D','E','t']

# 2) Create the linear program: "MaxDistance" with objective = maximize x_s.
prob = pulp.LpProblem("MaxDistance", pulp.LpMaximize)

# 3) Create LP variables x[v] for each vertex v.
#    For v != 't', we have x[v] >= 0; for v == 't', we have x[t] <= 0.
x = {}
for v in vertex_order:
    if v == 't':
        x[v] = pulp.LpVariable(name=v, lowBound=None, upBound=0)  # x_t <= 0
    else:
        x[v] = pulp.LpVariable(name=v, lowBound=0)                # x_v >= 0

# 4) Objective: maximize x_s
prob += x['s'], "Objective_x_s"

# 5) For each edge (u,v) with length c_uv, add the constraint x_u - x_v <= c_uv
for u in graph:
    for (v, length) in graph[u]:
        prob += (x[u] - x[v] <= length), f"Edge_{u}_to_{v}"

# 6) Solve the LP
prob.solve()

# 7) Print the results
print("Status:", pulp.LpStatus[prob.status])
print("Optimal objective value:", pulp.value(prob.objective))
for v in vertex_order:
    print(f"x_{v} = {pulp.value(x[v])}")
