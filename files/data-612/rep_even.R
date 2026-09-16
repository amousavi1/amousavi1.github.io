#' Repeat Even Numbers and Replace Odd Numbers with Zeros
#'
#' This function takes a vector of natural numbers and creates a new vector
#' according to the following rules:
#'
#' * If an element is even, the element is repeated by its own value.
#' * If an element is odd, zero is repeated by the value of that element.
#'
#' For example, if the input is `c(2, 3, 4)`, the function returns
#' `c(2, 2, 0, 0, 0, 4, 4, 4, 4)`.
#'
#' @param x A numeric vector containing natural numbers (positive integers).
#'
#' @return A numeric vector constructed by repeating each even number by
#'   its value and replacing each odd number with the same number of zeros.
#'
#' @examples
#' rep_even(c(2, 3, 4))
#' # Returns: 2 2 0 0 0 4 4 4 4
#'
#' rep_even(c(1, 2, 5))
#' # Returns: 0 2 2 0 0 0 0 0
#'
#' @export
rep_even <- function(x) {
  
  # Check that every element of x is a natural number.
  # An element is invalid if it is less than 1 OR if it has a
  # nonzero remainder when divided by 1 (meaning it is not an integer).
  if (any((x < 1) | (x %% 1 != 0))) {
    stop("All elements of input must be natural numbers!")
  }
  
  # Initialize an empty vector.
  # We will add the results for each element of x to this vector.
  z <- NULL
  
  # Loop through the positions of the input vector.
  for (i in 1:length(x)) {
    
    # Check whether the current element is even.
    # An even number has remainder 0 when divided by 2.
    if (x[i] %% 2 == 0) {
      
      # If x[i] is even, repeat it x[i] times.
      rep_x_i_even <- rep(x[i], x[i])
      
      # Append these values to the output vector.
      z <- c(z, rep_x_i_even)
      
    } else {
      
      # If x[i] is odd, create x[i] zeros instead.
      rep_x_i_odd <- rep(0, x[i])
      
      # Append the zeros to the output vector.
      z <- c(z, rep_x_i_odd)
    }
  }
  
  # Return the completed vector.
  return(z)
}
