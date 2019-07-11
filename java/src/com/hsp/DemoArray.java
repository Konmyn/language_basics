package com.hsp;


import java.util.*;

public class DemoArray {
    public static void main (String[] args) {
        ArrayList al=new ArrayList();
        //显示大小
        System.out.println("al大小是："+al.size());
        //向al中加入数据（类型是Object）
        Clerk clerk1 = new Clerk("宋江", "50", 1000);
        Clerk clerk2 = new Clerk("吴用", "45", 1200);
        Clerk clerk3 = new Clerk("林冲", "35", 1600);
        //将clerk1加入到al中
        al.add(clerk1);
        al.add(clerk2);
        al.add(clerk3);
        //可不可以放入同样的对象
        al.add(clerk1);
        System.out.println("al大小是："+al.size());
        //访问al中的数据
        //访问第一个对象
        Clerk temp=(Clerk)al.get(0);
        System.out.println("第一个人的名字："+temp.getName());

        //遍历
        for(int i=0; i<al.size(); i++){
            Clerk tmp=(Clerk)al.get(i);
            System.out.println("名字："+tmp.getName());
        }

        //如何删除
        System.out.println("删除元素");
        al.remove(1);
        System.out.println("al大小是："+al.size());
    }
}

class Clerk {
    private String name;
    private String age;
    private double sal;

    public void setName(String name) {
        this.name = name;
    }

    public String getAge() {
        return age;
    }

    public void setAge(String age) {
        this.age = age;
    }

    public double getSal() {
        return sal;
    }

    public void setSal(double sal) {
        this.sal = sal;
    }

    public Clerk(String name, String age, double sal) {
        this.name = name;
        this.age = age;
        this.sal = sal;
    }
}