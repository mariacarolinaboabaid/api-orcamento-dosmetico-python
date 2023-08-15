# API Orçamento Doméstico

API REST que permite armazenar e exibir registros de despesas.

Orientações gerais:

- Uma DESPESA possui os seguintes dados: Valor, Descrição, Data, Tipo de Pagamento e Categoria;
- Os TIPOS DE PAGAMENTO são: Dinheiro, Débito, Crédito, Pix;
- A listagem de DESPESAS mostra apenas os registros do mês vigente;

## API REST

### Endpoint

A API disponibiliza um _endpoint_ que permita o cadastro e exibição de despesas:

| Verbo HTTP | Path           | Função            |
| ---------- | -------------- | ----------------- |
| GET        | /api/despesas  | Listar despesas   |
| POST       | /api/despesas  | Cadastrar despesa |

### Response body

Independente da função executada (listagem ou cadastro) o JSON de retorno possui o seguinte formato:

```json
{
    "data": null,
    "success": true
}
```

O valor do atributo `data` é o resultado da request executada. Para a função "Listar" contém a lista de despesas cadastradas no banco de dados. Para a função "Cadastrar" contém o ID da despesa recém inserida no banco de dados.

O atributo `success` será um booleano indicando o êxito, ou não, da função executada.
