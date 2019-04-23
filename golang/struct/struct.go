package main

import (
    "fmt"
)

type treeNode struct {
    value int
    left, right *treeNode
}

func (t treeNode) print() {
    fmt.Print(t.value, " ")
}

func (t *treeNode) setValue(v int) {
    t.value = v
}

func (t *treeNode) traverse() {
    t.traverseFunc(func(n *treeNode) {
        n.print()
    })
    fmt.Println()
}

func (t *treeNode) traverseFunc(f func(*treeNode)) {
    if t == nil {
        return
    }
    t.left.traverseFunc(f)
    f(t)
    t.right.traverseFunc(f)
}

func createTreeNode(n int) *treeNode {
    return &treeNode{value: n}
}

func main () {
    var root treeNode

    root = treeNode{value: 1}
    root.left = &treeNode{}
    root.right = &treeNode{6, nil, nil}
    root.right.left = new(treeNode)
    root.left.left = createTreeNode(88)

    fmt.Println(root)

    node := []treeNode{
        {value: 1},
        {},
        {3, nil, nil},
        {7, nil, &root},
    }
    fmt.Println(node)

    root.traverse()

    nodeCount := 0
    root.traverseFunc(func(node *treeNode) {
        nodeCount++
    })
    fmt.Println("nodeCount: ", nodeCount)
}
