public void start(int interval,final boolean beep){
    ActionListener listener=new ActionListener(){
        public void actionPerformed(ActionEvent event){
            Date now=new Date();
            System.out.println("At the tone, the time is"+now);
            if(beep)Toolkit.getDefaultToolkit().beep();
        }
    };
    Timer t=new Timer(interval,listener);
    t.start();
}
/**
 * 它的涵义为，创建一个实现ActionListener接口的类的新对象，需要实现的方法actionPerformed定义在括号{}内
 * 如果构造参数的闭圆括号跟一个开花括号，正在定义的就是匿名内部类
 */
import ArrayList;
import java.lang.String;
 //双花括号初始化
 ArrayList<String> friends=new ArrayList<>();
 friends.add("Harry");
 friends.add("Tony");

 /**
  * 如果不需要这个类，则将其作为匿名列表，作为匿名列表，应该如下添加元素
  */
  invite(new ArrayList<String>() {{add("Harry");add("Tony"); }})//外层括号建立了一个匿名子类，内层括号则是一个对象构造块

  /**
   * 生成日志或者调试信息时，通常希望包含当前类的类名
   * System.out.println("Something awful happened in"+getClass());
   * 不过这对于静态方法并不奏效，因为调用getClass时调用的是this.getClass()
   */ 

   /**
    * 有时候，使用内部类只是为了将一个类隐藏在另一个类的内部，并不需要内部类引用外围类对象，此时可以将内部类声明为static,以便取消产生的引用
    */
    /**
     * 比如下面，想要遍历一次数组，返回最大和最小，这样返回的时候，会由两个值，那么通过写一个类，将两个值放到这个类函数中，使得它只返回一个
     */
    public class StartcInnerClassTest{
        public static void main(String[] args){
            double[] d=new double[20];
            for(int i=0;i<d.length;i++)
                d[i]=100*Math.random();
                //因为pair类这个名字很大众化，所以为了解决名字冲突问题，将Pair定义为ArrayAlg的内部公有类，通过ArrayAlg.Pair来访问它
            ArrayAlg.Pair p=ArrayAlg.minmax(d);
            System.out.println("min="+p.getFirst());
            System.out.println("max="+p.getSecond());
        }
    }
    class ArrayAlg{
        /**
         * A pair of floating-point numbers
         */
        public static class Pair{
            private double first;
            private double second;
            public Pair(double f,double s){
                first=f;
                second=s;
            }
            public double getFirst(){
                return first;
            }
            public double getSecond(){
                return second;
            }
        }
        public static Pair minmax(double[] values){
            double min=Double.MAX_VALUE;
            double max=Double.MIN_VALUE;
            for(double v:values){
                if(min>v) min=v;
                if(max<v) max=v;
            }
            return new Pair(min,max);
        }
    }