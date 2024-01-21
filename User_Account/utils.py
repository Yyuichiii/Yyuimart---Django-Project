import math, random


def generateOTP(digit) : 
    # Declare a digits variable  
    # which stores all digits 
    digits = "0123456789"
    OTP = "" 
   # length of password can be changed
   # by changing value in range
    for i in range(digit) :
        OTP += digits[math.floor(random.random() * 10)] 
    return OTP