package com.hsp;

import java.util.*;

public class DemoLinked {
    public static void main(String[] args){
        LinkedList ll=new LinkedList();
        ll.add("a");
        ll.addFirst("b");
        ll.addLast("c");
        ll.add("D");

        for(int i=0; i<ll.size(); i++){
            System.out.println((String)ll.get(i));
        }

        Vector vv=new Vector();
        vv.add("A");
        vv.add("b");
        for(int j=0;j<vv.size();j++){
            String s=(String)vv.get(j);
        }

        Stack stack=new Stack();
        stack.push("AA");

        Map hm=new HashMap();
//        HashMap hm=new HashMap();
        hm.put("a", "你好");
        hm.put("b", "我好");
        hm.put("c", "大家好");

        System.out.println(hm.containsKey("a"));
        System.out.println(hm.get("a"));

        //遍历HashMap中所有的key和值
        Iterator it=hm.keySet().iterator();
        while(it.hasNext()){
            //取出key
            String key=it.next().toString();
            //取出value
            String s=(String)hm.get(key);
            System.out.println(key+" "+s);
        }

        Hashtable ht=new Hashtable();
//        ht.put();
//        ht.get();
//        ht.put(null, null);  // 不允许
//        ht.get(null);  // 不允许

        hm.put(null, null);
        hm.get(null);

    }
}
