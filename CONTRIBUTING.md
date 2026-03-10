# Contribuindo para CRUD_python

Obrigado pelo interesse em contribuir! Aqui estão passos simples para começar:

1. Fork este repositório para sua conta GitHub.
2. Clone o fork:

   git clone https://github.com/<seu-usuario>/CRUD_python.git
   cd CRUD_python

3. Crie um branch para sua alteração:

   git checkout -b feat/minha-mudanca

4. Configure o ambiente local e instale dependências:

   python -m venv .venv; .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt

5. Configure as variáveis de ambiente (use `.env.example`):

   copy .env.example .env
   # Edite o .env e coloque suas credenciais locais do MySQL

6. Teste a aplicação e verifique seu código.

7. Faça commits claros e push para o seu fork:

   git add .
   git commit -m "Descrição da mudança"
   git push origin feat/minha-mudanca

8. Abra um Pull Request (PR) para o branch `main` do repositório original.

Observações:
- Mantenha PRs pequenos e focados.
- Documente mudanças importantes no README quando necessário.
- Se possível, adicione pequenos testes ou validações para regressões.

Licença e Código de Conduta
- Ao contribuir, você concorda em submeter seu código sob a licença MIT do projeto.
