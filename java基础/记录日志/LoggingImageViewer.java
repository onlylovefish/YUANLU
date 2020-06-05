import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.util.logging.*;
import javax.swing.*;
import javax.swing.filechooser.FileFilter;

import sun.net.www.content.text.plain;
import sun.util.logging.resources.logging;
public class LoggingimageViewer{
    public static void main(String[] args) {
        if(System.getProperty("java.util.logging.config.class")==null&&System.getProperty("java.util.logging.config.file")==null){
            try{
                Logger.getLogger("com.horstmann.corejava").setLevel(Level.ALL);
                final int LOG_ROTATION_COUNT=10;
                Handler handler=new FileHandler("%h/myapp.log",0,LOG_ROTATION_COUNT);
                Logger.getLogger("com.horstmann.corejava").addHandler(handler);
            }
            catch(IOException e){
                logger.getLogger("com.horstmann.corejava").log(Level.SEVERE,"Can't create log file handler",e);
            }
        }
        EventQueue.invokeLater(new Runnable(){
            public void run(){
                Handler windowHandler=new WindowHandler();
                windowHandler.setLevel(Level.ALL);
                Logger.getLogger("com.horstmann.corejava").addHandler(windowHandler);
                JFrame frame=new ImageViewFrame();
                frame.setTitle("LoggingImageViewer");
                frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                Logger.getLogger("com.horstmann.corejava").fine("showing frame");
                frame.setVisible(true);
            }
        }
        );
    }
}
/**
 * the frame that show the image,由于java的UI已经过时了，这块就不写了，主要了解整个日志机制
 */
class ImageViewFrame extends JFrame{
   private static Logger logger=Logger.getLogger("com.horstmann.corejava");
   public ImageViewFrame(){
       logger.entering("ImageViewzframe", "<init>");
       exitItem.addActionListener(new ActionListener(){
           public void actionPerformed(ActionEvent event){
               logger.fine("Exiting.");
               System.exit(0);
           }
       });
       logger.exiting("ImageViewerFrame", "<init>");
   }

private class FileOpenListener implements ActionListener{
    public void actionPerformed(ActionEvent event){
        logger.entering("ImageViewFrame.FileOpenListener","actionPerformed",event);
        //set up file chooser
        JFileChooser chooser=new JFileChooser();
        chooser.setCurrentDirectory(new File("."));
        //accept all files ending with .gif
        chooser.setFileFilter(new javax.swing.filechooser.FileFilter(){
        
            @Override
            public String getDescription() {
                // TODO Auto-generated method stub
                return "GIF Images";
            }
        
            @Override
            public boolean accept(File f) {
                // TODO Auto-generated method stub
                return f.getName().toLowerCase().endWith(".gif")||f.isDirectory();
            }

        });
        //show file chooser dialog
        int r=chooser.showOpenDialog(ImageViewrFrame.this);
        //if image file accpeted,set it as icon of the label
        if(r==JFileChooser.APPROVE_OPTION){
            String name=chooser.getSelectedFile().getPath();
            logger.log(Level.FINE,"Reading file{0}",name);
            label.setIcon(new ImageIcon(name));
        }
        else logger.fine("File open dialog canceled.");
        logger.exiting("ImageViewerFrame.FileOpenListener","actionPerformed");
    }
}
}
/**
 * A handler for displaying log records in a window
 */
class windowHandler extends StreamHandler{
    private 
}