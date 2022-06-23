import { Routes, Route } from "react-router-dom";
// import loadable from "@loadable/component";

import { DefaultTheme } from "@component/theme/DefaultTheme";
import MainPage from "@pages/MainPage";
import TestPage from "@pages/TestPage";
import LoginPage from "@pages/LoginPage";
import ErrorPage from "@pages/ErrorPage";

// const ARR_ROUTES = [
//   {
//     path: "/",
//     realPath: "@pages/MainPage"
//   },
//   {
//     path: "/test",
//     realPath: "@pages/TestPage"
//   }
// ];

// const AsyncPage = loadable(
//   (props: any) => import(/* @vite-ignore */ `${props.page}`)
// );

export default function CustomRoutes() {
  return (
    <>
      <Routes>
        {/* {ARR_ROUTES.map((r, index) => (
          <Route
            key={index}
            path={r.path}
            element={
              <DefaultTheme>
                <AsyncPage page={r.realPath} />
              </DefaultTheme>
            }
          />
        ))} */}
        <Route
          path={"/"}
          element={
            <DefaultTheme>
              <MainPage />
            </DefaultTheme>
          }
        />
        <Route
          path={"/test"}
          element={
            <DefaultTheme>
              <TestPage />
            </DefaultTheme>
          }
        />
        <Route path={"/login"} element={<LoginPage />} />
        <Route path="*" element={<ErrorPage />} />
      </Routes>
    </>
  );
}
