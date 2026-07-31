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
