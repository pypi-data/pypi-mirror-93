#m1:nrow✖nk  m2：nk×ncol  rst:nrow×ncol
def mxmul(mx1,mx2,nrow,nk,ncol):
    rst = [[0 for y in range(ncol)] for x in range(nrow)]
    for i in range(nrow):
        for j in range(ncol):
            for k in range(nk):
                rst[i][j] += mx1[i][k] * mx2[k][j]
    return rst

def mxsum(mx,nrrow,ncol):
    s = 0
    for i in range(nrrow):
        for j in range(ncol):
            s += mx[i][j]
    return s

if __name__ == "__main__":
    import time
    nrrow, nk, ncol = 50,30,50
    mx1 = [[y for y in range(nk)] for x in range(nrrow)]
    mx2 = [[y for y in range(ncol)] for x in range(nk)]
    start = time.perf_counter()
    rst = mxmul(mx1,mx2,nrrow,nk,ncol)
    end = time.perf_counter()
    print("运算时间为{:.4f}s".format(end-start))