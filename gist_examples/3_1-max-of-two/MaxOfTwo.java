/**
 * Java Reference Implementation: Maximum of Two Numbers
 * Demonstrates basic if-else branching logic
 */
public class MaxOfTwo {
    
    /**
     * Returns the maximum of two integer values.
     * 
     * @param a First integer value
     * @param b Second integer value
     * @return The larger of the two values
     */
    public static int maxOfTwo(int a, int b) {
        if (a > b) {
            return a;
        } else {
            return b;
        }
    }
    
    /**
     * Test driver for maxOfTwo function
     */
    public static void main(String[] args) {
        // Test case 1: First value is smaller
        System.out.println("max(5, 7) = " + maxOfTwo(5, 7)); // Expected: 7
        
        // Test case 2: Second value is negative
        System.out.println("max(10, -3) = " + maxOfTwo(10, -3)); // Expected: 10
        
        // Test case 3: Both values are equal
        System.out.println("max(4, 4) = " + maxOfTwo(4, 4)); // Expected: 4
    }
}
