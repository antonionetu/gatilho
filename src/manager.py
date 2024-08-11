import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from services.models import Guest

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_active_guest():
    guest_name = input("Digite o nome novo Guest: ")
    guest_name = guest_name.strip().lower().replace(" ", "_")

    db = SessionLocal()

    try:
        new_guest = Guest(name=guest_name, is_valid=True)
        db.add(new_guest)
        db.commit()
        db.refresh(new_guest)
        print(f"Guest criado com sucesso: ID={new_guest.id}, Name={new_guest.name}, Is Active={new_guest.is_valid}")

    except Exception as e:
        print(f"Ocorreu um erro ao criar o item: {e}")

    finally:
        db.close()


def block_guest():
    db = SessionLocal()

    print("Guests:")
    for guest in db.query(Guest).all():
        print(f"ID={guest.id}, Name={guest.name}, Is Active={guest.is_valid}")

    guest_name = input("Digite o nome do Guest que deseja bloquear: ")
    guest_name = guest_name.strip().lower().replace(" ", "_")

    try:
        guest = db.query(Guest).filter(Guest.name == guest_name).first()

        if guest is None:
            print("Guest não encontrado")
            return

        guest.is_valid = False
        db.commit()
        db.refresh(guest)
        print(f"Guest bloqueado com sucesso: ID={guest.id}, Name={guest.name}, Is Active={guest.is_valid}")

    except Exception as e:
        print(f"Ocorreu um erro ao bloquear o item: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    choice = input("""
    1. Criar novo Guest
    2. Bloquear Guest
    3. Sair
    
    Sua escolha: """)

    match choice:
        case "1":
            create_active_guest()
        case "2":
            block_guest()
        case "3":
            print("Saindo...")
        case _:
            print("Opção inválida")
