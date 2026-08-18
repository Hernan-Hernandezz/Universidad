'use client';
import { useState, useEffect } from 'react';
import { fetchAPI } from '../../lib/api';
import { useRouter } from 'next/navigation';
import { z } from 'zod';

const dias = ['lunes', 'martes', 'miercoles', 'jueves', 'vierne', 'sabado', 'domingo'];
const formatearFecha = (fechaISO: string) => {
  const fecha = new Date(fechaISO);
  return fecha.toLocaleDateString('es-CO', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
};
const horarioSchema = z.object({
  fecha_proxima_clase: z.string(),
  hora_fin: z.iso.time(),
  hora_inicio: z.iso.time(),
  id_dia_semana: z.number(),
  id_clase_horario: z.number(),
  nombre_materia: z.string(),
  aula: z.string(),
});
const listHorariosSchemas = z.array(horarioSchema);
const diaSchema = z.object({
  clases: listHorariosSchemas,
  dia: z.string(),
});
type HorarioType = z.infer<typeof horarioSchema>;
type DiaType = z.infer<typeof diaSchema>;

const Dia = ({ clases, dia }: DiaType) => {
  return (
    <ul className="flex h-full flex-col items-center border">
      <h3 className="bold capitalize">{dia}</h3>
      {clases.map((h: HorarioType, index) => (
        <li key={index} className="m-5 list-disc">
          <p className="text-base font-bold">
            {h.hora_inicio} - {h.hora_fin}
          </p>
          <div className="pl-2">
            <p>{h.id_dia_semana}</p>
            <p>{h.nombre_materia}</p>
            <p>{formatearFecha(h.fecha_proxima_clase)}</p>
            <p>{h.aula}</p>
          </div>
        </li>
      ))}
    </ul>
  );
};

const Horarios = () => {
  const router = useRouter();
  const [horarios, setHorarios] = useState([[], [], [], [], []]);
  useEffect(() => {
    const cargarDatos = async () => {
      const token = localStorage.getItem('token');
      if (!token) {
        router.push('/login');
        return;
      }
      //llamados a la api desde el la funcion fetchAPI que hace verificacion de login
      const dataHorarios = await fetchAPI('/user/horarios', token);
      const resultado = listHorariosSchemas.safeParse(dataHorarios);
      if (resultado.success) {
        // datos validados y tipados
        const datos = horarios;
        resultado.data.map((data: HorarioType) => {
          datos[data.id_dia_semana - 1].push(data);
        });
        setHorarios(datos);
        console.log(horarios);
      } else {
        console.error(resultado.error); // muestra qué campo falló
      }
    };
    cargarDatos();
  }, []);
  return (
    <div>
      <h1>Horarios</h1>
      <div>
        <h2 className="capitalize">proximas clases</h2>
        <div className="grid grid-cols-5 justify-around gap-2 px-2">
          {horarios.map((list, index) => {
            return <Dia clases={list} key={index} dia={dias[index]} />;
          })}
        </div>
      </div>
    </div>
  );
};

export default Horarios;
