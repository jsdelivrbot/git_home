import java.util.*;

public class FindKthSmallest {
    public static int Finder (List<Integer> A, List<Integer> B, int k) {
        // Lower bound of elements we will choose in A.
        int b = Math.max(0, k-B.size());
        // Upper bound of elements we will choose in A.
        int t = Math.min(A.size(), k);
        
        while (b < t){
            int x = b + ((t-b)/2);
            int ax1 = (x <= 0 ? Integer.MIN_VALUE : A.get(x-1));
            int ax = (x >= A.size() ? Integer.MAX_VALUE : A.get(x));
            int bkx1 = (k - x <= 0 ? Integer.MIN_VALUE : B.get(k-x-1));
            int bkx = (k-x >= B.size() ? Integer.MAX_VALUE : B.get(k-x));
            
            if (ax < bkx1) {
                b = x + 1;
            } else if (ax1 > bkx) {
                t = x - 1;
            } else {
                return Math.max(ax1, bkx1);
            }
        }
    int ab1 = b <= 0 ? Integer.MIN_VALUE : A.get(b-1);
    int bkb1 = k - b - 1 < 0 ? Integer.MIN_VALUE : B.get(k-b-1);
    return Math.max(ab1, bkb1);
    }

    public static int anotherFinder(List<Integer> A, List<Integer> B, int k) {
        int low = Math.max(0, k-B.size());
        int high = Math.min(A.size(), k);

        while (low < high) {
            int mid = low + (high-low)/2;
            int A_mid = (mid > 0 ? A.get(mid-1) : Integer.MIN_VALUE);
            int A_mid_next = (mid < A.size() ? A.get(mid) : Integer.MAX_VALUE);
            int B_guess = (k - mid - 1 < B.size() ? B.get(k-mid-1) : Integer.MIN_VALUE);
            int B_guess_next = (k - mid < B.size() ? B.get(k-mid) : Integer.MAX_VALUE);
            
            if (A_mid_next < B_guess){
                low = mid + 1;
            } else if (A_mid > B_guess_next) {
                high = mid - 1;
            } else {
                return Math.max(A_mid, B_guess);
            }
        }
        
        int A_last = (low > 0 ? A.get(low-1) : Integer.MIN_VALUE);
        int B_last = (k-low > 0 ? B.get(k-low-1) : Integer.MIN_VALUE);
        return Math.max(A_last, B_last);
    }
    
    public static void main (String[] args){
        List<Integer> A = new ArrayList<Integer>(Arrays.asList(10, 13, 14, 16, 22, 34));
        List<Integer> B = new ArrayList<Integer>(Arrays.asList(9, 10, 12, 30, 32, 32, 35));
        for (int k=1; k<=13; k++){
            System.out.println(Finder(A, B, k)+"\t"+anotherFinder(A, B, k));
        }
    }
}
