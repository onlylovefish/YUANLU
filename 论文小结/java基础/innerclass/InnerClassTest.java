//内部类可以访问该类定义所在的作用域中的数据，包括私有的数据
// 内部类可以对同一个包中的其他类隐藏起来
// 当想要定义一个回调函数且不想编写大量代码时，使用匿名内部类比较便捷
//在外围的作用域外，可以这里引用内部类：outerClass.InnerClass
/**
 * 内部类是一种编译器现象，与虚拟机无关，编译器会将内部类翻译成用＄符号分隔外部类名与内部类名的常规文件，但虚拟机并不知道
 */
import java.awt.*;
import java.awt.event.*;
import java.sql.Date;
import java.util.*;
//import javax.swing.*;
import javax.swing.Timer;

//import sun.swing.PrintColorUIResource;

/**
 * this program demonstrates the use of inner clsses
 */
public class InnerClassTest{
    public static void main(final String[] args) {
        final TalkingClock clock = new TalkingClock(1000, true);
        clock.start();
    }

}

class TalkingClock {
    private final int interval;
    private final boolean beep;

    /**
     * construct a talking clock
     */
    public TalkingClock(final int interval,final boolean beep){
        this.interval=interval;
        this.beep=beep;
    }

    /**
     * start the clock
     */
    public void start(){
        ActionListener listener=new TimePrinter();
        Timer t=new Timer(interval, listener);
        t.start();
    }
    //TimePrinter类位于TalkingClock类内部，这并不意味着每个TalkClock都有一个TimePrinter实例域
    //为了能够运行该程序，内部类的对象总有一个隐式的引用，它指向了创建它的外部类对象，这个引用在内部类的定义中是不可见的
    //TimePrinter类申明为私有的，只有TalkClock的方法才能够构造TimePrinter对象，只有内部类可以是私有类，而常规类只可以具有包可见性，或公有可见性
    class TimePrinter implements ActionListener{
        public void actionPerformed(final ActionEvent event){
            final Date now=new Date();
            System.out.println("At the tone,the time is"+now);
            if(beep) Toolkit.getDefaultToolkit().beep();//实际这里是TalkClock.this.beep
        }
    }
}

