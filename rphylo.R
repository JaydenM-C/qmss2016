# returns a randomly generated label which sounds like a one to three
# syllable word; should be pronounceable in most cases; the returned
# label is guaranteed to be different from those is 'prev.labels'
rlabel <- function(prev.labels = c()) {
  # starting label
  label <- ''
  
  
  # models; empty strings are used for absence, repeated values
  # give more weight to an option
  first.cons <- c('p', 'b', 't', 'd', 'k', 'g', 's', 'z', 'r')
  vowel <- c('a', 'ai', 'e', 'i', 'o', 'oi', 'u', 'ui')
  second.cons <- c('s', 'r', 'l', 'n', '', '')
  
  # generate a random number of "syllables", between 1 and 3,
  # with a bias towards 2-syllable words
  syls <- sample(c(1, 2, 2, 2, 3), 1)
  for (i in 1:syls) {
    label <- paste0(label,
                    sample(first.cons, 1),
                    sample(vowel, 1),
                    sample(second.cons, 1))
    
  }
  
  
  # check if the current label has not been used, calling this function
  # again if positive; please note that this could, in theory, get stuck
  # in a loop
  if (label %in% prev.labels) {
    label <- rlabel(prev.labels)
  }
  
  # return the new random label
  label
  
}

# returns a dataframe with randomly generated data for phylogenetic
# analysis; 'vars' is a vector with the type of variables to be
# included, provided as characters ('b'-binary, 's'-state,
# 'c'-continous, 'r'-random) and 'comp' a vector with complementary
# definitions for random variable generation
rphylo <- function(vars, comp, depth, split.mean, split.sd, tm.diag) {
  # set random, suitable values for 'vars' and 'comp' if not provided
  # by the user
  if (missing(vars)) {
    vars <- c('r', 'b', 'b', 'b', 's', 'c')
    comp <- c( NA,  NA, NA,   NA,   7,  10)
  }
  
  # set a random depth level for tree, if none is provided by the user
  if (missing(depth)) {
    depth <- floor(rnorm(1, 7.5, 3))
  }
  
  
  # set the mean and standard deviation for random number of splits,
  # if not provided by the user; these values try to mimic the
  # behaviour of trees for cultural and linguistic history
  if (missing(split.mean)) {
    split.mean <- 2.0
  }
  
  if (missing(split.sd)) {
    split.sd <- 1.0
  }
  
  # set the reference value for transition matrices diagonals, if
  # non is provided by the user
  if (missing(tm.diag)) {
    tm.diag <- 0.95
  }
  
  
  # set transition matrix for all variables where required and where the
  # matrix is not provided; this random setting also sets the matrix
  # diagonal to a high value, in order to guarantee that transitions are
  # conservative in terms of changes (otherwise, we likely end up with states
  # that jump continously back and forth, which is not a good model for
  # human behaviour evolution)
  tm <- list()
  for (i in 1:length(vars)) {
    if (vars[i] == 'b') {
      # binary
      tmp <- matrix(runif(2 * 2), nrow = 2, ncol = 2)
      diag(tmp) <- 0.95
      colnames(tmp) <- 1:2
      rownames(tmp) <- 1:2
      tm[[i]] <- tmp
    } else if (vars[i] == 's') {
      # state
      tmp <-
        matrix(runif(comp[i] * comp[i]), nrow = comp[i], ncol = comp[i])
      diag(tmp) <- comp[i] * (0.95 / 2)
      colnames(tmp) <- 1:comp[i]
      rownames(tmp) <- 1:comp[i]
      tm[[i]] <- tmp
    } else {
      # no transition matrix needed
      tm[[i]] <- NA
    }
  }
  
  # add the root node, with label, variables, depth count and
  # true direct ancestor (if any)
  df <- data.frame(label = rlabel(), stringsAsFactors = FALSE)
  for (i in 1:length(vars)) {
    var.name <- paste0('var', i)
    if (vars[i] == 'r') {
      # random number
      df[, var.name] <- runif(1)
    } else if (vars[i] == 'b') {
      # binary
      df[, var.name] <- sample(1:2, 1) # changed to T/F later
    } else if (vars[i] == 's') {
      # state
      df[, var.name] <- sample(1:comp[i], 1)
    } else if (vars[i] == 'c') {
      # continuous
      df[, var.name] <- floor(rnorm(1, mean = 0, sd = comp[i]))
    }
  }
  df$depth <- 0
  df$ancestral <- NA
  
  # depth-1 because we are counting from zero, making the root
  # depth==0
  for (cur.depth in 1:(depth - 1)) {
    # select only states from the previous depth
    ancestrals <- subset(df, depth == cur.depth - 1)
    
    # makes easier to undestand than apply() and by()
    for (a in 1:nrow(ancestrals)) {
      ancestral <- ancestrals[a, ]
      
      
      # number of random splits, guaranteeing at least one split for
      # the root; in case of zero splits, the branch "dies"
      splits <- floor(rnorm(1, mean = split.mean, sd = split.sd))
      
      if (cur.depth == 1) {
        splits <- max(1, splits)
        
      } else {
        splits <- max(0, splits)
        
      }
      
      for (s in 1:splits) {
        # initiates row with a new random label, guaranteed to be unique
        row <- c(rlabel(df$label))
        # iterate vars
        for (i in 1:length(vars)) {
          if (vars[i] == 'r') {
            # random number
            row <- c(row, runif(1))
          } else if (vars[i] == 'b') {
            # binary
            state <- ancestral[[i + 1]] # i+1, as first row is 'label'
            trans <- tm[[i]][state, ]
            row <- c(row, sample(1:2, 1, prob = trans)) # changed to T/F later
          } else if (vars[i] == 's') {
            # state
            state <- ancestral[[i + 1]] # i+1, as first row is 'label'
            trans <- tm[[i]][state, ]
            row <- c(row, sample(1:comp[i], 1, prob = trans))
          } else if (vars[i] == 'c') {
            # continous
            m <- as.numeric(ancestral[[i + 1]]) # i+1, as first row is 'label'
            v <- floor(rnorm(1, mean=, sd=comp[i]))
            row <- c(row, v)
          }
        }
        
        # add current depth and ancestor
        row <- c(row, cur.depth, ancestral$label)
        
        # add row to dataframe
        df <- rbind(df, row)
      }
      
    }
    
    # borrowing/HGT implementation should go here
    
  }
  
  # turn all 1:2 variables into binary features
  for (i in 1:length(vars)) {
    if (vars[i] == 'b') {
      # i+1 because the first var in the dataframe is the 'label'
      df[, i + 1] <- df[, i + 1] == 2
    }
  }
  
  # set labels as row names
  df <- data.frame(df[, -1], row.names = df[, 1])
  
  # return the data frame
  df
  
}