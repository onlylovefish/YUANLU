import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.PrintWriter;

import jdk.nashorn.internal.parser.Scanner;

//创建异常类,异常类包含两个构造器，一个是默认的构造器，还有一个是带有详细描述信息的构造器
/**
 * Throwable()
 * Throwable(String message)
 * String getMessage()
 */
class FileFormatException extends IOException{
    public FileFormatException(){}
    public FileFormatException(String gripe){
        super(gripe);
    }
}

/**
 * try-catch代码演示
 */
public void read(String filename){
    try{
        InputStream in=new InputStream(filename);
        int b;
        while(b=in.read()!=-1)
            System.out.println("not -1");
            
    }
    catch(IOException exception){
        exception.printStackTrace();
    }
}
/**
 * 改进：抛出的异常让调用者操心,此外不允许在子类的throws说明符中出现超过超类方法所列出的异常类范围
 */
public void read1(String filename) throws IOException{
    InputStream in=new InputStream(filename);
    int b;
    while(b=in.read()!=-1)
        System.out.println("not -1");
}
/**
 * 捕获多个异常
 * try{
 * code that might throw exceptions}
 * catch(fileNotFoundException e){}
 * catch(UnknownHostException e){}
 * catch(IOException e){}
 * 通过e.getMessage()得到详细的错误信息，或者使用e.getClass().getName()得到异常对象的实际类型
 */

 /**
  * 再次抛出异常与异常链，在catch语句中可以抛出一个异常，可以改变异常的类型，例如ServletException，用带有异常信息文本的构造器来构造
  */
  try{
      access the database
  }
  catch(SQLException e){
      Throwable se=new ServletException("database error");
      se.initCause(e);
      throw se;
  }
  //当捕获到异常时就可以用se.getCause();重新得到原始异常
//这种包装技术，很有效，比如我们只想记录一个异常，再将它重新抛出，而不做任何改变
try{
    access the database
}
catch(Exception e){
    logger.log(level,message,e);
    throw e;
}

/**
 * 关于finally语句，当代码抛出一个异常时，就会终止方法中剩余代码的处理，并推出这个方法的执行，并且例如在方法使用了资源，资源需要被回收时
 * Finally{
 *  in.close()
 * }
 */

 /**
  * 带有资源的try块
  open a resource
  try{
      work with the resource
  }
  finally{
      close the resource
  }

  最简形式为：
  try(Resource res=……){
      work with res
  }
  try块退出时，会自动调用res.close(),这个块正常退出时，或者存在一个异常时，都会调用in.close()方法，就好像使用了finally块一样
  */
  try(java.util.Scanner in=new Scanner(new FileInputStream(file))){
      while(in.hasNext())
        System.out.println(in.next());
  }


  try(java.util.Scanner in=new Scanner(new FileInputStream(file)));
  PrintWriter out=new PrintWriter("out.txt"){
    while(in.hasNext())
      System.out.println(in.next().toUpperCase());
  }