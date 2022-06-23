
import { gql } from "@apollo/client";

export const GQL_LOGIN = gql`
mutation Login($id: String!, $password: String!) {
  login(id: $id, password: $password) {
    userId
    token
  }
}
`

