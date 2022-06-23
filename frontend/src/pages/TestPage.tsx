import { useState, useEffect } from "react";
import { AgGridReact } from "ag-grid-react";
import { atom, useAtom } from "jotai";
import { toast } from "react-toastify";

import { fetchToken } from "@util/comm-util";
import { useQuery } from "@apollo/client";
import { GQL_CODES } from "@gql/code";

import "ag-grid-community/dist/styles/ag-grid.css";
import "ag-grid-community/dist/styles/ag-theme-alpine.css";

export default function TestPage() {
  const { called, data } = useQuery(GQL_CODES, {
    fetchPolicy: "network-only",
    variables: { page: 1 }
  });

  const [columnDefs] = useState([
    { field: "CId" },
    { field: "CParentId" },
    { field: "CName" }
  ]);

  return (
    <div className="container h-full">
      <div className="ag-theme-alpine w-full h-full">
        {called && (
          <AgGridReact
            rowData={data?.codes}
            columnDefs={columnDefs}
          ></AgGridReact>
        )}
      </div>
    </div>
  );
}
