'use client';
import { useRouter } from 'next/navigation';
import { useRef } from 'react';

const Input = ({ ref, placeholder, name, type }) => {
  return (
    <input
      name={name}
      type={type}
      ref={ref}
      placeholder={placeholder}
      // onChange={(e) => setMail(e.target.value)}
      className="border-primary h-6 rounded-full border-2 p-5"
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
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mail, password }),
      });
      if (respuesta.ok) {
        const datos = await respuesta.json();
        localStorage.setItem('token', datos.access_token);
        router.push('/dashboard');
      }
    } catch (e) {
      console.error(e);
    }
  };
  return (
    <div className="flex h-screen w-screen items-center justify-center capitalize">
      <div className="flex flex-col justify-center">
        <h1 className="mb-3 px-5 text-3xl font-bold">inicio de sesion</h1>
        <form
          className="grid h-3/4 grid-cols-1 content-center justify-between justify-items-center gap-3"
          method="POST"
          onSubmit={handleSubmit}
        >
          {/* <label htmlFor="mail">mail:</label> */}
          <Input ref={inputEmail} name="mail" type="email" placeholder="correo institucional" />
          {/* <label htmlFor="password">password</label> */}
          <Input
            name="password"
            type="password"
            ref={inputPassword}
            placeholder="contraseña"
            // onChange={(e) => setPassword(e.target.value)}
          />
          <button
            className="bg-primary flex h-6 w-full items-center justify-center rounded-full p-5 text-white capitalize hover:cursor-pointer"
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
