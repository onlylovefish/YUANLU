//内部类可以访问该类定义所在的作用域中的数据，包括私有的数据
// 内部类可以对同一个包中的其他类隐藏起来
// 当想要定义一个回调函数且不想编写大量代码时，使用匿名内部类比较便捷
import java.awt.*;
import java.awt.event.*;
import java.util.*;
//import javax.swing.*;
import javax.swing.Timer;

//import sun.swing.PrintColorUIResource;

/**
 * this program demonstrates the use of inner clsses
 */
public class InnerClassTest{
    public static void main(String[] args) {
        TalkingClock clock=new TalkingClock(1000,true);
        clock.start();
    }
   

}
class TalkingClock{
    private int interval;
    private boolean beep;
    /**
     * construct a talking clock
     */
    public TalkingClock(int interval,boolean beep){
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
    //TimePrinter类位于TalkingClock类内部，
    public class TimePrinter implements ActionListener{
        public void actionPerformed(ActionEvent event){
            Date now=new Date();
            System.out.println("At the tone,the time is"+now);
            if(beep) Toolkit.getDefaultToolkit().beep();
        }
    }
}