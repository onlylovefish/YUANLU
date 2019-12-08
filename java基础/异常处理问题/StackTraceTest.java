import java.util.Scanner;

/**
 * a program that displays a trace feature of a recursive method call
 */
public class StackTraceTest {
    public static int factorial(final int n) {
        System.out.println("factorial(" + n + "):");
        final Throwable t = new Throwable();
        final StackTraceElement[] frames = t.getStackTrace();
        for (final StackTraceElement f : frames)
            System.out.println(f);
        int r;
        if (n <= 1)
            r = 1;
        else {
            r = n * factorial(n - 1);
        }
        System.out.println("return" + r);
        return r;
    }

    public static void main(String[] args) {
        // Scanner in = new Scanner(System.in);
        Scanner in = new Scanner(System.in);
        System.out.println("Enter n:");
        final int n = in.nextInt();
        factorial(n);
    }
}