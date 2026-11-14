"""Modelo educacional de frames; não é o PMM do kernel."""
class OutOfFrames(Exception): pass
class FrameAllocator:
    def __init__(self, available):
        self.free=set(available)
        self.allocated=set()
    def alloc(self):
        if not self.free: raise OutOfFrames("sem frames livres")
        frame=min(self.free)
        self.free.remove(frame);self.allocated.add(frame)
        return frame
    def release(self, frame):
        if frame not in self.allocated: raise ValueError("double free ou frame desconhecido")
        self.allocated.remove(frame);self.free.add(frame)
