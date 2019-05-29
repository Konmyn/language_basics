package main

import (
    "os/exec"
    "path"
    "os"
    "fmt"
    "io/ioutil"
    "syscall"
    "strconv"
)

const cgroupMemoryHierarchyMount = "/sys/fs/cgroup/memory"

func main() {
    fmt.Println("hint: must run as root!")
    if os.Args[0] == "/proc/self/exe" {
        fmt.Printf("current pid %d\n", syscall.Getpid())
        fmt.Println()
        cmd := exec.Command("sh", "-c", `stress --vm-bytes 200m --vm-keep -m 1`)
        cmd.SysProcAttr = &syscall.SysProcAttr{}
        cmd.Stdin = os.Stdin
        cmd.Stdout = os.Stdout
        cmd.Stderr = os.Stderr
        if err := cmd.Run(); err != nil {
            fmt.Println(err)
            os.Exit(1)
        }
    }

    cmd := exec.Command("/proc/self/exe")
    cmd.SysProcAttr = &syscall.SysProcAttr{
        Cloneflags: syscall.CLONE_NEWUTS | syscall.CLONE_NEWIPC | syscall.CLONE_NEWPID | syscall.CLONE_NEWNS | syscall.CLONE_NEWUSER | syscall.CLONE_NEWNET,
    }
    // not work with below commad, do not know why
    // cmd.SysProcAttr.Credential = &syscall.Credential{Uid: uint32(1), Gid: uint32(1)}
    cmd.Stdin = os.Stdin
    cmd.Stdout = os.Stdout
    cmd.Stderr = os.Stderr

    if err := cmd.Start(); err != nil {
        fmt.Println("ERROR", err)
        os.Exit(1)
    } else {
        fmt.Printf("%v\n", cmd.Process.Pid)
        os.Mkdir(path.Join(cgroupMemoryHierarchyMount, "testmemorylimit"), 0755)
        ioutil.WriteFile(path.Join(cgroupMemoryHierarchyMount, "testmemorylimit", "tasks"), []byte(strconv.Itoa(cmd.Process.Pid)), 0644)
        ioutil.WriteFile(path.Join(cgroupMemoryHierarchyMount, "testmemorylimit", "memory.limit_in_bytes"), []byte("100m"), 0644)
    }
    cmd.Process.Wait()
}
