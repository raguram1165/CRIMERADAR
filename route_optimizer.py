"""
RedShield AI — Smart Patrol Route Optimizer
Uses NetworkX + Dijkstra's algorithm for optimal patrol routing.
Run: python route_optimizer.py
"""

import networkx as nx
import pandas as pd

print("🚓 RedShield — Smart Patrol Route Optimizer")
print("=" * 50)

# Load high-risk locations
data = pd.read_csv("dataset/fir_data.csv")
high_risk = data[data["risk"] >= 85][["location", "latitude", "longitude", "risk"]].drop_duplicates("location")

# Build weighted graph
G = nx.Graph()

# Add police station as hub
G.add_node("Police_HQ", lat=13.0827, lng=80.2707, type="station")

# Add crime hotspots as nodes
for _, row in high_risk.iterrows():
    node_id = row["location"].replace(" ", "_")
    G.add_node(node_id, lat=row["latitude"], lng=row["longitude"],
               risk=row["risk"], type="hotspot")

# Add edges with distance as weight
nodes = list(G.nodes(data=True))
for i in range(len(nodes)):
    for j in range(i + 1, len(nodes)):
        n1, d1 = nodes[i]
        n2, d2 = nodes[j]
        dist = ((d1["lat"] - d2["lat"])**2 + (d1["lng"] - d2["lng"])**2)**0.5
        weight = round(dist * 111, 2)  # convert to km approx
        G.add_edge(n1, n2, weight=weight)

print(f"\n📍 Nodes (locations): {G.number_of_nodes()}")
print(f"🔗 Edges (connections): {G.number_of_edges()}")

# Find optimal route from HQ through all hotspots (greedy TSP)
hotspots = [n for n, d in G.nodes(data=True) if d.get("type") == "hotspot"]

print(f"\n🚨 High-Risk Hotspots to cover: {len(hotspots)}")

# Greedy nearest neighbor from Police HQ
current = "Police_HQ"
unvisited = hotspots.copy()
route = ["Police_HQ"]
total_distance = 0

while unvisited:
    nearest = min(unvisited, key=lambda n: G[current][n]["weight"])
    dist = G[current][nearest]["weight"]
    total_distance += dist
    route.append(nearest)
    unvisited.remove(nearest)
    current = nearest

# Return to base
total_distance += G[current]["Police_HQ"]["weight"]
route.append("Police_HQ")

print("\n🗺️  OPTIMAL PATROL ROUTE:")
print("-" * 40)
for i, stop in enumerate(route):
    prefix = "🏠" if stop == "Police_HQ" else f"🔴 Stop {i}"
    print(f"  {prefix}: {stop.replace('_', ' ')}")

print(f"\n📏 Total Patrol Distance: ~{total_distance:.2f} km")
print(f"🕐 Estimated Time: ~{int(total_distance * 3)} minutes (at 20km/h)")
print("\n✅ Route optimization complete!")

# Also compute shortest path between two specific locations
print("\n🔍 SHORTEST PATH ANALYSIS:")
if len(hotspots) >= 2:
    src = hotspots[0]
    dst = hotspots[-1]
    try:
        path = nx.shortest_path(G, src, dst, weight="weight")
        path_dist = nx.shortest_path_length(G, src, dst, weight="weight")
        print(f"  From: {src.replace('_', ' ')}")
        print(f"  To:   {dst.replace('_', ' ')}")
        print(f"  Path: {' → '.join(p.replace('_', ' ') for p in path)}")
        print(f"  Distance: {path_dist:.2f} km")
    except nx.NetworkXNoPath:
        print("  No path found between these nodes.")
