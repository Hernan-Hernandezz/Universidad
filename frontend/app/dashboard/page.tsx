"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { fetchAPI } from "../lib/api";
import Exit from "../Components/Exit";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

const Dashboard = () => {
  const router = useRouter();
  const [horarios, setHorarios] = useState([]);
  const [resumen, setResumen] = useState([]);
  useEffect(() => {
    const cargarDatos = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        router.push("/login");
        return;
      }

      const dataHorarios = await fetchAPI("/user/horarios", token);
      setHorarios(dataHorarios);

      const dataResumen = await fetchAPI("/user/academic_summary", token);
      setResumen(dataResumen);
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
      <h1>Dashboard</h1>

      <h2 className="capitalize">proximas clases</h2>
      <ul className="flex flex-col">
        {horarios.map((h, index) => (
          <li key={index} className="">
            <p className="font-bold">
              {h.hora_inicio} - {h.hora_fin}
            </p>
            <div className="pl-2">
              <p>{h.nombre_materia}</p>
              <p>{formatearFecha(h.fecha_proxima_clase)}</p>
            </div>
          </li>
        ))}
      </ul>

      <h2>Resumen Académico</h2>
      <ul>
        {resumen.map((r, index) => (
          <div key={index}>
            <p>{r.nombre_materia}</p>
            <p>Nota: {r.nota_final ?? "Sin calificar"}</p>
          </div>
        ))}
      </ul>
      <Exit />
    </div>
  );
};

export default Dashboard;
