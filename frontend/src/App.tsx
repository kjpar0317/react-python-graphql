import { Suspense } from "react";

import { ApolloProvider } from "@apollo/client";
import { ErrorBoundary } from "react-error-boundary";
import { ToastContainer } from "react-toastify";

import CustomRoutes from "@route/CustomRoutes";
import { apolloClient } from "@util/apollo-util";
import ErrorBoundaryFallback from "@component/layout/error/ErrorBoundaryFallback";
import { Loading } from "@component/layout/common/index";

import "virtual:windi.css";
import "./index.css";
import "react-toastify/dist/ReactToastify.css";

export default function App() {
  return (
    <ErrorBoundary
      FallbackComponent={ErrorBoundaryFallback}
      onReset={() => {
        // reset the state of your app so the error doesn't happen again
        window.location.reload();
      }}
    >
      <Suspense fallback={<Loading />}>
        <ApolloProvider client={apolloClient}>
          <CustomRoutes />
        </ApolloProvider>
      </Suspense>
      <ToastContainer
        position="bottom-right"
        pauseOnFocusLoss
        draggable
        pauseOnHover
      />
    </ErrorBoundary>
  );
}
