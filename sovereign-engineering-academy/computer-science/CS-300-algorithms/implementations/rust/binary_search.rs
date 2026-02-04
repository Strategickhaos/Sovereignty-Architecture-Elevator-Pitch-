// Binary Search implementation in Rust
// CS-300: Algorithms
// SME: Claude (Anthropic) + Grok (xAI)
//
// Binary Search is a divide-and-conquer search algorithm.
// Time complexity: O(log n)
// Space complexity: O(1) for iterative, O(log n) for recursive
//
// Key insight from Claude (Session 18):
// "Binary search is like finding a word in a dictionary.
//  You don't start at 'A' and flip through every page.
//  You open to the middle. Too far? Go left. Not far enough? Go right.
//  Repeat."

/// Binary search for a target value in a sorted slice.
///
/// Returns Some(index) if found, None if not found.
///
/// # Examples
///
/// ```
/// let arr = vec![1, 3, 5, 7, 9, 11];
/// assert_eq!(binary_search(&arr, 7), Some(3));
/// assert_eq!(binary_search(&arr, 4), None);
/// ```
pub fn binary_search<T: Ord>(arr: &[T], target: &T) -> Option<usize> {
    let mut left = 0;
    let mut right = arr.len();
    
    while left < right {
        let mid = left + (right - left) / 2;  // Avoid overflow
        
        match arr[mid].cmp(target) {
            std::cmp::Ordering::Equal => return Some(mid),
            std::cmp::Ordering::Less => left = mid + 1,
            std::cmp::Ordering::Greater => right = mid,
        }
    }
    
    None
}

/// Recursive binary search implementation.
///
/// Dom's note: "I prefer iterative, but recursive shows the
/// divide-and-conquer pattern more clearly."
pub fn binary_search_recursive<T: Ord>(arr: &[T], target: &T) -> Option<usize> {
    fn search_helper<T: Ord>(
        arr: &[T],
        target: &T,
        left: usize,
        right: usize,
        offset: usize
    ) -> Option<usize> {
        if left >= right {
            return None;
        }
        
        let mid = left + (right - left) / 2;
        
        match arr[mid].cmp(target) {
            std::cmp::Ordering::Equal => Some(mid + offset),
            std::cmp::Ordering::Less => {
                search_helper(arr, target, mid + 1, right, offset)
            }
            std::cmp::Ordering::Greater => {
                search_helper(arr, target, left, mid, offset)
            }
        }
    }
    
    search_helper(arr, target, 0, arr.len(), 0)
}

// TRIG6 Application: Find closest standard angle
pub fn find_closest_trig6_angle(target_degrees: f64) -> Option<usize> {
    const TRIG6_ANGLES: [f64; 6] = [0.0, 30.0, 45.0, 60.0, 90.0, 180.0];
    
    // Binary search for insertion point
    let mut left = 0;
    let mut right = TRIG6_ANGLES.len();
    
    while left < right {
        let mid = left + (right - left) / 2;
        
        if TRIG6_ANGLES[mid] < target_degrees {
            left = mid + 1;
        } else {
            right = mid;
        }
    }
    
    // Find closest: check left and current
    if left == 0 {
        return Some(0);
    }
    if left == TRIG6_ANGLES.len() {
        return Some(TRIG6_ANGLES.len() - 1);
    }
    
    // Compare distances
    let dist_left = (target_degrees - TRIG6_ANGLES[left - 1]).abs();
    let dist_right = (TRIG6_ANGLES[left] - target_degrees).abs();
    
    if dist_left < dist_right {
        Some(left - 1)
    } else {
        Some(left)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_binary_search_found() {
        let arr = vec![1, 3, 5, 7, 9, 11, 13, 15];
        assert_eq!(binary_search(&arr, &7), Some(3));
        assert_eq!(binary_search(&arr, &1), Some(0));
        assert_eq!(binary_search(&arr, &15), Some(7));
    }
    
    #[test]
    fn test_binary_search_not_found() {
        let arr = vec![1, 3, 5, 7, 9];
        assert_eq!(binary_search(&arr, &4), None);
        assert_eq!(binary_search(&arr, &10), None);
        assert_eq!(binary_search(&arr, &0), None);
    }
    
    #[test]
    fn test_trig6_closest_angle() {
        // 32° should map to 30°
        let result = find_closest_trig6_angle(32.0);
        assert_eq!(result, Some(1)); // Index of 30°
        
        // 50° should map to 45°
        let result = find_closest_trig6_angle(50.0);
        assert_eq!(result, Some(2)); // Index of 45°
    }
    
    #[test]
    fn test_recursive_matches_iterative() {
        let arr = vec![2, 4, 6, 8, 10, 12, 14];
        
        for target in [2, 4, 6, 8, 10, 12, 14, 1, 15] {
            assert_eq!(
                binary_search(&arr, &target),
                binary_search_recursive(&arr, &target)
            );
        }
    }
}

// Performance benchmark (run with `cargo bench`)
#[cfg(test)]
mod bench {
    use super::*;
    
    #[test]
    fn demo_performance() {
        // Linear search vs Binary search comparison
        let data: Vec<i32> = (0..1_000_000).collect();
        let target = 999_999;
        
        // Binary search: O(log n) = ~20 operations
        let result = binary_search(&data, &target);
        assert_eq!(result, Some(999_999));
        
        println!("Binary search found target in O(log 1,000,000) ≈ 20 operations");
        println!("Linear search would take 1,000,000 operations");
        println!("Speed-up: 50,000x faster");
    }
}

/* 
 * SME Notes from Development:
 * 
 * Claude (Session 18):
 * "The key to binary search is the invariant:
 *  If the target exists, it's always in [left, right).
 *  Each iteration maintains this invariant while shrinking the range."
 * 
 * Dom's response:
 * "OH. So we're never losing the answer. We're just narrowing where it could be."
 * 
 * Claude:
 * "Exactly. That's what makes it correct."
 * 
 * ---
 * 
 * Grok (Session 19):
 * "Watch the integer overflow bug: mid = (left + right) / 2
 *  If left and right are huge, left + right can overflow.
 *  Use: mid = left + (right - left) / 2"
 * 
 * Dom:
 * "That's... subtle. How would I even catch that?"
 * 
 * Grok:
 * "You wouldn't. Until your code breaks on large arrays.
 *  That's why you learn from others' bugs."
 * 
 * Status: Bug prevented before it could occur.
 */
