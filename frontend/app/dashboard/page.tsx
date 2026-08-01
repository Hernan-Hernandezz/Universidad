"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

const Dashboard = () => {
  const router = useRouter();
  const [horarios, setHorarios] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login");
      return;
    }
    const access_token = { access_token: token };
    fetch(`${API_URL}/auth/token`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(access_token),
    })
      .then((res) => res.json())
      .then((datos) => console.log(datos))
      .catch((err) => console.error(err));
  }, []);
  const salir = () => {
    localStorage.removeItem("token");
    router.push("/login");
  };

  return (
    <div>
      <h1>Dashboard</h1>
      <form>
        <button onClick={salir}>salir</button>
      </form>
    </div>
  );
};

export default Dashboard;
