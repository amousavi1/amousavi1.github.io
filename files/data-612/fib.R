#' Compute the nth Fibonacci Number
#'
#' This function computes the nth number in the Fibonacci sequence.
#' The Fibonacci sequence starts with 1 and 1, and every subsequent
#' number is obtained by adding the previous two numbers.
#'
#' For example, the first few Fibonacci numbers are:
#' 1, 1, 2, 3, 5, 8, 13, ...
#'
#' @param n A positive integer indicating the position in the
#'   Fibonacci sequence.
#'
#' @return The nth Fibonacci number.
#'
#' @examples
#' fib(1)
#' # Returns: 1
#'
#' fib(6)
#' # Returns: 8
#'
#' fib(7)
#' # Returns: 13
#'
#' @export
fib <- function(n) {
  
  # Check that n is a positive integer.
  # n %% 1 == 0 checks that n has no decimal part.
  # n > 0 checks that n is positive.
  # stopifnot() stops the function with an error if the
  # condition is not satisfied.
  stopifnot(n %% 1 == 0 & n > 0)
  
  # The first and second Fibonacci numbers are both 1.
  # Since we already know the answer for these two cases,
  # return 1 immediately without running the rest of the function.
  if (n <= 2) {
    return(1)
  }
  
  # Create a numeric vector of length n.
  # numeric(n) initially creates:
  # 0, 0, 0, ..., 0
  # We will use this vector to store the Fibonacci numbers
  # as they are calculated.
  f <- numeric(n)
  
  # Set the first two Fibonacci numbers.
  f[1] <- 1
  f[2] <- 1
  
  # Starting from the third position, calculate each Fibonacci
  # number by adding the previous two numbers.
  for (i in 3:n) {
    f[i] <- f[i - 1] + f[i - 2]
  }
  
  # f now contains the Fibonacci sequence up to position n.
  # Return only the nth Fibonacci number.
  return(f[n])
}
