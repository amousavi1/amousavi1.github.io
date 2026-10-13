#' Add a Value to the Second Half of a Vector
#'
#' This function takes a numeric vector x and adds y to the elements
#' in the second half of the vector.
#'
#' If x has an even number of elements, the vector is divided into
#' two equal halves. The first half remains unchanged, while y is
#' added to every element in the second half.
#'
#' If x has an odd number of elements, the middle element is treated
#' randomly: it either remains unchanged or has y added to it.
#' All elements before the middle remain unchanged, and all elements
#' after the middle have y added to them.
#'
#' @param x A numeric vector.
#' @param y A numeric value to be added to selected elements of x.
#'
#' @return A numeric vector with y added to the second half of x.
#'   If the length of x is odd, the middle element is randomly
#'   assigned to either the unchanged or modified half.
#'
#' @examples
#' add_half(c(1, 2, 3, 4, 5, 6), 10)
#' # Returns: 1 2 3 14 15 16
#'
#' add_half(c(1, 2, 3, 4, 5), 10)
#' # Returns either:
#' # 1 2 3 14 15
#' # or
#' # 1 2 13 14 15
#'
#' @export
add_half <- function(x, y) {
  
  # Find the number of elements in x.
  len_x <- length(x)
  
  # Check whether the length of x is even.
  # A number is even if its remainder after division by 2 is zero.
  if (len_x %% 2 == 0) {
    
    # When the length is even, divide x into two equal halves.
    #
    # 1:(len_x/2) selects the first half.
    # ((len_x/2)+1):len_x selects the second half.
    #
    # Leave the first half unchanged and add y to every
    # element in the second half.
    z <- c(
      x[1:(len_x/2)],
      x[((len_x/2) + 1):len_x] + y
    )
    
  } else {
    
    # If the length is odd, floor(len_x/2) gives the number
    # of elements that appear before the middle element.
    #
    # For example, if len_x = 5:
    # floor(5/2) = 2
    # so the middle element is at position 3.
    flr_x <- floor(len_x/2)
    
    # The middle element is x[flr_x + 1].
    #
    # Randomly choose between:
    #   1. leaving the middle element unchanged, or
    #   2. adding y to the middle element.
    #
    # sample(..., size = 1) randomly selects one of these
    # two possibilities.
    s <- sample(
      c(x[flr_x + 1], x[flr_x + 1] + y),
      size = 1
    )
    
    # Construct the final vector:
    #
    # 1. Keep all elements before the middle unchanged.
    # 2. Insert the randomly selected middle value, s.
    # 3. Add y to all elements after the middle.
    z <- c(
      x[1:flr_x],
      s,
      x[(flr_x + 2):len_x] + y
    )
  }
  
  # Return the resulting vector.
  return(z)
}
