import { useRouter } from "next/navigation";
const API_URL = process.env.NEXT_PUBLIC_API_URL;

console.log(API_URL);
// Pista — así se hace una petición POST en TypeScript
export const login = async (mail: string, password: string) => {
  try {
    const respuesta = await fetch(`${API_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mail, password }),
    });
    return respuesta.json();
  } catch (error) {
    console.error("Error:", error);
  }
};
export const fetchAPI = async (pathUrl: string, access_token: string) => {
  let response = [];
  const data = fetch(`${API_URL}${pathUrl}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${access_token}`,
    },
    body: JSON.stringify({ access_token: access_token }),
  })
    .then((res) => {
      if (res.status === 401) {
        // Opción A: Redirigir de inmediato
        localStorage.removeItem("token");
        throw new Error("No autorizado");
      }
      if (!res.ok) {
        throw new Error("Otro error del servidor");
      }
      const resJson = res.json();
      return resJson;
    })
    .catch((err) => console.error(err));
  return data;
};
