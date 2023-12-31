import networkx as nx
import random
import math
import sys
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as mb

start = []
end = []
obstacles = []
addit_points = []
max_iterat = 500
maxCoordX = 700
maxCoordY = 650
temp = []


def Distance(node1, node2):
    return math.sqrt((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2)


def MinNode(g, node):
    minDist = 100000
    minNode = None
    for n in g.nodes:
        if Distance(n, node) < minDist and n != node:
            minDist = Distance(n, node)
            minNode = n
    return minNode


def Colides(obstacles, currentNode, minNode):
    for obstacle in obstacles:

        if Distance(obstacle[0], currentNode) <= obstacle[1] + obstacle[1] / 10:
            return True
        t = (currentNode[0] * (currentNode[0] - minNode[0]) + currentNode[1] * (currentNode[1] - minNode[1]) -
             obstacle[0][0] * (currentNode[0] - minNode[0]) - obstacle[0][1] * (
                     currentNode[1] - minNode[1])) / (0 - (currentNode[1] - minNode[1]) ** 2 -
                                                      (currentNode[0] - minNode[0]) ** 2)
        node = ((currentNode[0] + t * (currentNode[0] - minNode[0])), (currentNode[1] +
                                                                       t * (currentNode[1] - minNode[1])))

        if (line_intersection(obstacle[0][0], obstacle[0][1], node[0], node[1], minNode[0], minNode[1], currentNode[0],
                              currentNode[1]) or line_intersection(obstacle[0][0], obstacle[0][1], node[0] + 0.5,
                                                                   node[1] + 0.5,
                                                                   minNode[0], minNode[1], currentNode[0],
                                                                   currentNode[1]) or line_intersection(obstacle[0][0],
                                                                                                        obstacle[0][1],
                                                                                                        node[0] - 0.5,
                                                                                                        node[1] - 0.5,
                                                                                                        minNode[0],
                                                                                                        minNode[1],
                                                                                                        currentNode[0],
                                                                                                        currentNode[
                                                                                                            1])) \
                and Distance(node, obstacle[0]) <= obstacle[1] + obstacle[1] / 100:
            return True
    return False


def MidCoords(node1, node2):
    return ((node1[0] + node2[0]) / 2, (node1[1] + node2[1]) / 2)


def line_intersection(x1, y1, x2, y2, x3, y3, x4, y4):
    def on_segment(px, py, qx, qy, rx, ry):
        if (qx <= max(px, rx) and qx >= min(px, rx) and
                max(py, ry) >= qy >= min(py, ry)):
            return True
        return False

    def orientation(px, py, qx, qy, rx, ry):
        val = (qy - py) * (rx - qx) - (qx - px) * (ry - qy)
        if val == 0:
            return 0
        return 1 if val > 0 else -1

    o1 = orientation(x1, y1, x2, y2, x3, y3)
    o2 = orientation(x1, y1, x2, y2, x4, y4)
    o3 = orientation(x3, y3, x4, y4, x1, y1)
    o4 = orientation(x3, y3, x4, y4, x2, y2)

    if o1 != o2 and o3 != o4:
        return True

    if o1 == 0 and on_segment(x1, y1, x3, y3, x2, y2):
        return True

    if o2 == 0 and on_segment(x1, y1, x4, y4, x2, y2):
        return True

    if o3 == 0 and on_segment(x3, y3, x1, y1, x4, y4):
        return True

    if o4 == 0 and on_segment(x3, y3, x2, y2, x4, y4):
        return True

    return False


def HasMin(currentNode, minNode, graph):
    dist = Distance(currentNode, minNode)
    minDist = dist
    minToRep = []
    for u, v in graph.edges():
        t = (u[0] * (u[0] - v[0]) + u[1] * (u[1] - v[1]) - currentNode[0] * (u[0] - v[0]) - currentNode[1] * (
                u[1] - v[1])) / (-(u[1] - v[1]) ** 2 - (u[0] - v[0]) ** 2)
        newNode = ((u[0] + t * (u[0] - v[0])), (u[1] + t * (u[1] - v[1])))
        if newNode != currentNode and newNode != minNode and (
                line_intersection(newNode[0], newNode[1], currentNode[0], currentNode[1], u[0],
                                  u[1], v[0], v[1]) or line_intersection(newNode[0] + 1, newNode[1] + 1, currentNode[0],
                                                                         currentNode[1], u[0],
                                                                         u[1], v[0], v[1]) or line_intersection(
            newNode[0] - 1, newNode[1] - 1, currentNode[0], currentNode[1], u[0],
            u[1], v[0], v[1])):
            newDist = Distance(newNode, currentNode)
            if newDist < minDist:
                minDist = newDist
                minToRep = [newNode, u, v]

    if minDist < dist:
        return minToRep
    return None


def MinNodeWithOut(g, currentNode, nodes):
    minDist = 100000
    minNode = None
    for n in g.nodes:
        if Distance(n, currentNode) < minDist and n not in nodes:
            minDist = Distance(n, currentNode)
            minNode = n
    return minNode


def RRT(start, end, obstacles, max_iterat, maxX, maxY):
    st = (start[0], start[1])
    en = (end[0], end[1])
    for obstacle in obstacles:
        if Distance(start, obstacle[0]) <= obstacle[1] + 1 or Distance(end, obstacle[0]) <= obstacle[1] + 1:
            return None
    currentNode = st
    g = nx.Graph()
    g.add_node(currentNode)

    for _ in range(max_iterat):
        currentNode = (random.randint(50, maxX - 50), random.randint(50, maxY - 50))
        minNode = MinNode(g, currentNode)
        toRep = HasMin(currentNode, minNode, g)
        if toRep is not None:
            g.add_node(toRep[0])
            g.remove_edge(toRep[1], toRep[2])
            g.add_edge(toRep[1], toRep[0], weight=Distance(toRep[1], toRep[0]))
            g.add_edge(toRep[2], toRep[0], weight=Distance(toRep[2], toRep[0]))
            minNode = toRep[0]
        newNode = currentNode
        t = 0.01
        while currentNode == minNode or Colides(obstacles, currentNode, minNode):
            currentNode = ((newNode[0] - t * (newNode[0] - minNode[0])),
                           (newNode[1] - t * (newNode[1] - minNode[1])))
            t = t + 0.01
            if t > 1.02:
                break
        g.add_edge(currentNode, minNode, weight=Distance(currentNode, minNode))
    minNode = MinNode(g, en)

    for i in range(len(addit_points)-1):
        tmp = (addit_points[i][0], addit_points[i][1])
        toRep = HasMin(tmp, minNode, g)
        g.add_node(toRep[0])
        g.remove_edge(toRep[1], toRep[2])
        g.add_edge(toRep[1], toRep[0], weight=Distance(toRep[1], toRep[0]))
        g.add_edge(toRep[2], toRep[0], weight=Distance(toRep[2], toRep[0]))
        t = 0.01
        minNode = MinNode(g, tmp)
        g.add_edge(tmp, minNode, weight=Distance(tmp, minNode))

    nodes = []
    minNode = MinNode(g, en)
    f = True
    while Colides(obstacles, en, minNode):
        nodes.append(minNode)
        if len(nodes) - 1 <= len(g.nodes):
            f = False
            break
        minNode = MinNodeWithOut(g, en, nodes)
    if f:
        g.add_edge(en, minNode, weight=Distance(currentNode, minNode))
        return g
    else:
        return None
    


def dijkstra_algorithm(graph, start_node):
    unvisited_nodes = list(graph.nodes())
    for i in range(len(addit_points)):
        unvisited_nodes.append(addit_points[i])

    shortest_path = {}

    previous_nodes = {}

    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value

    shortest_path[start_node] = 0

    while unvisited_nodes:

        current_min_node = None
        for node in unvisited_nodes:
            if current_min_node is None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node

        neighbors = graph.neighbors(current_min_node)
        for neighbor in neighbors:
            tentative_value = shortest_path[current_min_node] + graph.get_edge_data(current_min_node, neighbor)[
                "weight"]
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value

                previous_nodes[neighbor] = current_min_node

        unvisited_nodes.remove(current_min_node)

    return previous_nodes, shortest_path


def print_result(previous_nodes, shortest_path, start_node, target_node):
    path = []
    node = target_node

    while node != start_node:
        path.append(node)
        node = previous_nodes[node]

    path.append(start_node)
    path.reverse()
    return path


def draw_edges():
    global start
    global end
    max_iterat = int(entry.get())
    try:
        graph = RRT(start, end, obstacles, max_iterat, maxCoordX, maxCoordY)
    except:
        mb.showinfo("Маршрут", "нет пути")
    st = start
    for j in range(len(addit_points)):
        t = True
        for i in obstacles:
            if ((addit_points[j][0] - i[0][0])**2 + (addit_points[j][1]-i[0][1])**2)**0.5 < i[1]:
                mb.showinfo("Маршрут", "нет пути")
                clear_scene()
                return None
        
    if graph is None:
        mb.showinfo("Маршрут", "нет пути")
    else:
        for u, v in graph.edges:
            canvas.create_line(u[0], u[1], v[0], v[1])
        canvas.create_oval(start[0] - 3, start[1] - 3, start[0] + 3, start[1] + 3, fill="red")
        canvas.create_oval(end[0] - 3, end[1] - 3, end[0] + 3, end[1] + 3, fill="purple")
        
        st = start
        for i in range(len(addit_points)):
            en = addit_points[i]
            previous_nodes, shortest_path = dijkstra_algorithm(graph, (st[0], st[1]))
            path = print_result(previous_nodes, shortest_path, (st[0], st[1]), (en[0], en[1]))
            for i in range(len(path) - 1):
                node1 = path[i]
                node2 = path[i + 1]
                canvas.create_line(node1[0], node1[1], node2[0], node2[1], fill="green", width=3)
            st = en
        mb.showinfo("Маршрут", "Найден следующий лучший маршрут {}.".format(shortest_path[(end[0], end[1])]))


def save_scene():
    file = open("RRT.txt", "w")
    file.write("start, end:\n" + str(start) + '\n' + str(end) + '\n' + "addit_points:\n" + str(list(i for i in addit_points)) + "\n" + "obstracles:\n")
    for obstacle in obstacles:
        file.write(str(obstacle) + '\n')
    file.close()


def load_scene():
    global addit_points
    file = open("RRT.txt")
    canvas.delete("all")
    obstacles.clear()
    start.clear()
    end.clear()
    f_start = False
    f_end = False
    f_addit_points = False
    for line in file:
        if line != "start, end:\n" and line != "obstracles:\n" and line != "addit_points:\n":
            if not f_start:
                l = line.split(", ")
                start.append(float(l[0][1:]))
                start.append(float(l[1][:len(l[1]) - 2]))
                f_start = True
            elif not f_end:
                l = line.split(", ")
                end.append(float(l[0][1:]))
                end.append(float(l[1][:len(l[1]) - 2]))
                f_end = True
            elif not f_addit_points:
                l = line[2:len(l)-4]
                tmp = []
                k = ""
                l = l.replace("(", "")
                l = l.replace(")", "")
                l = l.split(", ")
                for i in range(0, len(l), 2):
                    addit_points.append((int(l[i]), int(l[i+1])))
                    canvas.create_oval(int(l[i]) - 3, int(l[i+1]) - 3, int(l[i]) + 3, int(l[i+1]) + 3, fill="green", tags="cc")
                f_addit_points = True
            else:
                l = line.split("), ")
                l1 = l[0].split(", ")
                obstacles.append(((float(l1[0][2:]), float(l1[1])), float(l[1][:len(l[1]) - 2])))
    canvas.create_oval(start[0] - 3, start[1] - 3, start[0] + 3, start[1] + 3, fill="yellow", tags="cc")
    canvas.create_oval(end[0] - 3, end[1] - 3, end[0] + 3, end[1] + 3, fill="green", tags="cc")
    for obstacle in obstacles:
        canvas.create_oval(obstacle[0][0] - obstacle[1], obstacle[0][1] - obstacle[1], obstacle[0][0] + obstacle[1],
                           obstacle[0][1] + obstacle[1], fill="grey")

def clear_scene():
    global addit_points
    canvas.delete("all")
    addit_points = []
    start.clear()
    end.clear()
    obstacles.clear()


root = Tk()
root.title("RRT")
root.geometry(f'{maxCoordX + 200}x{maxCoordY + 100}')

entry = ttk.Entry()
entry.place(x=maxCoordX + 50, y=maxCoordY - 500, width=120, height=40)
entry.insert(0, "100")

canvas = Canvas(bg="white", width=maxCoordX, height=maxCoordY)
canvas.pack(anchor="nw", expand=1)
btn = ttk.Button(text="Draw", command=draw_edges)
btn.place(x=maxCoordX + 50, y=maxCoordY - 400, width=120, height=40)
btn1 = ttk.Button(text="Save", command=save_scene)
btn1.place(x=maxCoordX + 50, y=maxCoordY - 300, width=120, height=40)
btn2 = ttk.Button(text="Load", command=load_scene)
btn2.place(x=maxCoordX + 50, y=maxCoordY - 200, width=120, height=40)
btn3 = ttk.Button(text="Clear", command=clear_scene)
btn3.place(x=maxCoordX + 50, y=maxCoordY - 100, width=120, height=40)


def add_conclusion_vertex(event):
    global addit_points
    global end
    if len(start) == 0:
        canvas.delete("cc")
        start.clear()
        end.clear()
        start.append(event.x)
        start.append(event.y)
        canvas.create_oval(event.x - 3, event.y - 3, event.x + 3, event.y + 3, fill="yellow", tags="cc")
    else:
        addit_points.append((event.x, event.y))
        canvas.create_oval(event.x - 3, event.y - 3, event.x + 3, event.y + 3, fill="green", tags="cc")
        end = []
        end.append(event.x)
        end.append(event.y)


def add_obstacle(event):
    temp.append((event.x, event.y))

    if len(temp) == 2:
        center = (temp[0][0], temp[0][1])
        radius = Distance(center, (temp[1][0], temp[1][1]))
        canvas.create_oval(center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius, fill="grey")
        temp.clear()
        obstacles.append((center, radius))


canvas.bind('<Button-3>', add_conclusion_vertex)
canvas.bind('<Button-1>', add_obstacle)

root.mainloop()