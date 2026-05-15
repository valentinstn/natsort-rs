from natsort_rs import natsort

alist: list[str] = ['a', 'x', 'z']
blist = natsort(alist)

alist: list[float] = [5.1, 3.1]
clist = natsort(alist)

alist: list[float] = [5.1, 3.1]
dlist = natsort(alist, return_indices=True)
