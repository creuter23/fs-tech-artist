#Quotation Manipulation
# A script used to test the different ways to manipulate string data in python

#Fortune Cookie Quote
quote = "It is better to beg than to steal, but it is better to work than to beg."

print "Original quote: "
print quote

print "\nIn uppercase: "
print quote.upper()

print "\nIn lowercase: "
print quote.lower()

print "\nAs a title: "
print quote.title()

print "\nWith a minor replacement: "
print quote.replace("work", "labor")

print "\nOriginal quote is still: "
print quote

raw_input("\n\nPress the enter key to exit.")
