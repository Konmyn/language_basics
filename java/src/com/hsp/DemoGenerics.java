package com.hsp;

import java.util.*;
import java.lang.reflect.Method;

public class DemoGenerics {
    public static void main(String[] args){
//        ArrayList<Dog> al=new ArrayList<Dog>();
//        Dog dog1=new Dog();
//        al.add(dog1);
//        Dog tmp=al.get(0);
        Gen<Cat> gen1=new Gen<>(new Cat());
        gen1.showTypeName();
    }
}

class Dog {
    private String name;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    private int age;
}

class Cat {
    public void sing(){
        System.out.println("aaa");
    }

    public void count(int a, int b){
        System.out.println(a+b);
    }

}

class Gen<T> {
    private T o;

    public void showTypeName(){
        System.out.println("类型是："+o.getClass().getName());
        // 通过反射机制，可以得到T这个类型的很多信息
        Method[] m=o.getClass().getDeclaredMethods();
        // 打印
        for(int i=0; i<m.length; i++) {
            System.out.println(m[i].getName());
        }
    }

    public Gen(T a) {
        this.o=a;
    }
}