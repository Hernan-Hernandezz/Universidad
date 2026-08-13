"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { fetchAPI } from "../lib/api";
import Header from "../Components/Header";

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
    <div className="flex w-screen gap-5">
      <Header />
      <div className="w-2xs">
        <h2 className="capitalize">proximas clases</h2>
        <ul className="flex flex-col h-fit">
          {horarios.map((h, index) => (
            <li key={index} className="list-disc m-5 ">
              <p className="font-bold text-base">
                {h.hora_inicio} - {h.hora_fin}
              </p>
              <div className="pl-2">
                <p>{h.nombre_materia}</p>
                <p>{formatearFecha(h.fecha_proxima_clase)}</p>
              </div>
            </li>
          ))}
        </ul>
      </div>

      <h2>Resumen Académico</h2>
      <table className="h-fit w-max text-left ">
        <tr className="text-center">
          <th scope="col">asignatura</th>
          <th scope="col">nota</th>
        </tr>
        {resumen.map((r, index) => (
          <>
            <tr className="p-1" key={index}>
              <td>{r.nombre_materia}</td>
              <td>Nota: {r.nota_final ?? "Sin calificar"}</td>
            </tr>
          </>
        ))}
      </table>
    </div>
  );
};

export default Dashboard;
