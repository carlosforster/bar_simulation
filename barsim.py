#
# An Event-based Simulation by Carlos Forster (c) 2024
#
# Model of a Bar
#
#


import random
import heapq

aguarda_servir=[]
aguarda_beber=[]
copos_limpos=["c1", "c2", "c3", "c4", "c5"]
copos_sujos=[]
copos_em_uso=[]
garcom_disponivel=["g1", "g2"]

def info(time, text):
    print(f"{time:06.2f}:  {text}")


class Simulation:

    clock = []
    now = 0
    
    animation=[]
    
    def sched(self, time, tup):
        heapq.heappush(self.clock, (self.now+time,tup))
        
    def next_event(self):
        newtime, tup = heapq.heappop(self.clock)
        self.now = newtime
        return tup

    def remove_event(self, element):
        self.clock.remove(element)
        heapq.heapify(self.clock)

    def go(self):
        self.sched(0, ('start',) )
        self.animation_frame()
        while True:
            if self.now>300: return # stops simulation at 300
            again = 1
            while again:
                again=0
                
                while aguarda_servir and copos_limpos and garcom_disponivel:
                    cliente = aguarda_servir.pop()
                    copo = copos_limpos.pop()
                    garcom = garcom_disponivel.pop()
                    self.sched(random.uniform(10, 12), ('servir',cliente,copo,garcom))
                    info(self.now,f"Garçom {garcom} atendeu {cliente.name}.")
                    self.animation_frame()
                    again =1
                    
                while copos_sujos and garcom_disponivel:
                    copo = copos_sujos.pop()
                    garcom = garcom_disponivel.pop()
                    self.sched(random.uniform(3, 4), ('lavar', copo, garcom))
                    self.animation_frame()
                    again =1
                    
            try:
                ev = self.next_event()
            except:
                return # nothing to do, simulation finished
            
            if ev[0] == 'cliente_chega':
                cliente = Cliente()
                if cliente.name[-1]=="9": continue # stop at 8
                info(self.now,f"{cliente.name} chegou.")
                aguarda_servir.append(cliente)
                self.sched(random.expovariate(1.0/10),('cliente_chega',))
                
            elif ev[0] == 'servir':
                _, cliente, copo, garcom = ev
                aguarda_beber.append(cliente)
                copos_em_uso.append(copo)
                garcom_disponivel.append(garcom)
                info(self.now, f"{cliente.name} bebendo {copo}.")
                self.sched(random.uniform(20, 22), ('beber', cliente, copo))
                
            elif ev[0] == 'beber':
                _, cliente, copo = ev
                aguarda_beber.remove(cliente)
                if random.random() > 0.3:
                    aguarda_servir.append(cliente)
                else:
                    info(self.now,f"{cliente.name} se foi.")
                    pass #cliente vai embora
                copos_em_uso.remove(copo)
                copos_sujos.append(copo)
                
            elif ev[0] == 'lavar':
                _,copo, garcom = ev
                garcom_disponivel.append(garcom)
                copos_limpos.append(copo)
                info(self.now, f"Copo {copo} lavado por {garcom}.") 
                
            elif ev[0] == 'start':
                self.sched(0, ('cliente_chega',) )
            
            else:
                print(f"Unrecogized event {ev[0]}.")
                return
            
            self.animation_frame()

                
    def animation_frame(self):
        frame=[]
        for cli in aguarda_servir: frame.append("cli"+cli.name[-1]+"w")
        for cli in aguarda_beber: frame.append("cli"+cli.name[-1]+"b")
        for c in copos_sujos: frame.append(c+"s")
        for c in copos_limpos: frame.append(c+"l")
        for c in copos_em_uso: frame.append(c+"u")
        for g in garcom_disponivel: frame.append(g)
        for _,ev in self.clock:
            if ev[0]=='servir':
              _, cliente, copo, garcom = ev
              frame.append("cli"+cliente.name[-1]+"s")
              frame.append(garcom+"s")
              frame.append(copo+"u")
            if ev[0]=='lavar':
              _,copo, garcom = ev
              frame.append(garcom+"l")
              frame.append(copo+"s")
            if ev[0]=='beber':
              _, cliente, copo = ev
              frame.append(copo+"u")
        
        self.animation.append(frame)
        
        

class Cliente:
    cont = 0
    def __init__(self):
        Cliente.cont += 1
        self.name =f"Cliente{Cliente.cont}"

random.seed(10)
sim = Simulation()
sim.go()

with open("bartemplate.html","r") as f:
    template=f.read()
with open("barsim.svg","r") as f:
    svgtemplate=f.read()
with open("barsim.html", "w") as f:
    f.write(template
     .replace("XXXXX",str(sim.animation))
     .replace("YYYYY",svgtemplate)
    )
     
