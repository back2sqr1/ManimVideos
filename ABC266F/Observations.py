from manim import *

import networkx as nx
from networkx import nodes, edges


def create_textbox(color, string, h, w):
    result = VGroup()  # create a VGroup
    box = Rectangle(  # create a box
        height=h, width=w, fill_color=color,
        fill_opacity=0.5, stroke_color=color
    )
    text = Text(string).move_to(box.get_center())  # create text
    result.add(box, text)  # add both objects to the VGroup
    return result


class ManimStack:
    border_height, border_width = 0, 0
    color = BLUE
    player = None
    stackBorder = Rectangle(height=1, width=1)
    elements = []
    sz = 0
    # Max amount of elements is 5
    # TODO
    rv = 1
    L, R, U, D = 0, 0, 0, 0

    def __init__(self, player, border_height=5, border_width=2, color=BLUE, rt=1, wt=1, L=0, R=0, U=0, D=0):
        self.border_height = border_height
        self.border_width = border_width
        self.color = color
        self.player = player
        self.stackBorder = Rectangle(height=border_height, width=border_width).shift(
            LEFT * L + RIGHT * R + UP * U + DOWN * D)
        self.player.play(Create(self.stackBorder, run_time=rt))
        self.player.wait(wt)
        self.L = L
        self.R = R
        self.U = U
        self.D = D

    def move_to(self, U=0, D=0, L=0, R=0, rt=1, wt=1):
        self.stackBorder.generate_target()
        self.stackBorder.target.move_to(LEFT * L + RIGHT * R + UP * U + DOWN * D)
        if (U == 0 and D == 0) or U > 0:
            U -= 3
        else:
            D += (self.sz) - 2
        cnt = 0
        for x in self.elements:
            x.generate_target()
            if (U == 0 and D == 0) or U > 0:
                U += 1
            else:
                D -= 1
            x.target.move_to(LEFT * L + RIGHT * R + UP * U + DOWN * D)
            cnt += 1
        self.player.play(MoveToTarget(self.stackBorder), run_time=rt)
        self.player.wait(wt)
        for x in self.elements:
            self.player.play(MoveToTarget(x), run_time=rt)
            self.player.wait(wt)
            self.player.play(MoveToTarget(x), run_time=rt)
            self.player.wait(wt)

        self.L = L
        self.R = R
        self.U = U
        self.D = D

    def push(self, val, rt=1, wt=1):
        if self.sz == 5:
            return
        root = create_textbox(color=BLUE, string=val, h=self.border_height / 5, w=self.border_width)
        self.player.play(Create(root), run_time=rt)
        self.player.wait(wt)
        root.generate_target()
        L, R, U, D = self.L, self.R, self.U, self.D
        if not U == 0:
            U += self.sz + 1
        else:
            D += -self.sz + 4
            print("HERE")
        root.target.move_to(LEFT * L + RIGHT * R + UP * U + DOWN * D)
        self.player.play(MoveToTarget(root), run_time=rt)
        self.player.wait(wt)
        self.sz += 1
        self.elements.append(root)

    def pop(self, rt=1, wt=1):
        if self.sz == 0:
            return
        self.player.play(Uncreate(self.elements[-1]), run_time=rt)
        self.elements.remove(self.elements[-1])
        self.player.wait(wt)


