notes = read.table("../data/all_notes")
colnames(notes) <- c("pitch", "midi_clock")
notes = data.frame(notes)

#pdf("../report/distribution_of_notes.pdf")
maxp <- max(notes$pitch)
minp <- min(notes$pitch)
hist(notes$pitch, breaks = maxp-minp, main="Pitch Distribution of All Notes", xlab = "Pitch", ylab = "Count of Notes in All Training Data", xlim=c(0, maxp))

pdf("../distribution_of_length.pdf")
#attach(mtcars)
#par(mfrow=c(3,2))

hist(notes$midi_clock, breaks = 10000, main="All notes, breaks=10000", xlab = "Length (in MIDI-clock)", ylab="Count of Notes in All Data")

hist(notes$midi_clock, breaks = 10000, main="All notes, breaks=10000", xlab = "Length (in MIDI-clock), focus on 0~2000", xlim = c(0, 2000), ylab="Count of Notes in All Data")

mc = notes$midi_clock/24 # converto quater note

hist(mc, breaks = 10000, main="All notes, breaks=10000", xlab = "in quater notes (1/4 notes), focus on 0~100", xlim = c(0, 100), ylab="Count of Notes in All Data")
log_mc = log(mc,2)

mc = mc*32 #1/128 note

hist(mc, breaks = 10000, main="All notes, breaks=10000", xlab = "in 1/128 notes, focus on 0~2000", xlim = c(0,2000), ylab="Count of Notes in All Data")


log_mc = log(mc,2)  # take log to 2

hist(log_mc, breaks = 100, main="All notes, breaks = 100", xlab = "Notes in log2", ylab="Count of Notes in All Data")

log_mc = floor(log_mc)  # floor
h = hist(log_mc, breaks = 18, main="All notes, breaks = 18", xlab = "Notes in log2, rounded", xlim=c(0,20), ylab="Count of Notes in All Data")



dev.off()

