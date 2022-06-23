import { ApolloClient, ApolloLink, createHttpLink, InMemoryCache } from '@apollo/client';
import { onError } from "@apollo/client/link/error";
import { toast } from "react-toastify";

import { fetchToken } from "./comm-util"

const httpLink = createHttpLink({
  uri: '/graphql',
});

const errorLink = onError((props: any) => {
  if (props.graphQLErrors)
    props.graphQLErrors.forEach((f: any) => {
      toast.error(f.message);
      // console.log(
      //   `[GraphQL error]: Message: ${f.message}, Location: ${f.locations}, Path: ${f.path}`
      // )
    });
  if (props.networkError) {
    toast.error(props.networkError);
    // console.log(`[Network error]: ${props.networkError}`);
  }
});

const authLink = new ApolloLink((operation, forward) => {
  const token = fetchToken();

  operation.setContext((props: any) => ({ headers: {
    authorization: token ? `Bearer ${token}` : "",
    ...props.headers
  }}));
  return forward(operation);
});

export const apolloClient = new ApolloClient({
  // link: authLink.concat(httpLink),
  link: ApolloLink.from([errorLink, authLink]).concat(httpLink),
  cache: new InMemoryCache(),
});