# API Orçamento Doméstico

Você deve construir uma API REST que permita armazenar e exibir registros de despesas.

Orientações gerais:

- Uma DESPESA deve possuir os seguintes dados: Valor, Descrição, Data, Tipo de Pagamento e Categoria;
- Os TIPOS DE PAGAMENTO são: Dinheiro, Débito, Crédito, Pix;
- A listagem de DESPESAS deve mostrar apenas os registros do mês vigente;
- permitido a utilização de ORMs SqlAlchemy;
- Mantenha uma separação adequada de responsabilidades;
- Utilize conceitos Programação Orientada a Objetos quando achar pertinente;
- Utilize teste unitario;
- Necessário que o projeto esteja em Docker;

## API REST

### Endpoint

A API deverá disponibilizar um _endpoint_ que permita o cadastro e exibição de despesas:

| Verbo HTTP | Path           | Função            |
| ---------- | -------------- | ----------------- |
| GET        | /api/despesas  | Listar despesas   |
| POST       | /api/despesas  | Cadastrar despesa |

### Response body

Independente da função executada (listagem ou cadastro) o JSON de retorno deve possuir o seguinte formato:

```json
{
    "data": null,
    "success": true
}
```

O valor do atributo `data` deve ser o resultado da request executada. Para a função "Listar" deve conter a lista de despesas cadastradas no banco de dados. Para a função "Cadastrar" deve conter o ID da despesa recém inserida no banco de dados.

O atributo `success` será um booleano indicando o êxito, ou não, da função executada.