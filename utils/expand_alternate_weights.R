# Expands alternate CPS weights for year 2026 to all years.
# Uses the same ratio for original 2026 weight. Also multiplies by 100.

library(data.table)

orig.weights <- data.table(read.csv("~/cps_weights.csv"))

alt.weights <- data.table(read.csv("~/cps_weights_2026.csv"))

alt.weights2 <- copy(alt.weights)
alt.weights2[, SEQUENCE := recid * 100]

merged <- merge(alt.weights2, orig.weights, "SEQUENCE")

merged[, scaling.factor := s006 / WT2026]

# Set each column equal to its original value times scaling factor, times 100.
for (i in 15:27) {
  col <- paste0("WT20", i)
  col.orig <- paste0(col, ".orig")
  merged[, (col.orig) := get(col)]
  merged[, (col) := as.integer(round(get(col.orig) * scaling.factor * 100))]
}

final <- merged[, c("SEQUENCE", paste0("WT20", 15:27)), with=F]

# Check it's the same structure.
stopifnot(identical(names(final), names(orig.weights)))
stopifnot(identical(final$SEQUENCE, orig.weights$SEQUENCE))

# Export.
write.csv(final, "~/cps_weights_alt.csv")
