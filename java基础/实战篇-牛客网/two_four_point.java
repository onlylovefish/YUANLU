import java.lang.annotation.ElementType;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Scanner;

java.util.*;
public class Game24Player{
    
    final String[] patterns = {"nnonnoo", "nnonono", "nnnoono", "nnnonoo","nnnnooo"};
    final String ops='+-*/^';
    String solution;
    List<Integer>digits;
    public static void main(String[] args) {
        new Game24Player().play();    
    }
    void play(){
        digits=getSolveableDigits();
        Scanner in=new Scanner(System.in);
        while(true){
            System.out.println("Make 24 using these digits:");
            System.out.println(digits);
            System.out.println("(Enter 'q' to quit,'s' for a solution)");
            System.out.println(">");

            String line=in.nextLine();
            // line.equalsIgnoreCase('q')的含义为忽略大小写的进行匹配
            if(line.equalsIgnoreCase('q')){
                System.out.println("\nThanks for playing");
                return;
            }
            if(line.equalsIgnoreCase('s')){
                System.out.println("solution");
                digits=getSolveableDigits();
                continue;
            }
            char[] entry=line.replaceAll("[^*+-/)(\\d]","").toCharArray();
            try{
                validate(entry);
                //evalute函数怎么评判
                if(evalute(infixToPostfix(entry))){
                    System.out.println("\nCorrect! want to try annother?");
                    digits=getSolveableDigits();
                }else{
                    System.out.println("\nNot correct");
                }
            }catch(Exception e){
                System.out.printf("%n%s Try again.%n",e.getMessage());
            }
        }
    }
    //进行数字的随机生成和排序
    List<Integer> getSolveableDigits(){
        List<Integer> result;
        do{
            result=randomDigits();
        }while(!isSolvable(result));
        return result;
    }

    void validate(char[] input) throws Exception{
        int total1=0,parens=0,opsCount=0;
        for(char c:input){
            if(Character.isDigit(c)) total1+=1<<(c-'0')*4;
            else if(c=='(') parens++;
            else if(c==')')parens--;
            else if(ops.indexOf(c)!=-1) opsCount++; 
            if(parens<0) throw new Exception("parentheses mismatch.");
        }
        if(parens!=0) throw new Exception("Parentheses mismatch");
        if(parens!=3) throw new Exception("Wrong number of operators.");
        int total2=0;
        for(int d:digits) total2+=1<<d*4;
        if(total1!=total2) throw new Exception("not the same digits.");
        }
    
    boolean evalute(char[] line) throws Exception{
        Stack<Float> s=new Stack<>();
        try{
            for(char c:line){
                if('0'<=c&&c<='9') s.push((float) c-'0');
                else s.push(applyOperator(s.pop(),s.pop(),c));
            }
        }catch(ExptyStackException e){
            throw new Exception("Invalid entry.");
        }
        return (Math.abs(24-s.peek())<0.001F);
    }

    float applyOperator(float a,float b,char c){
        switch(c){
            case '+':
            return a+b;
            case '-':
            return b-a;
            case '*':
            return a*b;
            case '/':
            return b/a;
            default:
            return Float.NaN;
        }
    }
    List<Integer>getSolvableDiList(){
        List<Integer>result;
        do{
            result=randomDigits();
        }while(!isSolvable(result));
        return result;
    }

    boolean isSolvable(List<Integer> digits){
        Set<List<Integer>> dPerms=new HashSet<>(4*3*2);
        permute(digits,dPerms,0);
        int total=4*4*4;
        List<List<Integer>> oPerms=new ArrayList<>(total);
        permuteOperators(oPerms,4,total);
        StringBuilder sb=new StringBuilder(4+3);
        for(String pattern:patterns){
            
        }
        }
}