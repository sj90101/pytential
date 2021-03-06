from __future__ import division

__copyright__ = "Copyright (C) 2014 Shidong Jiang, Andreas Kloeckner"

__license__ = """
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import numpy as np


def muller_deflate(f, n, maxiter=100, eps=1e-14):
    """
    :arg n: number of zeros sought
    :return: (roots, niter, err) - roots of the given function; number of
    :iterations used for each root; and the relative error of each root.
    """
    # initialize variables
    roots = []
    niter = []
    err = []

    def f_deflated(z):
        y = f(z)
        for r in roots:
            y = y/(z-r)

        return y

    # finds n roots
    # checks for NaN which signifies the end of the root finding process.
    # Truncates the zero arrays created above if neccessary.
    for i in range(n):
        miter = 0
        roots0, niter0, err0 = muller0(f_deflated, maxiter, eps)
        roots.append(roots0)
        niter.append(niter0)
        err.append(err0)

        while (np.isnan(roots[i]) or niter[i] == maxiter) and miter < 50:
            roots0, niter0, err0 = muller0(f_deflated, maxiter, eps)
            roots[i] = roots0
            niter[i] = niter0
            err[i] = err0
            miter = miter+1

    return roots, niter, err


# Muller's method
def muller0(f, maxiter=100, eps=1e-13):

    # initialize variables
    niter = 0                      # counts iteration steps
    err = 100*eps

    z1, z2, z3 = np.random.rand(3) + 1j*np.random.rand(3)   # 3 initial guesses
    #x = rand(1,3)*10   % 3 initial guesses

    w1 = f(z1)
    w2 = f(z2)
    w3 = f(z3)

    # iterate until max iterations or tolerance is met
    #while niter < maxiter and (err>eps or abs(w3)>1e-30):
    while niter < maxiter and err > eps:
        niter = niter + 1

        h1 = z2 - z1
        h2 = z3 - z2
        lambda_ = h2/h1
        g = w1*lambda_*lambda_ - w2*(1+lambda_)*(1+lambda_)+w3*(1+2*lambda_)
        det = g*g - 4*w3*(1+lambda_)*lambda_*(w1*lambda_-w2*(1+lambda_)+w3)

        h1 = g + np.sqrt(det)
        h2 = g - np.sqrt(det)

        if np.abs(h1) > np.abs(h2):
            lambda_ = -2*w3*(1.0+lambda_)/h1
        else:
            lambda_ = -2*w3*(1.0+lambda_)/h2

        z1 = z2
        w1 = w2
        z2 = z3
        w2 = w3
        z3 = z2+lambda_*(z2-z1)
        w3 = f(z3)

        if np.abs(z3) < 1e-14:
            err = np.abs(z3-z2)
        else:
            err = np.abs((z3-z2)/z3)

        z = z3

    return z, niter, err
