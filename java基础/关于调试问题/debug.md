# 调试技巧：

可以启动编辑器自带的调试器，另外可以在启用调试之前，用下面的方法打印或记录任意变量的值：

    '''
    System.out.println("x="+x);
    或者：
    Logger.getGlobal().info("x="+x);
如果x是一个数值，则会被转换成等价的字符串，如果x是一个对象，那么java就会调用这个对象的toString方法，要想获得隐式参数对象的状态，就可以打印this这个对象的状态.
    
    '''
    Logger.getGlobal().info("this+"=this);

可以在每个类中放置一个main方法，这样就可以对每一个类进行单元测试

可以在代码的任何位置插入Thread.dumpStack();生成堆栈跟踪

    '''通过下面方法将堆栈跟踪和记录信息，捕获到一个字符串中
    ByteArrayOutputStream out=new ByteArrayOutputStream();
    new Throwable().printStackTrace(out);
    String description=out.toString();
//一般情况下，堆栈跟踪的信息将显示在System.err上，也可以利用printStackTrace(PrintWriter s)方法将它发送到一个文件中

通常情况下，错误信息被发送到System.err中，而不是System.out中，所以采用java MyProgram 2>errors.txt,想在同一个文件中同时捕获System.err和System.out，需要如下:
java MyProgram 1>errors.txt 2>&1

