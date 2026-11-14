"""Simulador didático, sem preempção, IRQ ou troca de contexto real."""
from collections import deque
def schedule(tasks, ticks):
    if ticks<0: raise ValueError("ticks negativos")
    queue=deque(tasks)
    if len(set(queue))!=len(queue): raise ValueError("tarefas duplicadas")
    trace=[]
    for _ in range(ticks):
        if not queue: break
        task=queue.popleft()
        trace.append(task)
        queue.append(task)
    return trace
def schedule_ready(tasks, blocked, ticks):
    return schedule([task for task in tasks if task not in blocked],ticks)
