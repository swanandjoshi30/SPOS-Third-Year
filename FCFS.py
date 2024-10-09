def findwaitingtime(processes,n,bt,wt):
    wt[0] = 0

    for i in range(1, n):
        wt[i] = bt[i - 1] + wt[i -1]

def findturnaroundtime(processes,n,bt,wt,tat):
    for i in range(n):
        tat[i] = bt[i] + wt[i]

def findavgtime(processses,n,bt):
    wt = [0] * n
    tat = [0] * n
    total_wt = 0
    total_tat = 0

    findwaitingtime(processses,n,bt,wt)

    findturnaroundtime(processses,n,bt,wt,tat)

    print("Processes Burst time " +
          " Waiting time " +
          " Turn around time")
    for i in range(n):
        total_wt = total_tat + wt[i]
        total_tat = total_tat + tat[i]

        print(" " + str(i + 1) + "\t\t" +
              str(bt[i]) + "\t " +
              str(wt[i]) + "\t\t " +
              str(tat[i]))

    print("Average waiting time = "+ str(total_wt / n))
    print("Average turnaround time = "+ str(total_tat / n))


if __name__ == "__main__":
    processes = [1, 2, 3]
    n = len(processes)

    burst_time = [10, 5, 8]

    findavgtime(processes, n, burst_time)