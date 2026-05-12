# Ярошенко Георгій

import asyncio
import random
import time
import networkx as nx
import matplotlib.pyplot as plt


# Базовий вузол
class Node:
    def __init__(self, name):
        self.name = name
        self.connections = []

    # З'єднання вузлів
    def connect(self, node):
        if node not in self.connections:
            self.connections.append(node)
            node.connections.append(self)

    # Відправка з імітацією затримки та втрат
    async def send(self, packet, network):
        await asyncio.sleep(random.uniform(0.05, 0.3))
        if random.random() < network.loss_rate:
            network.packets_lost += 1
            return
        await self.forward(packet, network)

    # Пересилання пакету далі
    async def forward(self, packet, network):
        if self == packet.dest or self in packet.visited:
            return
        packet.visited.append(self)
        for node in self.connections:
            if node not in packet.visited:
                await node.send(packet, network)


# Маршрутизатор
class Router(Node):
    pass


# Пакет даних
class Packet:
    def __init__(self, src, dest, size, protocol):
        self.src = src
        self.dest = dest
        self.size = size
        self.protocol = protocol
        self.visited = []


# Протокол TCP
class TCPProtocol:
    name = "TCP"

    @staticmethod
    async def transmit(src, dest, network):
        packet = Packet(src, dest, random.randint(200, 500), "TCP")
        await src.send(packet, network)


# Протокол UDP
class UDPProtocol:
    name = "UDP"

    @staticmethod
    async def transmit(src, dest, network):
        packet = Packet(src, dest, random.randint(50, 200), "UDP")
        await src.send(packet, network)


# Мережа
class Network:
    def __init__(self):
        self.nodes = []
        self.loss_rate = random.uniform(0.10, 0.15)  # 10-15% втрат
        self.packets_sent = 0
        self.packets_lost = 0
        self.total_time = 0

    # Симуляція передачі
    async def simulate(self, protocol, packets=5):
        for _ in range(packets):
            src, dest = random.sample(self.nodes, 2)
            start = time.time()
            self.packets_sent += 1
            print(f"Відправка {protocol.name}: {src.name} -> {dest.name}")
            await protocol.transmit(src, dest, self)
            self.total_time += time.time() - start

    # Аналіз продуктивності
    def analyze(self, topology_name):
        avg_time = self.total_time / self.packets_sent if self.packets_sent else 0
        loss = (self.packets_lost / self.packets_sent) * 100 if self.packets_sent else 0
        bandwidth = (self.packets_sent - self.packets_lost) / self.total_time if self.total_time else 0

        print(f"\n--- {topology_name} ---")
        print(f"Середній час передачі: {avg_time:.4f} с")
        print(f"Втрати пакетів: {loss:.2f}%")
        print(f"Пропускна здатність: {bandwidth:.2f} пак/с\n")

    # Графічна візуалізація
    def visualize(self, title, node_color):
        G = nx.Graph()
        for node in self.nodes:
            for conn in node.connections:
                G.add_edge(node.name, conn.name)
        plt.figure(figsize=(6, 4))
        nx.draw(G, with_labels=True, node_color=node_color, node_size=2000, font_size=10, font_weight="bold")
        plt.title(title)
        plt.show()


# Генерація Зіркової топології
def build_star():
    net = Network()
    router = Router("Router")
    pcs = [Node(f"PC{i}") for i in range(1, 5)]
    net.nodes = [router] + pcs
    for pc in pcs:
        router.connect(pc)
    return net


# Генерація Кільцевої топології
def build_ring():
    net = Network()
    pcs = [Node(f"PC{i}") for i in range(1, 6)]
    net.nodes = pcs
    for i in range(len(pcs)):
        pcs[i].connect(pcs[(i + 1) % len(pcs)])
    return net


# Головна функція
async def main():
    # Тест Зіркової топології (TCP)
    star_net = build_star()
    await star_net.simulate(TCPProtocol, packets=5)
    star_net.analyze("Зіркова топологія (TCP)")
    star_net.visualize("Зіркова топологія", "skyblue")

    # Тест Кільцевої топології (UDP)
    ring_net = build_ring()
    await ring_net.simulate(UDPProtocol, packets=5)
    ring_net.analyze("Кільцева топологія (UDP)")
    ring_net.visualize("Кільцева топологія", "orange")


if __name__ == "__main__":
    asyncio.run(main())