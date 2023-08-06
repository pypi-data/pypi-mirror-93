def ve_loan(amount):
    tax=float(input("Enter vehicle Loan Tax"))
    total_amount=amount*tax+amount
    #print("home loan amount {}".format(total_amount))
    return total_amount
