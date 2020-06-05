/**
 * 关于堆栈跟踪，时一个方法调用过程的列表，它包含了程序执行过程中方法调用的特定位置，当java程序正常终止时，这个列表就是显示
 * 可以调用Throwable类的printStackTrace方法访问堆栈跟踪的文本描述信息
 */
    
    ''' java
    Throwable t=new Throwable();

    StringWriter out=new StringWriter();

    t.printStackTrace(new PrintWriter(out));

    String description=out.toString();



'''

//一种更灵活的方式是使用getStackTrace方法访问堆栈跟踪的文本描述信息
Throwable t=new Throwable();
StackTraceElement[] frames=t.getStackTrace();
for(StackTraceElement frame:frames)
analyze frame
/**
 * stackTraceElement类含有能够获得文件名和当前执行的代码行号的方法，同时还含有能够获得类名和方法名的方法，toString方法将产生一个格式化的字符串，其中包含所跟踪的信息
 * 静态的Thread.getAllStackTrace方法，可以产生所有线程的堆栈跟踪
 */

    '''

    Map<Thread,StackTraceElement[]> map=Thread.getAllStackTraces();

    for(Thread t:map.keySet()){

    StackTraceElement[] frames=map.get(t);
    
    analyze
}

