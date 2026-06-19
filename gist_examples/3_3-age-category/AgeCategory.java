/**
 * Java Reference Implementation: Age Category Classification
 * Demonstrates chained if-else-if branching for range detection
 */
public class AgeCategory {
    
    /**
     * Categorizes a person's age into demographic groups.
     * 
     * Age ranges:
     * - invalid: age < 0
     * - child: 0-12
     * - teen: 13-19
     * - adult: 20-64
     * - senior: 65+
     * 
     * @param age The person's age in years
     * @return A string representing the age category
     */
    public static String ageCategory(int age) {
        if (age < 0) {
            return "invalid";
        } else if (age < 13) {
            return "child";
        } else if (age < 20) {
            return "teen";
        } else if (age < 65) {
            return "adult";
        } else {
            return "senior";
        }
    }
    
    /**
     * Test driver for ageCategory function
     */
    public static void main(String[] args) {
        // Test case 1: Invalid age
        System.out.println("ageCategory(-2) = " + ageCategory(-2)); // Expected: invalid
        
        // Test case 2: Child
        System.out.println("ageCategory(5) = " + ageCategory(5)); // Expected: child
        
        // Test case 3: Teen
        System.out.println("ageCategory(15) = " + ageCategory(15)); // Expected: teen
        
        // Test case 4: Adult
        System.out.println("ageCategory(35) = " + ageCategory(35)); // Expected: adult
        
        // Test case 5: Senior
        System.out.println("ageCategory(80) = " + ageCategory(80)); // Expected: senior
    }
}
