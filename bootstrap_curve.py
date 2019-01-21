import matplotlib.pyplot as plt
import numpy as np
import math
from product import Bond

def plot(x, y):
    plt.plot(x, y)
    plt.ylim(bottom=0)
    plt.ylim(top=max(y)*1.1)
    plt.show()

def bootstrap(bonds):
    y = []
    x = []

    # Take care of the zero coupons first
    # We assume that coupon == 0 even for the first annual for now. Not sure how the
    # product is represented when we have a bond with < 1Y time until maturity with coupon
    # on maturity. Might need to make a special case for this.
    for bond in bonds:
        if bond.coupon == 0:
            y.append((bond.face_value / bond.price - 1) / bond.tau)
            x.append(bond.tau)

    # Now we take the ones with coupon
        elif bond.coupon != 0 and bond.tau >= 1:
            p = bond.price
            coupon_amt = bond.face_value * bond.coupon

            for i in range(1, bond.tau):
                i_year_rate = y[x.index(i)]
                pv_coupon = coupon_amt / ((i_year_rate + 1) ** i)
                p -= pv_coupon

            # Bond price should only reflect payout at maturity now
            y.append(((bond.face_value + coupon_amt) / p) ** (1 / float(bond.tau)) - 1)
            x.append(bond.tau)

    # General case, we need to figure out the interest rate of the first coupon.
    # If tau is e.g. 1.66, we know that we need to have the interest rate for .66 year.
    # tau

    # This is very easy if we know the previous integers of annual rate.
    # It requires us to look back at the previous integer of tau and its calculated rate.
    # Let's do the easy non-general case first. We know that it's 1 and 2

    x.insert(0, 0)
    y.insert(0, 0)

    return x, y

def run():
    b1 = Bond(tau=0.5, price=99.05)
    b2 = Bond(tau=0.75, price=98.45)
    b3 = Bond(tau=1, price=97.85)
    b4 = Bond(tau=2, price=101.40, coupon=0.035)
    b5 = Bond(tau=3, price=102.20, coupon=0.04)
    
    b = [b1, b2, b3, b4, b5]
    x, y = bootstrap(b)
    plot(x, y)

if __name__ == "__main__":
    run()

