import { gql } from "@apollo/client";

export const GQL_CODES = gql`
query Codes($page: Int) {
  codes(page: $page, pageSize: 10) {
    CDescription
    CEngName
    CId
    CParentId
    CName
  }
}`