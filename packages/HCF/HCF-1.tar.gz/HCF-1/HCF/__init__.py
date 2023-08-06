class HCF:
    def __init__(self,*n):
        num1=n[0] 
        num2=n[1] 
        self.gcd=self.hcf2(num1,num2) 
        for i in range(2,len(n)): 
            self.gcd=self.hcf2(self.gcd,n[i])
        if self.gcd==1:
            self.msg="Co-Primes"
        else:
            self.msg=""

    def hcf2(self,x, y): 
        while(y): 
            x, y = y, x % y 
        return x 