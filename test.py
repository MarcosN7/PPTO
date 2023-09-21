import requests

def test_register_user():
    """Testa a rota de registro de usuário."""

    # Cria um usuário
    user = {
        "name": "Fulano de Tal",
        "email": "fulano@example.com",
        "password": "123456"
    }

    # Realiza uma solicitação POST para a rota de registro
    response = requests.post("http://localhost:5000/register", json=user)

    # Verifica se a solicitação foi bem-sucedida
    assert response.status_code == 201

    # Verifica se o usuário foi salvo no banco de dados
    users = db.users.find()
    assert len(users) == 1
    assert users[0]["name"] == user["name"]
    assert users[0]["email"] == user["email"]


def test_register_professional():
    """Testa a rota de registro de profissional."""

    # Cria um profissional
    professional = {
        "name": "Ciclano de Tal",
        "email": "ciclano@example.com",
        "password": "123456",
        "company_name": "Minha Empresa",
        "services": ["construção", "pintura", "encanamento"],
        "whatsapp": "1234567890",
        "price_range": "R$ 100,00 - R$ 200,00"
    }

    # Realiza uma solicitação POST para a rota de registro
    response = requests.post("http://localhost:5000/register", json=professional)

    # Verifica se a solicitação foi bem-sucedida
    assert response.status_code == 201

    # Verifica se o profissional foi salvo no banco de dados
    professionals = db.professionals.find()
    assert len(professionals) == 1
    assert professionals[0]["name"] == professional["name"]
    assert professionals[0]["email"] == professional["email"]


def main():
    test_register_user()
    test_register_professional()


if __name__ == "__main__":
    main()
