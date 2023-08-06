def per_loan(amount):
    tax=float(input("Enter Personal Loan Tax"))
    total_amount=amount*tax+amount
    #print("home loan amount {}".format(total_amount))
    return total_amount
