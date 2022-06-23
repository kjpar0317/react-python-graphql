import { toast } from "react-toastify";

export function doSetToken(token: string) {
  localStorage.setItem("token", token); // make up your own token
}

export function removeToken() {
  localStorage.removeItem("token");
}

export function fetchToken() {
  return localStorage.getItem("token");
}

export async function fetchApi(url: string, options: any = null) {
  if (options) {
    options.headers.Authorization = `Bearer ${fetchToken()}`; 
  } else {
    options = {
      headers: {
        Authorization: `Bearer ${fetchToken()}`
      }
    };
  }

  const res = await fetch(url, options).then((res) => {
    if (res.ok) {
      return res.json();
    }
    throw res;
  }).catch(async (err) => {
    const res = await err.json();
    
    if (res.message) {
      toast.error(res.message);     
    }
  });
  
  return res;
}