class ManimGraph:
    nodes = []
    edges = []
    edge_config: dict | None = None
    vertex_config: dict | None = None
    L, R, U, D = 0, 0, 0, 0
    g = Graph(nodes, edges)
    g2 = Graph(nodes, edges)
    ly = "kamada_kawai"
    player = None  # self equivalent

    def __init__(self, player, nodes, edges, rt=1, wt=1, L=0, R=0, U=0, D=0, ly="kamada_kawai", rv = 1):
        self.nodes = nodes
        self.edges = edges
        self.L = L
        self.R = R
        self.U = U
        self.D = D
        self.ly = ly
        self.rv = rv
        self.g = Graph(vertices=self.nodes, edges=self.edges, layout=ly, root_vertex=self.rv, labels=True).shift(
            LEFT * L + RIGHT * R + UP * U + DOWN * D)
        self.player = player
        self.player.play(Create(self.g), run_time=rt)
        self.player.wait(wt)
        self.change_edge({(nodes[0], nodes[1]): {"stroke_color": WHITE}})
        self.change_node({nodes[0]: {"fill_color": WHITE}})

    def change_node(self, node_c, rt=1, wt=1, add=False):
        if add and not self.vertex_config == None:
            self.vertex_config.update(node_c)
        else:
            self.vertex_config = node_c
        self.g2 = Graph(vertices=self.nodes, edges=self.edges, layout=self.ly, root_vertex=self.rv, labels=True,
                        edge_config=self.edge_config, vertex_config=self.vertex_config).shift(
            LEFT * self.L + RIGHT * self.R + UP * self.U + DOWN * self.D)
        self.player.play(Transform(self.g, self.g2), run_time=rt)
        self.reset()
        self.player.wait(wt)

    def reset(self):
        self.g2 = Graph([], [])

    def change_ly(self, ly, rt=1, wt=1):
        self.ly = ly
        self.g2 = Graph(vertices=self.nodes, edges=self.edges, layout=self.ly, root_vertex=self.rv, labels=True,
                        edge_config=self.edge_config, vertex_config=self.vertex_config).shift(
            LEFT * self.L + RIGHT * self.R + UP * self.U + DOWN * self.D)
        self.player.play(Transform(self.g, self.g2), run_time=rt)
        self.reset()
        self.player.wait(wt)

    def change_edge(self, edge_c, rt=1, wt=1, add=False):
        if add:
            self.edge_config.update(edge_c)
        else:
            self.edge_config = edge_c
        self.g2 = Graph(vertices=self.nodes, edges=self.edges, layout=self.ly, root_vertex=self.rv, labels=True,
                        edge_config=self.edge_config, vertex_config=self.vertex_config).shift(
            LEFT * self.L + RIGHT * self.R + UP * self.U + DOWN * self.D)
        self.player.play(Transform(self.g, self.g2), run_time=rt)
        self.reset()
        self.player.wait(wt)

    def move_to(self, U=0, D=0, L=0, R=0, rt=1, wt=1):
        self.g.generate_target()
        self.g.target.move_to(RIGHT * (R + .15) + UP * U + DOWN * D + LEFT * L)
        self.L = L
        self.R = R
        self.U = U
        self.D = D
        self.player.play(MoveToTarget(self.g), run_time=rt)
        self.player.wait(wt)

    def transform(self, nodes, edges, rt=1, wt=1, ly="kamada_kawai", rv = 1):
        self.rv = rv
        g2 = Graph(vertices=nodes, edges=edges, layout=ly, root_vertex=self.rv, labels=True).shift(
            LEFT * self.L + RIGHT * self.R + UP * self.U + DOWN * self.D)
        print(edges)
        self.player.play(Uncreate(self.g), run_time=rt)
        self.player.play(Create(g2), run_time=rt)
        self.g = g2
        self.player.wait(wt)

    def highlight_paths(self, r=1, w=1, root=1, used={1000}, edge_used={(100, 0)}):
        temp_r, temp_w = r, w
        temp_ed = edge_used
        self.change_node({root: {"fill_color": RED}}, rt=r, wt=w, add=True)
        if root in used:
            return
        used.add(root)
        for ed in self.edges:
            if ed[0] == root and not ed in temp_ed:
                self.change_edge({ed: {"stroke_color": RED}}, rt=r, wt=w, add=True)
                temp_ed.add(ed)
                self.highlight_paths(root=ed[1], used=used, r=temp_r, w=temp_w)
                temp_ed.remove(ed)
                self.change_edge({ed: {"stroke_color": WHITE}}, rt=r, wt=w, add=True)
            elif ed[1] == root and not ed in temp_ed:
                self.change_edge({ed: {"stroke_color": RED}}, rt=r, wt=w, add=True)
                temp_ed.add(ed)
                self.highlight_paths(root=ed[0], used=used, r=temp_r, w=temp_w)
                temp_ed.remove(ed)
                self.change_edge({ed: {"stroke_color": WHITE}}, rt=r, wt=w, add=True)

        self.change_node({root: {"fill_color": WHITE}}, rt=r, wt=w, add=True)
        used.remove(root)


class Obs(Scene):

    def construct(self):
        title = Text("Observations").scale(2)
        self.play(Write(title), run_time = 3)
        self.wait(3)
        self.play(Unwrite(title), run_time = 3)
        self.wait(3);
        n = [1, 2, 3, 4, 5]
        e = [(1, 2), (1, 3), (2, 3), (1, 4), (2, 5)]

        g = ManimGraph(player = self, nodes = n, edges = e, rt = 3, wt = 3, ly = "kamada_kawai")
        g.move_to(R = 3);
        nodesText = Text("[1, 2, 3, 4, 5] : N nodes").scale(.5).shift(LEFT * 3 + UP)
        edgesText = Text("[(1, 2), (1, 3), (2, 3), (1, 4), (2, 5)] : N edges").scale(.5).shift(LEFT * 3);

        self.play(Write(nodesText), Write(edgesText), run_time = 3)
        self.wait(12);

        n = [1, 2, 3, 4, 5]
        e = [(1, 2), (2, 3), (1, 4), (2, 5)]
        self.play(Unwrite(nodesText), Unwrite(edgesText))

        t = ManimGraph(player = self, nodes = n, edges = e, ly = "tree", rt = 2, wt = 2, L = 3)
        for i in n:
            t.highlight_paths(r = .1, w = .1, root = i)
        g.change_node({1 : {"fill_color" : RED}}, add = True, rt = .25)
        g.change_edge({(1, 3): {"stroke_color" : RED}}, add = True, rt = .25)
        g.change_node({3: {"fill_color": RED}}, add = True, rt = .25)
        g.change_edge({(2, 3): {"stroke_color" : RED}}, add = True, rt = .25)
        g.change_node({2: {"fill_color": RED}}, add = True, rt = .25)
        g.change_edge({(1, 2): {"stroke_color" : RED}}, add = True, rt = .25)
        self.wait(10)
        c = Circle(radius = 1.05, color = RED, fill_opacity=1).shift(RIGHT * 3 + UP * .5)
        cText = Text("C").shift(RIGHT * 3 + UP * .5);

        self.play(Create(c), Write(cText))
        self.wait(30)
        self.play(Uncreate(t.g))
        self.wait(10)
        self.play(Uncreate(g.g), Uncreate(c), Unwrite(cText))
        self.wait(2)





