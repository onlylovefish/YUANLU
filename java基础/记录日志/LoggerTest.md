## 综述：
日志系统管理着一个名为Logger.global的默认日志记录器，可以用System.out替换它，并通过调用info方法记录日志信息，可以用System.out替换它，并通过调用info方法记录日志信息

Logger.getGlbal().info("File->open menu item selected");
会自动包含时间，调用的类名和方法名

## 高级日志：
企业级的日志，不要将所有的日志都记录到一个全局日志记录器中，二十可以自定义日志记录器
private static final Logger myLogger=Logger.getLogger("com.mycompany.myapp")

默认的日志配置记录了INFO或更高级别的所有记录

默认的日志记录将显示包含日志调用的类名和方法名，如同堆栈所显示的那样，但是如果虚拟机对执行过程进行了优化，就得不到准确的调用信息，此时可以调用logp方法获得调用类和方法的确切位置

该方法的签名为：void logp(Level 1,String className,String methodName,String message);

### 例如：
    '''java
    int read(String file,String pattern){
        logger.entering("com.mycompany.mylib.Reader","read",new Object[]{file,pattern});
        ...
        logger.exiting("com.mycompany.mylib.Reader","read",count);
        return count;
    }
    这些调用将生成FINER级别和以字符串”ENTRY“和RETURN开始的日志记录 
    
    '''

## 使用日志的常见用途就是记录那些不可预料的异常，例如：
    '''java
    if(...){
        IOException exception=new IOException("...");
        logger.throwing("com.mycompany.mylib.Reader","read",exception);
        throw exception;
    }
    //或者
    try{
        ...
    }
    catch(IOException e){
        Logger.getLogger("com.mycompany.myapp").log(Level.WARNING,"Reading image",e);
    }

## 修改日志管理器配置
可以通过编辑配置文件来修改日志系统的各种属性，在默认情况下，配置文件存在于：jre/lib/logging.properties,如果想使用另一个配置文件，就要将java.util.logging.config.file特性置为配置文件的存储位置，并用下列命令启动应用程序:java -Djava.util.logging.config.file=configFile MainClass
日志管理器在VM启动过程中被初始化，会在main之前执行。
可以通过这样的方式指定自己日志记录级别：

com.mycompany.myapp.level=FINE,也就是说，在日志文件名后面添加后缀.level

如果想在控制台上看到FINE级别的消息，可以像如下设置：

java.util.logging.ConsoleHandler.level=FINE

### 日志属性文件由java.util.logging.LogManager类处理，可以通过将java.util.logging.manager系统属性设置为某个子类的名字来指定一个不同的日志管理器

## 日志记录器会将记录发送到ConsoleHandler中并由它输出到System.error流中，还会将其发送到父处理器中
日志管理器配置文件设置的默认控制台处理器的日志记录级别为：java.util.logging.ConsoleHandler.level=INFO

如果你想记录FINE级别的日志，则必须修改配置文件中的默认日志记录级别和处理器级别。另外，还可以绕过配置文件，安装自己的处理器
    
    '''java
    Logger logger=Logger.getLogger("com.mycompany.myapp");
    logger.setlevel(Level.FINE);
    logger.setUseParentHandlers(false);//这里应该就是绕过了配置文件
    Handler handler=new ConsoleHandler();//新建自己的处理器
    handler.setLevel(Level.FINE);//设置处理器处理的日志级别
    logger.addHandler(handler);//将该处理器加入到处理器中 
    '''

## 将日志记录发送到其他地方，，默认的会发送到控制台
日志API提供了两个很有用的处理器，一个是FileHandler,另一个是SocketHandler,SocketHandler将记录发送到特定的主机和端口，FileHandler则会收集文件中的记录

    '''java
    FileHandler handler=new FileHandler();
    logger.add(handler);
    //这些记录会被发送到用户主目录的javan.log文件中，n是文件名的唯一编号，在默认情况下，文件就存储在C:\windows这样的默认位置上。默认情况下，记录被格式化为XML









