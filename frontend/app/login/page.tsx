"use client";
import { useRouter } from "next/navigation";
import { useRef } from "react";

const Input = ({ ref, placeholder, name, type }) => {
  return (
    <input
      name={name}
      type={type}
      ref={ref}
      placeholder={placeholder}
      // onChange={(e) => setMail(e.target.value)}
      className="h-6 border-2 border-primary p-5 rounded-full"
    />
  );
};

const Page = () => {
  const inputEmail = useRef(null);
  const inputPassword = useRef(null);
  const router = useRouter();
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    const mail = inputEmail.current.value;
    const password = inputPassword.current.value;
    const API_URL = process.env.NEXT_PUBLIC_API_URL;
    e.preventDefault(); // evita que recargue la página
    try {
      const respuesta = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mail, password }),
      });
      if (respuesta.ok) {
        const datos = await respuesta.json();
        localStorage.setItem("token", datos.access_token);
        router.push("/");
      }
    } catch (e) {
      console.error(e);
    }
  };
  return (
    <div className="w-screen h-screen flex justify-center items-center capitalize">
      <div className=" flex flex-col justify-center">
        <h1 className="text-3xl px-5 font-bold mb-3">inicio de sesion</h1>
        <form
          className="grid grid-cols-1 h-3/4 gap-3 justify-between content-center justify-items-center"
          method="POST"
          onSubmit={handleSubmit}
        >
          {/* <label htmlFor="mail">mail:</label> */}
          <Input
            ref={inputEmail}
            name="mail"
            type="email"
            placeholder="correo institucional"
          />
          {/* <label htmlFor="password">password</label> */}
          <Input
            name="password"
            type="password"
            ref={inputPassword}
            placeholder="contraseña"
            // onChange={(e) => setPassword(e.target.value)}
          />
          <button
            className="bg-primary w-full text-white  h-6 p-5 capitalize rounded-full flex items-center justify-center hover:cursor-pointer"
            type="submit"
          >
            iniciar sesíon
          </button>
          <p className="text-primary">¿olvidaste tu contraseña?</p>
        </form>
      </div>
    </div>
  );
};

export default Page;
