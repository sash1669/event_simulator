from des import SchedulerDES
from event import Event, EventTypes
from process import Process, ProcessStates

class FCFS(SchedulerDES):
    def scheduler_func(self, cur_event):
        process=self.processes[cur_event.process_id]
        process.process_state=ProcessStates.READY
        return process

    def dispatcher_func(self, cur_process):
        cur_process.process_state=ProcessStates.RUNNING
        # start executing the process at the current time -self.time
        #  execute it for the full length of time required -service time
        exec_time=cur_process.run_for(cur_process.service_time,self.time)
        self.time+=exec_time
        cur_process.process_state=ProcessStates.TERMINATED
        event=Event(process_id=cur_process.process_id,event_type=EventTypes.PROC_CPU_DONE,
        event_time=self.time)
        return event

class SJF(SchedulerDES):
    def scheduler_func(self, cur_event):
        #pick the proccess with the shortest service time and execute it to completion
        sorted_processes= sorted(self.processes, key=lambda process: process.service_time)
        #print('sorted processes',sorted_processes)
        for p in sorted_processes:
            if p.process_state!=ProcessStates.TERMINATED and p.arrival_time<=self.time:
                process=p
                break
        process.process_state = ProcessStates.READY
        return process

    def dispatcher_func(self, cur_process):
        cur_process.process_state = ProcessStates.RUNNING
        time=self.time
        exec_time=cur_process.run_for(cur_process.service_time, time)
        self.time += exec_time
        cur_process.process_state = ProcessStates.TERMINATED
        event = Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_DONE,
                      event_time=self.time)
        return event


class RR(SchedulerDES):
    def scheduler_func(self, cur_event):
        process = self.processes[cur_event.process_id]
        process.process_state = ProcessStates.READY
        return process

    def dispatcher_func(self, cur_process):
        cur_process.process_state = ProcessStates.RUNNING

        if self.quantum >= cur_process.remaining_time:
            exec_time = cur_process.run_for(self.quantum, self.time)
            self.time += exec_time
            cur_process.process_state = ProcessStates.TERMINATED
            event = Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_DONE,
                          event_time=self.time)
            return event

        else:
            exec_time = cur_process.run_for(self.quantum, self.time)
            self.time += exec_time
            cur_process.process_state = ProcessStates.READY
            event = Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_REQ,
                          event_time=self.time)
            return event


class SRTF(SchedulerDES):
    def scheduler_func(self, cur_event):
        sorted_processes = sorted(self.processes, key=lambda process: process.remaining_time)
        for i in sorted_processes:
            if i.process_state != ProcessStates.TERMINATED and i.arrival_time<=self.time:
                return i

    def dispatcher_func(self, cur_process):
        cur_process.process_state = ProcessStates.RUNNING
        # start executing the process at the current time -self.time
        #  execute it for the full length of time required -service time

        exec_time=self.next_event_time()-self.time

        if exec_time>=cur_process.remaining_time:
            self.time += cur_process.run_for(cur_process.remaining_time, self.time)
            cur_process.process_state = ProcessStates.TERMINATED
            event = Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_DONE,
                          event_time=self.time)
            return event

        if exec_time<cur_process.remaining_time:
            self.time += cur_process.run_for(exec_time, self.time)
            cur_process.process_state = ProcessStates.READY
            event = Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_REQ,
                          event_time=self.time)
            return event
