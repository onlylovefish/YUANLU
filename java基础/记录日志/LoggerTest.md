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

## 如果多个应用程序（或者是同一个应用程序的多个副本）使用同一个日志文件，就应该开启append标志，另外，应该再文件模式中使用%u,以便每个应用程序创建日志的唯一副本。
## 关于日志文件的配置问题，具体参数，参看文件处理器配置参数的表

## 过滤器
再默认情况下，过滤器会根据日志级别来进行过滤，每个日志记录器和处理器都可以有一个可选的过滤器来完成附加的过滤。另外可以通过实现fliter接口并定义方法来自定义过滤器：
boolean isLoggable(LogRecord record),将一个过滤器安装到一个日志记录器或者处理器中，只需要调用setFilter方法就可以了，同一时间最多只能安装一个过滤器。
## 格式化器
ConsleHandler类和FileHandler类可以生成文本和XML格式的日志记录，但是也可以自定义格式，这需要扩展Formatter类并覆盖下面这个方法：

String format(LogRecord record)可以根据自己的愿望对记录中的信息进行格式化，并返回结果字符串 String formatMessage(LogRecord record)对记录中的部分消息进行格式化，参数替换和本地化应用操作。调用setFormatter方法将格式化器安装到处理器中

## 日志记录说明
将日志记录器命名为与主应用程序包一样的名字，可以通过调用Logger logger=Logger.getLogger("com.mycompany.myprog")得到日志记录器

默认的日志配置将级别等于或高于INFO级别的所有消息记录到控制台
下面的程序是将所有的消息记录到应用程序特定的文件中，将下面的放到程序的main方法中

    '''java
    if(System.getProperty("java.util.logging.config.class")==null&&System.getProperty("java.util.logging.config.file")==null){
        try{
            Logger.getLogger("").setLevel(Level.ALL);
            final int LOG_ROTATION_COUNT=10;
            Handler handler=new FileHandler("%h/myapp.log",0,LOG_ROTATION_COUNT);
            Logger.getLogger("").addHandler(handler);
        }
        catch(IOException e){
            logger.log(Level.SEVERE,"Can't create log file handler",e);
        }
    }
    '''

将程序员想要的日志记录设置为FINE




