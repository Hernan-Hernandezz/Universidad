'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { fetchAPI } from '../../lib/api';

const Dashboard = () => {
  const router = useRouter();
  //defino los estados para los llamasdos a la API
  const [horarios, setHorarios] = useState([]);
  const [resumen, setResumen] = useState([]);
  const [tareas, setTareas] = useState([]);
  useEffect(() => {
    const cargarDatos = async () => {
      const token = localStorage.getItem('token');
      if (!token) {
        router.push('/login');
        return;
      }
      //llamados a la api desde el la funcion fetchAPI que hace verificacion de login
      const dataHorarios = await fetchAPI('/user/horarios', token);
      const dataResumen = await fetchAPI('/user/academic_summary', token);
      const dataTareas = await fetchAPI('/user/pending_tasks', token);
      //asigno los valores a los estados para pòsterior mente poder mostrarlos
      setResumen(dataResumen);
      setHorarios(dataHorarios);
      setTareas(dataTareas);
    };
    cargarDatos();
  }, []);
  const formatearFecha = (fechaISO: string) => {
    const fecha = new Date(fechaISO);
    return fecha.toLocaleDateString('es-CO', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };
  return (
    <div className="flex w-full justify-center gap-5">
      {/* contiene las proximas clases del estudiante*/}
      <div className="w-2xs">
        <h2 className="capitalize">proximas clases</h2>
        <ul className="flex h-fit flex-col">
          {horarios.slice(0, 3).map((h, index) => (
            <li key={index} className="m-5 list-disc">
              <p className="text-base font-bold">
                {h.hora_inicio} - {h.hora_fin}
              </p>
              <div className="pl-2">
                <p>{h.nombre_materia}</p>
                <p>{formatearFecha(h.fecha_proxima_clase)}</p>
                <p>{h.aula}</p>
              </div>
            </li>
          ))}
        </ul>
      </div>
      {/*contiene un resumen de las notas del estudiante*/}
      <div>
        <h2>Resumen Académico</h2>
        <div className="grid h-fit w-max grid-cols-2 text-left">
          <p>asignatura</p>
          <p>nota</p>
          {resumen.map((r, index) => (
            <div className="col-span-2 grid grid-cols-2" key={index}>
              <p>{r.nombre_materia}</p>
              <p>Nota: {r.nota_final ?? 'Sin calificar'}</p>
            </div>
          ))}
        </div>
      </div>
      {/*contiene las tareas pendientes del estudiante*/}
      <div>
        <h2>tareas pendientes</h2>
        <div className="flex flex-col">
          {tareas.map((r, index) => (
            <div key={index} className="m-2 grid grid-cols-3">
              <p>{r.asignatura}</p>
              <p>{r.titulo_tarea}</p>
              <p>{formatearFecha(r.fecha_entrega)}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
