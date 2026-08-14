"use client";
import { useState, useEffect } from "react";
import { fetchAPI } from "../lib/api";
import { useRouter } from "next/navigation";
const Horarios = () => {
  const router = useRouter();
  const [horarios, setHorarios] = useState([]);
  useEffect(() => {
    const cargarDatos = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        router.push("/login");
        return;
      }
      //llamados a la api desde el la funcion fetchAPI que hace verificacion de login
      const dataHorarios = await fetchAPI("/user/horarios", token);
      setHorarios(dataHorarios);
    };
    cargarDatos();
  }, []);
  const formatearFecha = (fechaISO: string) => {
    const fecha = new Date(fechaISO);
    return fecha.toLocaleDateString("es-CO", {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };
  return (
    <div>
      <h1>Horarios</h1>
    </div>
  );
};

export default Horarios;
