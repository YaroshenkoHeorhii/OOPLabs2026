# Ярошенко Георгій

import asyncio
from sqlalchemy import Column, Integer, String, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.future import select

# Налаштування підключення до БД
DATABASE_URL = "sqlite+aiosqlite:///network.db"
Base = declarative_base()
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# 1. Створення моделі мережевого вузла
class Node(Base):
    __tablename__ = 'nodes'
    id = Column(Integer, primary_key=True)
    ip_address = Column(String, unique=True, nullable=False)
    status = Column(String, default="unknown")


# Створення таблиць у БД
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Очищення таблиці (корисно для повторних запусків скрипта)
async def reset_nodes():
    async with AsyncSessionLocal() as session:
        await session.execute(text("DELETE FROM nodes"))
        await session.commit()


# 2. Додавання 15 вузлів до бази
async def add_nodes(count=15):
    async with AsyncSessionLocal() as session:
        nodes = [Node(ip_address=f"192.168.1.{i}", status="unknown") for i in range(1, count + 1)]
        session.add_all(nodes)
        await session.commit()
    print(f"[Система] Успішно додано {count} вузлів зі статусом 'unknown'.")


# 3. Асинхронна функція для отримання списку вузлів із бази
async def get_nodes(label=""):
    print(f"\n--- {label} ---")
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Node))
        nodes = result.scalars().all()
        for node in nodes:
            print(f"ID: {node.id:<3} | IP: {node.ip_address:<15} | Status: {node.status}")


# 4. Асинхронна система збору статусів (імітація мережевих запитів)
async def monitor_nodes():
    print("\n[Моніторинг] Початок опитування вузлів (імітація затримки мережі)...")
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Node))
        nodes = result.scalars().all()

        for node in nodes:
            # Імітація асинхронного мережевого запиту до вузла
            await asyncio.sleep(0.2)

            # Логіка оновлення: непарні IP -> active, парні IP -> offline
            ip_last_octet = int(node.ip_address.split('.')[-1])
            if ip_last_octet % 2 == 0:
                node.status = "offline"
            else:
                node.status = "active"

        # Збереження оновлених статусів у БД
        await session.commit()
    print("[Моніторинг] Оновлення статусів завершено та збережено в БД.")


# 5. Головна асинхронна функція для демонстрації результатів
async def main():
    # Ініціалізація бази
    await create_tables()
    await reset_nodes()

    # Наповнення бази
    await add_nodes(15)

    # Виведення ДО моніторингу
    await get_nodes("Список вузлів ДО моніторингу")

    # Запуск моніторингу
    await monitor_nodes()

    # Виведення ПІСЛЯ моніторингу
    await get_nodes("Список вузлів ПІСЛЯ моніторингу")


if __name__ == "__main__":
    # Запуск асинхронної програми
    asyncio.run(main())