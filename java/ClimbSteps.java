import java.util.Scanner;

public class ClimbSteps {
    public static int[] A = new int[100];
    
    public static int f3(int n) {
        if (n <= 2)
            A[n] = n;
        if (A[n] > 0)
            return A[n];
        else
            A[n] = f3(n-1) + f3(n-2);
        return A[n];
    }

    public static void main (String[] args){
        Scanner scan = new Scanner(System.in);
        System.out.println("Enter a number:");
        int n = scan.nextInt();
        System.out.println(f3(n));
    }
}

