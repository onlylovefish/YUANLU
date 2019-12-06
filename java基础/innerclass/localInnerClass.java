import java.util.Date;

import javax.xml.crypto.Data;
import java.awt.*;
import java.awt.event.*;
import java.util.*;

import javax.swing.Action;
//import javax.swing.*;
import javax.swing.Timer;

/**
 * 由于在上一个内部类的文件中发现，只使用了一次TimePrinter这个类，所以可以创建局部内部类
 * 局部类可以由外部方法访问final变量
 */

public void start(){
    //局部类不能用public或private访问说明符进行声明，它的作用域被限定在声明这个局部类的块中，对外部世界完全隐藏
    class TimePrinter implements ActionListener{
        public void actionPerformed(ActionEvent event){
        Date now=new Date();
        System.out.println("at the tone,the time is"+now);
        if(beep) Toolkit.getDefaultToolkit().beep();
    }
}
    ActionListener listener=new TimePrinter();
    Timer t=new Timer(1000, listener);
    t.start();
}
/**
 * 局部类不仅可以访问包含他们的外部类，还可以访问局部变量，不过那些局部变量必须被声明成final
 */
public void start(int interval,final boolean beep){
    class TimePrinter implements ActionListener{
        public void actionPerformed(ActionEvent event){
            Date now=new Date();
            System.out.println("at the tone,the time is"+now);
            if(beep) Toolkit.getDefaultToolkit().beep();
        }
    }
    ActionListener listener=new TimePrinter();
    Timer t=new Timer(interval, listener);
    t.start();
}


/**
 * 假设想跟新一个封闭作用域中的计数器，则将变量命名为final并不可行
 */
//例如下面：
int counter=0;
Date[] dates=new Date[100];
for(int i=0;i<dates.length;i++)
    dates[i]=new Date()
        {
        public int compareTo(Date other){
            counter++;//这是不对的
            return super.compareTo(other);
        }
    };
Arrays.sort()
System.out.println(counter+"comparisons.");

/**
 * 不能将counter声明为final，由于Integer对象是不可变的，所以也不能用Integer来代替，补救的办法就是使用一个长度为1的数组
 * 这样的话，数组变量被声明为final，但是这仅仅表示不可以让它引用另一个数组，数组中的数据元素可以自由地更改
 */
final int[] counter=new int[1];
for(int i=0;i<dates.length;i++)
//后面和上面一样
/**
 * 顺便在这里说下数组的问题，之前没有写下来
 * int[] a=new int[100];这句话的涵义是，创建了一个可以存储100个整数的数组，数组长度不要求是常量，new int[n]会创建一个长度为n的数组
 * 创建一个数字数组时，所有元素都初始化为0，boolean元素会初始化为false，对象数组的元素则初始化为一个特殊值null,这表示这些元素还未存放任何对象
 * 例如String[] s=new String[10];这会创建一个包含10个字符串的数组，所有字符串都为null，而不是空串，所以如果要置为空串，则需要进行for赋值
 */
