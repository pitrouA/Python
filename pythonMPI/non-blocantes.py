from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

data = {}

if rank == 0:
    data = {'a': 7, 'b': 3.14}
    req = comm.isend(data, dest=1, tag=11)
    req.wait()
elif rank == 1:
    req = comm.irecv(source=0, tag=11)
    data = req.wait()

print("rank = "+str(rank)+" : "+str(data))
