class Process:
    def __init__(self, pid, arrival, burst):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.remaining = burst
        self.finish_time = 0
        self.start_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0

def main():
    filename = 'processes.txt'
    try:
        with open(filename, 'r') as file:
            context_switch = int(file.readline().strip().split()[0])
            quantum = int(file.readline().strip().split()[0])
            processes = []
            for line in file:
                parts = line.split()
                if len(parts) >= 3:
                    processes.append(Process(int(parts[0]), int(parts[1]), int(parts[2])))
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    def fcfs_scheduling(processes, context_switch):
        current_time = 0
        for process in sorted(processes, key=lambda x: x.arrival):
            if current_time < process.arrival:
                current_time = process.arrival
            process.start_time = current_time
            process.finish_time = current_time + process.burst
            current_time += process.burst + context_switch

    def calculate_metrics(processes):
        total_time = max(p.finish_time for p in processes) - min(p.arrival for p in processes)
        total_burst_time = sum(p.burst for p in processes)
        cpu_utilization = (total_burst_time / total_time) * 100

        total_waiting_time = sum(p.finish_time - p.arrival - p.burst for p in processes)
        average_waiting_time = total_waiting_time / len(processes)

        total_turnaround_time = sum(p.finish_time - p.arrival for p in processes)
        average_turnaround_time = total_turnaround_time / len(processes)

        return cpu_utilization, average_waiting_time, average_turnaround_time

    def display_results(processes, cpu_utilization, average_waiting_time, average_turnaround_time):
        print("PID Arrival Burst Finish Wait Turn")
        for process in processes:
            process.waiting_time = process.finish_time - process.arrival - process.burst
            process.turnaround_time = process.finish_time - process.arrival
            print(f"{process.pid}    {process.arrival}        {process.burst}      {process.finish_time}   {process.waiting_time}   {process.turnaround_time}")
        print(f"\nCPU Utilization: {cpu_utilization:.2f}%")
        print(f"Average Waiting Time: {average_waiting_time:.2f} ms")
        print(f"Average Turnaround Time: {average_turnaround_time:.2f} ms")

    fcfs_scheduling(processes, context_switch)
    results = calculate_metrics(processes)
    display_results(processes, *results)

if __name__ == '__main__':
    main()
