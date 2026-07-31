"use client";
import { useRouter } from "next/navigation";
// import { login } from "../lib/api";
import { useState } from "react";
import { useRef } from "react";

const Page = () => {
  // const [mail, setMail] = useState("");
  // const [password, setPassword] = useState("");
  const inputEmail = useRef(null);
  const inputPassword = useRef(null);
  const router = useRouter();
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    const mail = inputEmail.current.value;
    const password = inputPassword.current.value;
    const API_URL = process.env.NEXT_PUBLIC_API_URL;
    e.preventDefault(); // evita que recargue la página
    try {
      const respuesta = await fetch(`http://localhost:8000/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mail, password }),
      });
      if (respuesta.ok) {
        const datos = await respuesta.json();
        localStorage.setItem("token", datos.access_token);
        router.push("/dashboard");
      }
    } catch (e) {
      console.error(e);
    }
  };
  return (
    <form method="POST" onSubmit={handleSubmit}>
      <label htmlFor="mail">mail:</label>
      <input
        name="mail"
        type="email"
        ref={inputEmail}
        // onChange={(e) => setMail(e.target.value)}
        className="border-2 border-black"
      />
      <label htmlFor="password">password</label>
      <input
        name="password"
        type="password"
        ref={inputPassword}
        // onChange={(e) => setPassword(e.target.value)}
      />
      <button type="submit">ingresar</button>
    </form>
  );
};

export default Page;
